import re
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.schemas.common import success_response
from app.schemas.quiz import QuizSubmitRequest
from app.models.quiz import Quiz, QuizQuestion, QuizRecord, QuizAnswer

router = APIRouter()
record_router = APIRouter()


@router.get("")
def list_quizzes(
    category: str | None = None, 
    keyword: str = "", 
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db)
):
    page_size = 20
    
    # 从数据库查询 quizzes
    query = db.query(Quiz)
    if category:
        query = query.filter(Quiz.category == category)
    if keyword:
        query = query.filter(Quiz.title.contains(keyword))
    
    total = query.count()
    quizzes_db = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 转换为前端需要的格式
    result_list = []
    for quiz in quizzes_db:
        result_list.append({
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "questionCount": quiz.question_count,
            "timeLimit": quiz.time_limit_minutes,
            "passScore": quiz.pass_score,
            "totalScore": quiz.total_score,
            "category": quiz.category,
            "difficulty": quiz.difficulty,
            "tags": quiz.tags,
            "createdAt": quiz.created_at.isoformat() if quiz.created_at else None,
            "attemptCount": 0,  # 可以从 QuizRecord 统计
            "bestScore": None,
        })
    
    return success_response({
        "list": result_list,
        "total": total,
        "page": page,
        "pageSize": page_size,
    })


@router.get("/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return success_response({
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "questionCount": quiz.question_count,
        "timeLimit": quiz.time_limit_minutes,
        "passScore": quiz.pass_score,
        "totalScore": quiz.total_score,
        "category": quiz.category,
        "difficulty": quiz.difficulty,
        "tags": quiz.tags,
        "createdAt": quiz.created_at.isoformat() if quiz.created_at else None,
        "attemptCount": db.query(QuizRecord).filter(QuizRecord.quiz_id == quiz.id).count(),
        "bestScore": None,
    })


@router.get("/{quiz_id}/questions")
def get_questions(quiz_id: int, db: Session = Depends(get_db)):
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.position).all()
    
    result = []
    for q in questions:
        stem_text = q.stem
        options = []
        
        # 对于单选题，尝试从题干中解析选项
        if q.question_type == 'single_choice':
            # 匹配 A. xxx B. xxx C. xxx D. xxx 格式
            pattern = r'([A-D])\.\s*([^A-D]*(?:[^A-D]|$))'
            matches = re.findall(pattern, stem_text)
            
            if matches:
                # 找到第一个选项的位置，提取纯问题文本
                first_option_pos = stem_text.find('A.')
                if first_option_pos > 0:
                    stem_text = stem_text[:first_option_pos].strip()
                
                for label, text in matches:
                    if text.strip():
                        options.append({
                            "label": label,
                            "text": text.strip()
                        })
        
        # 如果数据库中有单独的选项表数据，也合并进来
        if q.options and not options:
            for opt in q.options:
                options.append({
                    "label": opt.label,
                    "text": opt.text,
                })
        
        result.append({
            "id": q.id,
            "quizId": q.quiz_id,
            "type": q.question_type,
            "stem": stem_text,
            "options": options,
            "answer": q.correct_answer,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "category": q.category,
            "tags": q.tags,
        })
    
    return success_response(result)


@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: int, payload: QuizSubmitRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    questions_db = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    
    # 计算每道题的分值
    score_per_question = max(1, round(quiz.total_score / len(questions_db)))
    
    # 创建记录
    record = QuizRecord(
        quiz_id=quiz_id,
        user_id=user["id"],
        total_score=quiz.total_score,
        total_questions=len(questions_db),
        time_spent_seconds=0,
    )
    db.add(record)
    db.flush()  # 获取 record.id
    
    total_score = 0
    correct_count = 0
    
    for question in questions_db:
        user_answer = payload.answers.get(str(question.id))
        is_correct = False
        awarded = 0
        
        if user_answer is not None:
            # 比较答案（注意 correct_answer 可能是 JSON 数组）
            if isinstance(question.correct_answer, list):
                # 多选题：比较两个列表
                if isinstance(user_answer, list) and sorted(user_answer) == sorted(question.correct_answer):
                    is_correct = True
                    awarded = score_per_question
            else:
                # 单选题或判断题
                if str(user_answer) == str(question.correct_answer):
                    is_correct = True
                    awarded = score_per_question
        
        if is_correct:
            total_score += awarded
            correct_count += 1
        
        # 保存答案
        answer = QuizAnswer(
            record_id=record.id,
            question_id=question.id,
            user_answer=user_answer,
            is_correct=is_correct,
            score_awarded=awarded,
        )
        db.add(answer)
    
    # 更新记录
    record.score = total_score
    record.correct_count = correct_count
    record.submitted_at = datetime.now()
    
    db.commit()
    
    return success_response({
        "score": total_score,
        "totalScore": quiz.total_score,
        "correctCount": correct_count,
        "totalQuestions": len(questions_db),
    }, "提交成功")


@record_router.get("/my")
def my_quiz_records(user=Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(QuizRecord).filter(QuizRecord.user_id == user["id"]).order_by(QuizRecord.submitted_at.desc()).all()
    
    result = []
    for record in records:
        quiz = db.query(Quiz).filter(Quiz.id == record.quiz_id).first()
        result.append({
            "id": record.id,
            "quizId": record.quiz_id,
            "quizTitle": quiz.title if quiz else "",
            "score": record.score,
            "totalScore": record.total_score,
            "correctCount": record.correct_count,
            "totalQuestions": record.total_questions,
            "submittedAt": record.submitted_at.isoformat() if record.submitted_at else None,
        })
    
    return success_response(result)
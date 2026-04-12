from typing import Literal

from pydantic import BaseModel


class QuestionOptionOut(BaseModel):
    label: str
    text: str


class QuestionOut(BaseModel):
    id: int
    type: Literal["single", "multiple", "judge", "essay"]
    stem: str
    options: list[QuestionOptionOut] | None = None
    answer: str | list[str]
    explanation: str
    difficulty: Literal["easy", "medium", "hard"]
    category: str
    tags: list[str]


class QuizOut(BaseModel):
    id: int
    title: str
    description: str
    questionCount: int
    timeLimit: int
    passScore: int
    totalScore: int
    attemptCount: int
    bestScore: int | None = None
    category: str
    tags: list[str]
    createdAt: str


class QuizSubmitRequest(BaseModel):
    answers: dict[str, str | list[str]]


class UserAnswerOut(BaseModel):
    questionId: int
    userAnswer: str | list[str]
    isCorrect: bool
    score: int


class QuizRecordOut(BaseModel):
    id: int
    quizId: int
    quizTitle: str
    score: int
    totalScore: int
    correctCount: int
    totalQuestions: int
    timeSpent: int
    submittedAt: str
    answers: list[UserAnswerOut]


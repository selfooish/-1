/**
 * 劳动技能分类映射
 */
export const CATEGORY_CONFIG: Record<
  string,
  { label: string; icon: string; color: string; description: string }
> = {
  家电维修: {
    label: '家电维修',
    icon: '⚡',
    color: '#e67e22',
    description: '电饭煲、电风扇、电暖器等小家电维修技能',
  },
  收纳整理: {
    label: '收纳整理',
    icon: '📦',
    color: '#3498db',
    description: '衣柜、厨房、书桌的高效收纳方法',
  },
  绿植养护: {
    label: '绿植养护',
    icon: '🌿',
    color: '#27ae60',
    description: '家庭常见绿植的养护与繁殖技巧',
  },
  手工制作: {
    label: '手工制作',
    icon: '✂️',
    color: '#9b59b6',
    description: '环保手工、DIY创意、手账装饰等',
  },
  安全常识: {
    label: '安全常识',
    icon: '🛡️',
    color: '#e74c3c',
    description: '消防、用电、防溺水等生活安全知识',
  },
  烹饪基础: {
    label: '烹饪基础',
    icon: '🍳',
    color: '#f39c12',
    description: '家常菜烹饪技巧与食品安全知识',
  },
  衣物护理: {
    label: '衣物护理',
    icon: '👕',
    color: '#1abc9c',
    description: '衣物洗涤、晾晒、熨烫与保养技巧',
  },
  清洁卫生: {
    label: '清洁卫生',
    icon: '🧹',
    color: '#95a5a6',
    description: '家庭日常清洁与卫生防护方法',
  },
}

/**
 * 难度等级配置
 */
export const DIFFICULTY_CONFIG = {
  easy: { label: '入门', color: '#27ae60', bgColor: 'rgba(39,174,96,0.1)' },
  medium: { label: '进阶', color: '#f39c12', bgColor: 'rgba(243,156,18,0.1)' },
  hard: { label: '高级', color: '#e74c3c', bgColor: 'rgba(231,76,60,0.1)' },
}

/**
 * 格式化时长（如 "45:30" → "45分30秒"）
 */
export function formatDuration(minutes: number): string {
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  if (h > 0) return `${h}h${m > 0 ? m + 'm' : ''}`
  return `${m}m`
}

/**
 * 格式化秒数为时分秒
 */
export function formatTime(seconds: number): string {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  if (h > 0) return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

/**
 * 格式化数字（1000 → 1k）
 */
export function formatCount(n: number): string {
  if (n >= 10000) return (n / 10000).toFixed(1) + 'w'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return String(n)
}

/**
 * 根据积分计算等级
 */
export function getLevelFromPoints(points: number): { level: number; title: string; progress: number } {
  const levels = [
    { min: 0, level: 1, title: '劳动新手' },
    { min: 100, level: 2, title: '劳动学徒' },
    { min: 300, level: 3, title: '劳动助手' },
    { min: 600, level: 4, title: '劳动能手' },
    { min: 1000, level: 5, title: '劳动标兵' },
    { min: 1500, level: 6, title: '劳动达人' },
    { min: 2100, level: 7, title: '劳动巧匠' },
    { min: 2800, level: 8, title: '劳动高手' },
    { min: 3600, level: 9, title: '劳动大师' },
    { min: 5000, level: 10, title: '劳动传奇' },
  ]
  for (let i = levels.length - 1; i >= 0; i--) {
    const currentLevel = levels[i]
    if (currentLevel && points >= currentLevel.min) {
      const nextMin = levels[i + 1]?.min ?? currentLevel.min + 1000
      const progress = Math.round(((points - currentLevel.min) / (nextMin - currentLevel.min)) * 100)
      return { level: currentLevel.level, title: currentLevel.title, progress }
    }
  }
  return { level: 1, title: '劳动新手', progress: 0 }
}

/**
 * 生成渐变色头像背景
 */
export function getAvatarBg(name: string): string {
  const colors = [
    'linear-gradient(135deg, #42b883, #5dd1c1)',
    'linear-gradient(135deg, #3498db, #85c1e9)',
    'linear-gradient(135deg, #9b59b6, #d7bde2)',
    'linear-gradient(135deg, #e67e22, #f0b27a)',
    'linear-gradient(135deg, #e74c3c, #f1948a)',
    'linear-gradient(135deg, #1abc9c, #76d7c4)',
  ]
  const index = name.charCodeAt(0) % colors.length
  return colors[index] ?? colors[0] ?? 'linear-gradient(135deg, #42b883, #5dd1c1)'
}

export function toIso(date: string | Date) {
  return new Date(date).toISOString()
}

export function calcLevel(points: number) {
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

  for (let i = levels.length - 1; i >= 0; i -= 1) {
    const current = levels[i]
    if (current && points >= current.min) {
      return current
    }
  }

  return levels[0]!
}

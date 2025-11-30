export interface HabitWeekStat {
  week: string;        // "2025-W47"
  completed: number;
  missed: number;
}

export interface HabitStats {
  habit_id: number;

  total_completed: number;
  total_missed: number;
  total_pending: number;

  current_streak: number;
  max_streak: number;

  repeat_limit: number | null;
  progress_percent: number | null;

  last_30_days: Record<string, string>; // "2025-11-26": "completed"
  per_week: HabitWeekStat[];
}

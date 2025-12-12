export interface HabitInstanceFilters {
  status?: string;
  date?: string;   // формат YYYY-MM-DD
}

export interface HabitInstance {
  id: number;
  scheduled_datetime: string;
  status: string;
  habit: number;
  action: string;
  time: string;
}

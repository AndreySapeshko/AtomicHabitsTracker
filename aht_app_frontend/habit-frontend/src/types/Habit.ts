export interface Habit {
  id: number;

  action: string;
  place: string;
  time_of_day: string;

  is_pleasant: boolean;
  related_pleasant_habit: number | null;
  reward_text: string | null;

  periodicity_days: number;    // 1,2,3,5,7
  repeat_limit: number;        // 21,30,45

  grace_minutes: number;       // backend вычисляет
  fix_minutes: number;         // backend вычисляет

  is_public: boolean;
  is_active: boolean;

  created_at: string;
}


export interface HabitCreateData {
  action: string;
  place: string;
  time_of_day: string;

  is_pleasant: boolean;
  related_pleasant_habit: number | null;
  reward_text: string | null;

  periodicity_days: number;
  repeat_limit: number;

  is_public: boolean;
  is_active?: boolean;
}

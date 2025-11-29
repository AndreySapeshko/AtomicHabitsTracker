export interface Habit {
  id: number;
  action: string;
  place: string;
  time: string;
  is_pleasant: boolean;
  related_pleasant_habit: number | null;
  reward_text: string | null;
  periodicity: string[];
  duration: number;
  fix_deadline: boolean;
}

export type HabitCreateData = Omit<Habit, "id">;

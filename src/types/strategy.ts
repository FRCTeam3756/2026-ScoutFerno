export interface TeamSummary {
  team_number: number;
  name: string | null;
  competitions: string[];
  match_count: number;
  interview_count: number;
  primary_color: string | null;
  secondary_color: string | null;
}

interface RecordBase {
  team_number: number;
  competition: string;
}

export interface MatchRecord extends RecordBase {
  match_number: number;
  robot_position: string | null;
  no_show: boolean | null;
  auto_fuel_scored: number | null;
  auto_collection_location: string | null;
  auto_addition_actions: string | null;
  auto_stuck: boolean | null;
  auto_climbed: boolean | null;
  alliance_won_auto: boolean | null;
  teleop_fuel_scored: number | null;
  field_usability: string | null;
  defended_by_opponent: boolean | null;
  fuel_fed_passed: number | null;
  opp_zone_actions: string | null;
  climbed: boolean | null;
  climb_position: string | null;
  mechanical_issue: boolean | null;
  died: boolean | null;
  fell_over: boolean | null;
  scoring_efficiency: number | null;
  scored_how: string | null;
  scoring_location: string | null;
  feeding_skills: number | null;
  passed_how: string | null;
  defense_skill: number | null;
  cards: string | null;
  comments: string | null;
  id?: number;
}

export interface InterviewRecord extends RecordBase {
  ball_storage: number | null;
  drivetrain_type: string | null;
  shooter_type: string | null;
  shooter_ball_width: number | null;
  intake_type: string | null;
  intake_amount: number | null;
  field_elements_usability: string | null;
  climb_level: string | null;
  climb_positions: string | null;
  id?: number;
}

export interface TeamAllData {
  match: MatchRecord[];
  interview: InterviewRecord[];
}

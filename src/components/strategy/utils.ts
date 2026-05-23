import scoutingConfig from "../../assets/config.json";
import type {
  TeamAllData,
  TeamSummary,
} from "../../types/strategy";
import type { MatchBundle, KeyValueField } from "./types";

const FIELD_LABELS = new Map<string, string>(
  scoutingConfig.sections.flatMap((section) =>
    section.fields.map((field) => [field.code, field.title] as const),
  ),
);

const FIELD_LABEL_ALIASES: Record<string, string> = {
  auto_addition_actions: "Other Auto Actions",
  scoring_efficiency: "Scoring Effectiveness",
  feeding_skills: "Passing Effectiveness",
  defense_skill: "Defense Skill",
  fuel_fed_passed: "Fuel Herded & Passed",
  estimated_fuel_passed: "Fuel Herded & Passed",
  subjective_scoring_skill: "Scoring Effectiveness",
  subjective_passing_skill: "Passing Effectiveness",
  subjective_defense_skill: "Defense Skill",
};

export const MATCH_FIELD_ORDER = [
  "competition",
  "match_number",
  "team_number",
  "robot_position",
  "no_show",
  "auto_fuel_scored",
  "auto_collection_location",
  "auto_addition_actions",
  "auto_additional_actions",
  "auto_stuck",
  "auto_climbed",
  "alliance_won_auto",
  "teleop_fuel_scored",
  "traversal_ability",
  "defended_by_opponent",
  "fuel_fed_passed",
  "estimated_fuel_passed",
  "opp_zone_actions",
  "climbed",
  "climb_position",
  "mechanical_issue",
  "died",
  "fell_over",
  "scoring_efficiency",
  "subjective_scoring_skill",
  "scored_how",
  "scoring_location",
  "feeding_skills",
  "subjective_passing_skill",
  "passed_how",
  "defense_skill",
  "subjective_defense_skill",
  "cards",
  "comments",
] as const;

export const INTERVIEW_FIELD_ORDER = [
  "competition",
  "team_number",
  "ball_storage",
  "drivetrain_type",
  "shooter_type",
  "shooter_ball_width",
  "intake_type",
  "intake_amount",
  "field_elements_usability",
  "climb_level",
  "climb_positions",
] as const;

export function parseTeamNumber(value: string | null) {
  if (!value) {
    return null;
  }

  const match = value.match(/\d+/);

  if (!match) {
    return null;
  }

  const parsed = Number.parseInt(match[0], 10);
  return Number.isFinite(parsed) ? parsed : null;
}

export function formatTeamLabel(team: TeamSummary) {
  return team.name
    ? `Team ${team.team_number} • ${team.name}`
    : `Team ${team.team_number}`;
}

export function formatValue(value: unknown) {
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(1);
  }

  if (typeof value === "string" && value.trim()) {
    return value;
  }

  if (Array.isArray(value)) {
    const parts = value
      .map((item) => (typeof item === "string" ? item.trim() : String(item)))
      .filter(Boolean);
    return parts.length ? parts.join(", ") : "—";
  }

  return "—";
}

function humanizeKey(key: string) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function getFieldLabel(key: string) {
  return FIELD_LABEL_ALIASES[key] ?? FIELD_LABELS.get(key) ?? humanizeKey(key);
}

export function buildVisibleFields<T extends object>(
  data: T,
  orderedKeys: readonly string[],
): KeyValueField<T>[] {
  const keys = Object.keys(data as Record<string, unknown>).filter(
    (key) => key !== "id",
  );
  const orderedSet = new Set(orderedKeys);
  const ordered = orderedKeys.filter((key) => keys.includes(key));
  const extras = keys
    .filter((key) => !orderedSet.has(key))
    .sort((left, right) => left.localeCompare(right));

  return [...ordered, ...extras].map((key) => ({
    key: key as keyof T,
    label: getFieldLabel(key),
  }));
}

export function average(values: Array<number | null | undefined>) {
  const valid = values.filter(
    (value): value is number => typeof value === "number",
  );

  if (!valid.length) {
    return null;
  }

  return valid.reduce((sum, value) => sum + value, 0) / valid.length;
}

export function percent(part: number, total: number) {
  if (!total) {
    return "—";
  }

  return `${Math.round((part / total) * 100)}%`;
}

export function uniqueNonEmpty(values: Array<string | null | undefined>) {
  return [
    ...new Set(
      values.filter((value): value is string => Boolean(value && value.trim())),
    ),
  ];
}

export function buildMatchBundles(teamData: TeamAllData): MatchBundle[] {
  const bundles = new Map<string, MatchBundle>();

  const ensureBundle = (competition: string, matchNumber: number) => {
    const key = `${competition}:${matchNumber}`;

    if (!bundles.has(key)) {
      bundles.set(key, { competition, matchNumber });
    }

    return bundles.get(key)!;
  };

  for (const record of teamData.match) {
    ensureBundle(record.competition, record.match_number).match = record;
  }

  return [...bundles.values()].sort((left, right) => {
    if (left.competition === right.competition) {
      return right.matchNumber - left.matchNumber;
    }

    return right.competition.localeCompare(left.competition);
  });
}

export type StrategyComment = {
  id: string;
  label: string;
  text: string;
};

export type StrategyMetrics = {
  matchBundles: MatchBundle[];
  averageAuto: number | null;
  averageTeleop: number | null;
  averageEfficiency: number | null;
  averagePassed: number | null;
  climbs: number;
  reliabilityEvents: number;
  comments: StrategyComment[];
  interviewTags: string[];
  hasTeamData: boolean;
  defensePlayedCount: number;
  noShowCount: number;
  mechanicalIssueCount: number;
  knockdownOrDeathCount: number;
};

export function buildStrategyMetrics(
  teamData: TeamAllData | null,
): StrategyMetrics {
  const matchRecords = teamData?.match ?? [];
  const interviewRecords = teamData?.interview ?? [];

  return {
    matchBundles: teamData ? buildMatchBundles(teamData) : [],
    averageAuto: average(matchRecords.map((record) => record.auto_fuel_scored)),
    averageTeleop: average(
      matchRecords.map((record) => record.teleop_fuel_scored),
    ),
    averageEfficiency: average(
      matchRecords.map((record) => record.scoring_efficiency),
    ),
    averagePassed: average(
      matchRecords.map((record) => record.fuel_fed_passed),
    ),
    climbs: matchRecords.filter((record) => record.climbed).length,
    reliabilityEvents: matchRecords.filter(
      (record) => record.mechanical_issue || record.died || record.fell_over,
    ).length,
    comments: matchRecords
      .filter((record) => record.comments && record.comments.trim())
      .map((record) => ({
        id: `${record.competition}-${record.match_number}`,
        label: `${record.competition.toUpperCase()} M${record.match_number}`,
        text: record.comments!.trim(),
      })),
    interviewTags: [
      ...uniqueNonEmpty(interviewRecords.map((record) => record.drivetrain_type)),
      ...uniqueNonEmpty(interviewRecords.map((record) => record.shooter_type)),
      ...uniqueNonEmpty(interviewRecords.map((record) => record.climb_level)),
    ].slice(0, 6),
    hasTeamData: Boolean(matchRecords.length || interviewRecords.length),
    defensePlayedCount: matchRecords.filter(
      (record) => (record.defense_skill || 0) > 0,
    ).length,
    noShowCount: matchRecords.filter((record) => record.no_show).length,
    mechanicalIssueCount: matchRecords.filter(
      (record) => record.mechanical_issue,
    ).length,
    knockdownOrDeathCount: matchRecords.filter(
      (record) => record.died || record.fell_over,
    ).length,
  };
}

export function buildCompetitionList(
  selectedSummary: TeamSummary | undefined,
  teamData: TeamAllData | null,
) {
  return selectedSummary?.competitions.length
    ? selectedSummary.competitions
    : uniqueNonEmpty(
        teamData
          ? [
              ...teamData.match.map((record) => record.competition),
              ...teamData.interview.map((record) => record.competition),
            ]
          : [],
      );
}

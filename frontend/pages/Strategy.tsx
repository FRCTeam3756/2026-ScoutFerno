import { startTransition, useDeferredValue, useEffect, useState } from "react";
import { Search } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import type {
  AutonomousRecord,
  EndgameRecord,
  InterviewRecord,
  PostmatchRecord,
  PrematchRecord,
  TeamAllData,
  TeamSummary,
  TeleopRecord,
} from "../types/strategy";
import { fetchTeamData, fetchTeamSummaries } from "../util/strategy";
import { getTeamTheme } from "../util/teamTheme";

type MatchBundle = {
  competition: string;
  matchNumber: number;
  prematch?: PrematchRecord;
  autonomous?: AutonomousRecord;
  teleop?: TeleopRecord;
  endgame?: EndgameRecord;
  postmatch?: PostmatchRecord;
};

type KeyValueField<T extends object> = {
  key: keyof T;
  label: string;
};

const PREMATCH_FIELDS: KeyValueField<PrematchRecord>[] = [
  { key: "scouter", label: "Scouter" },
  { key: "robot_position", label: "Robot Position" },
  { key: "no_show", label: "No Show" },
];

const AUTONOMOUS_FIELDS: KeyValueField<AutonomousRecord>[] = [
  { key: "auto_fuel_scored", label: "Auto Fuel Scored" },
  { key: "auto_collection_location", label: "Collection Location" },
  { key: "auto_addition_actions", label: "Additional Actions" },
  { key: "auto_stuck", label: "Auto Stuck" },
  { key: "auto_climbed", label: "Auto Climbed" },
];

const TELEOP_FIELDS: KeyValueField<TeleopRecord>[] = [
  { key: "alliance_won_auto", label: "Alliance Won Auto" },
  { key: "teleop_fuel_scored", label: "Teleop Fuel Scored" },
  { key: "field_usability", label: "Field Usability" },
  { key: "defended_by_opponent", label: "Defended By Opponent" },
  { key: "fuel_fed_passed", label: "Fuel Fed / Passed" },
  { key: "opp_zone_actions", label: "Opponent Zone Actions" },
];

const ENDGAME_FIELDS: KeyValueField<EndgameRecord>[] = [
  { key: "climbed", label: "Climbed" },
  { key: "climb_position", label: "Climb Position" },
  { key: "mechanical_issue", label: "Mechanical Issue" },
  { key: "died", label: "Died" },
  { key: "fell_over", label: "Fell Over" },
];

const POSTMATCH_FIELDS: KeyValueField<PostmatchRecord>[] = [
  { key: "scoring_efficiency", label: "Scoring Efficiency" },
  { key: "scored_how", label: "Scored How" },
  { key: "scoring_location", label: "Scoring Location" },
  { key: "feeding_skills", label: "Feeding Skills" },
  { key: "passed_how", label: "Passed How" },
  { key: "defense_skill", label: "Defense Skill" },
  { key: "cards", label: "Cards" },
  { key: "comments", label: "Comments" },
];

const INTERVIEW_FIELDS: KeyValueField<InterviewRecord>[] = [
  { key: "ball_storage", label: "Ball Storage" },
  { key: "drivetrain_type", label: "Drivetrain" },
  { key: "shooter_type", label: "Shooter" },
  { key: "shooter_ball_width", label: "Shooter Width" },
  { key: "intake_type", label: "Intake" },
  { key: "intake_amount", label: "Intake Amount" },
  { key: "field_elements_usability", label: "Field Elements" },
  { key: "climb_level", label: "Climb Level" },
  { key: "climb_positions", label: "Climb Positions" },
];

function parseTeamNumber(value: string | null) {
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

function formatTeamLabel(team: TeamSummary) {
  return team.name
    ? `Team ${team.team_number} • ${team.name}`
    : `Team ${team.team_number}`;
}

function formatValue(value: unknown) {
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toFixed(1);
  }

  if (typeof value === "string" && value.trim()) {
    return value;
  }

  return "—";
}

function average(values: Array<number | null | undefined>) {
  const valid = values.filter(
    (value): value is number => typeof value === "number"
  );

  if (!valid.length) {
    return null;
  }

  return valid.reduce((sum, value) => sum + value, 0) / valid.length;
}

function percent(part: number, total: number) {
  if (!total) {
    return "—";
  }

  return `${Math.round((part / total) * 100)}%`;
}

function uniqueNonEmpty(values: Array<string | null | undefined>) {
  return [
    ...new Set(
      values.filter((value): value is string => Boolean(value && value.trim()))
    ),
  ];
}

function buildMatchBundles(teamData: TeamAllData) {
  const bundles = new Map<string, MatchBundle>();

  const ensureBundle = (competition: string, matchNumber: number) => {
    const key = `${competition}:${matchNumber}`;

    if (!bundles.has(key)) {
      bundles.set(key, { competition, matchNumber });
    }

    return bundles.get(key)!;
  };

  for (const record of teamData.prematch) {
    ensureBundle(record.competition, record.match_number).prematch = record;
  }

  for (const record of teamData.autonomous) {
    ensureBundle(record.competition, record.match_number).autonomous = record;
  }

  for (const record of teamData.teleop) {
    ensureBundle(record.competition, record.match_number).teleop = record;
  }

  for (const record of teamData.endgame) {
    ensureBundle(record.competition, record.match_number).endgame = record;
  }

  for (const record of teamData.postmatch) {
    ensureBundle(record.competition, record.match_number).postmatch = record;
  }

  return [...bundles.values()].sort((left, right) => {
    if (left.competition === right.competition) {
      return right.matchNumber - left.matchNumber;
    }

    return right.competition.localeCompare(left.competition);
  });
}

function ProfileMetric({
  label,
  value,
  caption,
  theme,
}: {
  label: string;
  value: string;
  caption: string;
  theme: ReturnType<typeof getTeamTheme>;
}) {
  return (
    <div
      className="rounded-2xl border px-4 py-4"
      style={{
        backgroundColor: theme.surfaceAlt,
        borderColor: `${theme.primary}50`,
      }}
    >
      <div
        className="text-xs uppercase tracking-[0.28em]"
        style={{ color: theme.mutedText }}
      >
        {label}
      </div>
      <div
        className="mt-2 text-3xl font-semibold tracking-tight"
        style={{ color: theme.text }}
      >
        {value}
      </div>
      <div className="mt-1 text-sm" style={{ color: theme.accentStrong }}>
        {caption}
      </div>
    </div>
  );
}

function KeyValueGrid<T extends object>({
  data,
  fields,
  theme,
}: {
  data: T;
  fields: KeyValueField<T>[];
  theme: ReturnType<typeof getTeamTheme>;
}) {
  return (
    <dl className="grid gap-3 sm:grid-cols-2">
      {fields.map((field) => (
        <div
          key={String(field.key)}
          className="rounded-xl border px-3 py-3"
          style={{
            backgroundColor: theme.surfaceAlt,
            borderColor: `${theme.primary}35`,
          }}
        >
          <dt
            className="text-[11px] uppercase tracking-[0.24em]"
            style={{ color: theme.mutedText }}
          >
            {field.label}
          </dt>
          <dd className="mt-2 text-sm leading-6" style={{ color: theme.text }}>
            {formatValue(
              (data as Record<PropertyKey, unknown>)[field.key as PropertyKey]
            )}
          </dd>
        </div>
      ))}
    </dl>
  );
}

function MatchSection<T extends object>({
  title,
  data,
  fields,
  theme,
}: {
  title: string;
  data?: T;
  fields: KeyValueField<T>[];
  theme: ReturnType<typeof getTeamTheme>;
}) {
  return (
    <section className="space-y-3">
      <div className="flex items-center gap-3">
        <div
          className="h-px flex-1"
          style={{ backgroundColor: `${theme.primary}50` }}
        />
        <h4
          className="font-sports-ns text-lg uppercase tracking-[0.18em]"
          style={{ color: theme.accent }}
        >
          {title}
        </h4>
        <div
          className="h-px flex-1"
          style={{ backgroundColor: `${theme.primary}50` }}
        />
      </div>

      {data ? (
        <KeyValueGrid data={data} fields={fields} theme={theme} />
      ) : (
        <div
          className="rounded-xl border border-dashed px-4 py-6 text-sm"
          style={{
            borderColor: `${theme.primary}45`,
            color: theme.mutedText,
            backgroundColor: theme.surfaceAlt,
          }}
        >
          No {title.toLowerCase()} entry was recorded for this match.
        </div>
      )}
    </section>
  );
}

export function Strategy() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [teamSummaries, setTeamSummaries] = useState<TeamSummary[]>([]);
  const [directoryError, setDirectoryError] = useState<string | null>(null);
  const [directoryLoading, setDirectoryLoading] = useState(true);
  const [teamData, setTeamData] = useState<TeamAllData | null>(null);
  const [teamError, setTeamError] = useState<string | null>(null);
  const [teamLoading, setTeamLoading] = useState(false);
  const [query, setQuery] = useState(searchParams.get("team") ?? "");

  const selectedTeamNumber = parseTeamNumber(searchParams.get("team"));
  const deferredQuery = useDeferredValue(query);

  useEffect(() => {
    const controller = new AbortController();

    setDirectoryLoading(true);
    setDirectoryError(null);

    fetchTeamSummaries(controller.signal)
      .then((summaries) => {
        setTeamSummaries(summaries);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }

        setDirectoryError(
          error instanceof Error
            ? error.message
            : "Unable to load the team directory."
        );
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setDirectoryLoading(false);
        }
      });

    return () => controller.abort();
  }, []);

  useEffect(() => {
    const controller = new AbortController();

    if (selectedTeamNumber === null) {
      setTeamData(null);
      setTeamError(null);
      setTeamLoading(false);
      return () => controller.abort();
    }

    setTeamLoading(true);
    setTeamError(null);

    fetchTeamData(selectedTeamNumber, controller.signal)
      .then((data) => {
        setTeamData(data);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }

        setTeamError(
          error instanceof Error ? error.message : "Unable to load team data."
        );
        setTeamData(null);
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setTeamLoading(false);
        }
      });

    return () => controller.abort();
  }, [selectedTeamNumber]);

  useEffect(() => {
    const summary = teamSummaries.find(
      (team) => team.team_number === selectedTeamNumber
    );

    if (summary && !query.trim()) {
      setQuery(formatTeamLabel(summary));
    }
  }, [query, selectedTeamNumber, teamSummaries]);

  const filteredTeams = teamSummaries
    .filter((team) => {
      if (!deferredQuery.trim()) {
        return true;
      }

      const normalizedQuery = deferredQuery.toLowerCase();
      return (
        String(team.team_number).includes(normalizedQuery) ||
        (team.name || "").toLowerCase().includes(normalizedQuery) ||
        team.competitions.some((competition) =>
          competition.toLowerCase().includes(normalizedQuery)
        )
      );
    });

  const selectedSummary = teamSummaries.find(
    (team) => team.team_number === selectedTeamNumber
  );

  const theme = getTeamTheme(selectedTeamNumber ?? 3756);
  const matchBundles = teamData ? buildMatchBundles(teamData) : [];
  const averageAuto = teamData
    ? average(teamData.autonomous.map((record) => record.auto_fuel_scored))
    : null;
  const averageTeleop = teamData
    ? average(teamData.teleop.map((record) => record.teleop_fuel_scored))
    : null;
  const averageEfficiency = teamData
    ? average(teamData.postmatch.map((record) => record.scoring_efficiency))
    : null;
  const climbs = teamData
    ? teamData.endgame.filter((record) => record.climbed).length
    : 0;
  const reliabilityEvents = teamData
    ? teamData.endgame.filter(
        (record) => record.mechanical_issue || record.died || record.fell_over
      ).length
    : 0;
  const comments = teamData
    ? teamData.postmatch
        .filter((record) => record.comments && record.comments.trim())
        .map((record) => ({
          id: `${record.competition}-${record.match_number}`,
          label: `${record.competition.toUpperCase()} M${record.match_number}`,
          text: record.comments!.trim(),
        }))
    : [];
  const interviewTags = teamData
    ? [
        ...uniqueNonEmpty(
          teamData.interview.map((record) => record.drivetrain_type)
        ),
        ...uniqueNonEmpty(
          teamData.interview.map((record) => record.shooter_type)
        ),
        ...uniqueNonEmpty(
          teamData.interview.map((record) => record.climb_level)
        ),
      ].slice(0, 6)
    : [];
  const competitionList = selectedSummary?.competitions.length
    ? selectedSummary.competitions
    : uniqueNonEmpty(
        teamData
          ? [
              ...teamData.prematch.map((record) => record.competition),
              ...teamData.interview.map((record) => record.competition),
            ]
          : []
      );
  const hasTeamData = Boolean(
    teamData &&
      (teamData.prematch.length ||
        teamData.autonomous.length ||
        teamData.teleop.length ||
        teamData.endgame.length ||
        teamData.postmatch.length ||
        teamData.interview.length)
  );

  const selectTeam = (teamNumber: number, label?: string) => {
    if (label) {
      setQuery(label);
    }

    startTransition(() => {
      setSearchParams({ team: String(teamNumber) });
    });
  };

  const onLookup = () => {
    const parsed = parseTeamNumber(query);

    if (parsed === null) {
      setTeamError("Enter a valid team number to load a profile.");
      return;
    }

    const matchingSummary = teamSummaries.find(
      (team) => team.team_number === parsed
    );

    selectTeam(
      parsed,
      matchingSummary ? formatTeamLabel(matchingSummary) : `${parsed}`
    );
  };

  return (
    <main className="px-4 py-6 md:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 xl:grid xl:grid-cols-[340px_minmax(0,1fr)]">
        <aside className="space-y-5">
          <div className="space-y-2 pr-1">
            <section className="rounded-[28px] border border-zinc-800 bg-zinc-950/80 p-5">
              <div className="flex items-center gap-2">
                <Search className="h-4 w-4 text-zinc-400" />
                <h2 className="font-sports-ns text-xl uppercase tracking-[0.2em] text-zinc-100">
                  Team Lookup
                </h2>
              </div>

              <div className="mt-4 flex gap-2 scrollbar">
                <Input
                  type="text"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      event.preventDefault();
                      onLookup();
                    }
                  }}
                  placeholder="Enter team number"
                  className="h-11 rounded-xl border border-zinc-800 bg-zinc-900 px-4 text-zinc-50 placeholder:text-zinc-500"
                />
                <Button
                  type="button"
                  onClick={onLookup}
                  className="h-11 rounded-xl px-4"
                >
                  Load
                </Button>
              </div>

              {directoryError ? (
                <div className="mt-4 rounded-xl border border-red-950 bg-red-950/40 px-4 py-3 text-sm text-red-100">
                  {directoryError}
                </div>
              ) : null}

              <div className="mt-5 space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs uppercase tracking-[0.28em] text-zinc-500">
                    Available Teams
                  </h3>
                  {selectedTeamNumber !== null ? (
                    <button
                      type="button"
                      onClick={() => {
                        setQuery("");
                        startTransition(() => setSearchParams({}));
                      }}
                      className="text-xs uppercase tracking-[0.24em] text-zinc-500 transition-colors hover:text-zinc-200"
                    >
                      Clear
                    </button>
                  ) : null}
                </div>

                <div className="max-h-[28rem] space-y-2 overflow-y-auto pr-1">
                  {filteredTeams.map((team) => {
                    const isSelected = team.team_number === selectedTeamNumber;

                    return (
                      <button
                        key={team.team_number}
                        type="button"
                        onClick={() =>
                          selectTeam(team.team_number, formatTeamLabel(team))
                        }
                        className="w-full rounded-2xl border px-4 py-3 text-left transition-all duration-150"
                        style={{
                          borderColor: isSelected ? theme.primary : "#27272a",
                          backgroundColor: isSelected
                            ? `${theme.primary}18`
                            : "#09090b",
                        }}
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <div className="font-semibold text-zinc-100">
                              {formatTeamLabel(team)}
                            </div>
                            <div className="mt-1 text-xs uppercase tracking-[0.2em] text-zinc-500">
                              {team.competitions.length
                                ? team.competitions.join(" • ")
                                : "No competition tag"}
                            </div>
                          </div>
                          <div className="text-right text-xs text-zinc-400">
                            <div>{team.match_count} matches</div>
                            <div>{team.interview_count} interviews</div>
                          </div>
                        </div>
                      </button>
                    );
                  })}

                  {!directoryLoading && !filteredTeams.length ? (
                    <div className="rounded-2xl border border-dashed border-zinc-800 px-4 py-6 text-sm text-zinc-500">
                      No teams matched that search yet.
                    </div>
                  ) : null}
                </div>
              </div>
            </section>
          </div>
        </aside>

        <section className="min-w-0">
          {selectedTeamNumber === null ? (
            <div className="rounded-[32px] border border-dashed border-zinc-800 bg-zinc-950/70 px-8 py-12 text-center">
              <h2 className="mt-4 font-sports text-3xl uppercase tracking-[0.18em] text-zinc-100">
                Pick A Team
              </h2>
              <p className="mx-auto mt-3 max-w-xl text-sm leading-7 text-zinc-400">
                Enter a team number to view their profile and stats.
              </p>
            </div>
          ) : teamLoading ? (
            <div className="rounded-[32px] border border-zinc-800 bg-zinc-950/80 px-8 py-12 text-center text-zinc-300">
              Loading Team {selectedTeamNumber}…
            </div>
          ) : teamError ? (
            <div className="rounded-[32px] border border-red-950 bg-red-950/40 px-8 py-12 text-center text-red-100">
              {teamError}
            </div>
          ) : (
            <div className="space-y-6">
              <section
                className="relative overflow-hidden rounded-[32px] border p-6 md:p-8"
                style={{
                  background: theme.gradient,
                  borderColor: `${theme.primary}55`,
                  boxShadow: theme.shadow,
                }}
              >
                <div className="absolute -right-12 top-10 h-44 w-44 rounded-full bg-white/10 blur-3xl" />
                <div className="absolute bottom-0 right-0 h-28 w-80 bg-gradient-to-l from-white/10 to-transparent" />

                <div className="relative flex flex-col gap-6">
                  <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                    <div className="space-y-3">
                      <div>
                        <h2
                          className="font-sports text-5xl uppercase leading-none tracking-[0.12em]"
                          style={{ color: theme.text }}
                        >
                          Team {selectedTeamNumber}
                        </h2>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {competitionList.map((competition) => (
                          <Badge
                            key={competition}
                            className="border-0"
                            style={{
                              backgroundColor: `${theme.primary}cc`,
                              color: theme.text,
                            }}
                          >
                            {competition.toUpperCase()}
                          </Badge>
                        ))}
                        {!competitionList.length ? (
                          <Badge
                            variant="outline"
                            className="border-white/20 bg-white/5 text-white"
                          >
                            No event tag yet
                          </Badge>
                        ) : null}
                        {interviewTags.map((tag) => (
                          <Badge
                            key={tag}
                            variant="outline"
                            className="border-white/20 bg-white/5 text-white"
                          >
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div
                      className="max-w-md rounded-[28px] border px-5 py-4"
                      style={{
                        borderColor: `${theme.primary}40`,
                        backgroundColor: "rgba(255,255,255,0.06)",
                      }}
                    >
                      <div
                        className="flex items-center gap-2 text-sm"
                        style={{ color: theme.accent }}
                      >
                        Strategist Summary
                      </div>
                      <p
                        className="mt-3 text-sm leading-7"
                        style={{ color: theme.text }}
                      >
                        {hasTeamData
                          ? `Coverage spans ${
                              matchBundles.length
                            } matches with ${
                              comments.length
                            } written notes and ${
                              teamData?.interview.length || 0
                            } interview entries.`
                          : "No scouting entries recorded yet for this team."}
                      </p>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                    <ProfileMetric
                      label="Matches"
                      value={String(matchBundles.length)}
                      caption="Total matches scouted"
                      theme={theme}
                    />
                    <ProfileMetric
                      label="Auto Avg"
                      value={
                        averageAuto === null ? "—" : averageAuto.toFixed(1)
                      }
                      caption="Average auto score"
                      theme={theme}
                    />
                    <ProfileMetric
                      label="Teleop Avg"
                      value={
                        averageTeleop === null ? "—" : averageTeleop.toFixed(1)
                      }
                      caption="Average teleop score"
                      theme={theme}
                    />
                    <ProfileMetric
                      label="Climb Rate"
                      value={percent(climbs, teamData?.endgame.length || 0)}
                      caption={`${reliabilityEvents} reliability flags`}
                      theme={theme}
                    />
                  </div>
                </div>
              </section>

              <div className="grid gap-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,0.8fr)]">
                <section
                  className="rounded-[28px] border p-6"
                  style={{
                    borderColor: `${theme.primary}35`,
                    backgroundColor: theme.surface,
                  }}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <h3
                        className="font-sports-ns text-2xl uppercase tracking-[0.18em]"
                        style={{ color: theme.accent }}
                      >
                        Performance Snapshot
                      </h3>
                    </div>
                  </div>

                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    <div
                      className="rounded-2xl border p-4"
                      style={{
                        borderColor: `${theme.primary}35`,
                        backgroundColor: theme.surfaceAlt,
                      }}
                    >
                      <div
                        className="flex items-center gap-2 text-sm"
                        style={{ color: theme.accent }}
                      >
                        Scoring Profile
                      </div>
                      <div
                        className="mt-4 space-y-3 text-sm leading-6"
                        style={{ color: theme.text }}
                      >
                        <div className="flex items-center justify-between gap-4">
                          <span>Subjective Score</span>
                          <strong>
                            {averageEfficiency === null
                              ? "—"
                              : averageEfficiency.toFixed(1)}{" "}
                            / 5
                          </strong>
                        </div>
                        <div className="flex items-center justify-between gap-4">
                          <span>Defence Played Count</span>
                          <strong>
                            {teamData
                              ? teamData.postmatch.filter(
                                  (record) => (record.defense_skill || 0) > 0
                                ).length
                              : 0}
                          </strong>
                        </div>
                        <div className="flex items-center justify-between gap-4">
                          <span>Average Balls Passed</span>
                          <strong>
                            {teamData
                              ? (() => {
                                  const avg = average(
                                    teamData.teleop.map(
                                      (record) => record.fuel_fed_passed
                                    )
                                  );
                                  return avg === null ? "—" : avg.toFixed(1);
                                })()
                              : "—"}
                          </strong>
                        </div>
                      </div>
                    </div>

                    <div
                      className="rounded-2xl border p-4"
                      style={{
                        borderColor: `${theme.primary}35`,
                        backgroundColor: theme.surfaceAlt,
                      }}
                    >
                      <div
                        className="flex items-center gap-2 text-sm"
                        style={{ color: theme.accent }}
                      >
                        Reliability
                      </div>
                      <div
                        className="mt-4 space-y-3 text-sm leading-6"
                        style={{ color: theme.text }}
                      >
                        <div className="flex items-center justify-between gap-4">
                          <span>No-show reports</span>
                          <strong>
                            {teamData
                              ? teamData.prematch.filter(
                                  (record) => record.no_show
                                ).length
                              : 0}
                          </strong>
                        </div>
                        <div className="flex items-center justify-between gap-4">
                          <span>Mechanical issues</span>
                          <strong>
                            {teamData
                              ? teamData.endgame.filter(
                                  (record) => record.mechanical_issue
                                ).length
                              : 0}
                          </strong>
                        </div>
                        <div className="flex items-center justify-between gap-4">
                          <span>Knockdowns or deaths</span>
                          <strong>
                            {teamData
                              ? teamData.endgame.filter(
                                  (record) => record.died || record.fell_over
                                ).length
                              : 0}
                          </strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>

                <section
                  className="rounded-[28px] border p-6"
                  style={{
                    borderColor: `${theme.primary}35`,
                    backgroundColor: theme.surface,
                  }}
                >
                  <div className="flex items-center gap-2">
                    <h3
                      className="font-sports-ns text-2xl uppercase tracking-[0.18em]"
                      style={{ color: theme.accent }}
                    >
                      Notes Feed
                    </h3>
                  </div>

                  <div className="mt-5 space-y-3">
                    {comments.length ? (
                      comments.map((comment) => (
                        <article
                          key={comment.id}
                          className="rounded-2xl border p-4"
                          style={{
                            borderColor: `${theme.primary}35`,
                            backgroundColor: theme.surfaceAlt,
                          }}
                        >
                          <div
                            className="text-[11px] uppercase tracking-[0.24em]"
                            style={{ color: theme.mutedText }}
                          >
                            {comment.label}
                          </div>
                          <p
                            className="mt-2 text-sm leading-7"
                            style={{ color: theme.text }}
                          >
                            {comment.text}
                          </p>
                        </article>
                      ))
                    ) : (
                      <div
                        className="rounded-2xl border border-dashed p-4 text-sm"
                        style={{
                          borderColor: `${theme.primary}35`,
                          color: theme.mutedText,
                        }}
                      >
                        No written post-match notes yet.
                      </div>
                    )}
                  </div>
                </section>
              </div>

              <section
                className="rounded-[28px] border p-6"
                style={{
                  borderColor: `${theme.primary}35`,
                  backgroundColor: theme.surface,
                }}
              >
                <h3
                  className="font-sports-ns text-2xl uppercase tracking-[0.18em]"
                  style={{ color: theme.accent }}
                >
                  Interview Profile
                </h3>

                <div className="mt-5 space-y-4">
                  {teamData?.interview.length ? (
                    teamData.interview.map((interview) => (
                      <article
                        key={`${interview.competition}-${
                          interview.id || interview.team_number
                        }`}
                        className="rounded-2xl border p-5"
                        style={{
                          borderColor: `${theme.primary}35`,
                          backgroundColor: theme.surfaceAlt,
                        }}
                      >
                        <div className="mb-4 flex items-center justify-between gap-3">
                          <div
                            className="text-sm font-semibold"
                            style={{ color: theme.text }}
                          >
                            {interview.competition.toUpperCase()}
                          </div>
                          <Badge
                            variant="outline"
                            className="border-0"
                            style={{
                              backgroundColor: `${theme.primary}cc`,
                              color: theme.text,
                            }}
                          >
                            Team {interview.team_number}
                          </Badge>
                        </div>
                        <KeyValueGrid
                          data={interview}
                          fields={INTERVIEW_FIELDS}
                          theme={theme}
                        />
                      </article>
                    ))
                  ) : (
                    <div
                      className="rounded-2xl border border-dashed p-5 text-sm"
                      style={{
                        borderColor: `${theme.primary}35`,
                        color: theme.mutedText,
                      }}
                    >
                      No interview profile has been entered yet.
                    </div>
                  )}
                </div>
              </section>

              <section
                className="rounded-[28px] border p-6"
                style={{
                  borderColor: `${theme.primary}35`,
                  backgroundColor: theme.surface,
                }}
              >
                <h3
                  className="font-sports-ns text-2xl uppercase tracking-[0.18em]"
                  style={{ color: theme.accent }}
                >
                  Match Dossiers
                </h3>

                <div className="mt-5 space-y-5">
                  {matchBundles.length ? (
                    matchBundles.map((match) => (
                      <article
                        key={`${match.competition}-${match.matchNumber}`}
                        className="rounded-[28px] border p-5 md:p-6"
                        style={{
                          borderColor: `${theme.primary}35`,
                          backgroundColor: theme.surfaceAlt,
                        }}
                      >
                        <div className="mb-5 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                          <div>
                            <div
                              className="text-xs uppercase tracking-[0.28em]"
                              style={{ color: theme.mutedText }}
                            >
                              {match.competition.toUpperCase()}
                            </div>
                            <h4
                              className="mt-2 font-sports text-3xl uppercase tracking-[0.14em]"
                              style={{ color: theme.text }}
                            >
                              Match {match.matchNumber}
                            </h4>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {match.endgame?.climbed ? (
                              <Badge
                                className="border-0"
                                style={{
                                  backgroundColor: `${theme.primary}d9`,
                                  color: theme.text,
                                }}
                              >
                                Climbed
                              </Badge>
                            ) : null}
                            {match.endgame?.mechanical_issue ? (
                              <Badge variant="destructive">
                                Mechanical Issue
                              </Badge>
                            ) : null}
                            {match.teleop?.defended_by_opponent ? (
                              <Badge variant="secondary">Faced Defense</Badge>
                            ) : null}
                            {match.prematch?.no_show ? (
                              <Badge
                                variant="outline"
                                className="border-zinc-500 text-zinc-200"
                              >
                                No Show
                              </Badge>
                            ) : null}
                          </div>
                        </div>

                        <div className="space-y-6">
                          <MatchSection
                            title="Prematch"
                            data={match.prematch}
                            fields={PREMATCH_FIELDS}
                            theme={theme}
                          />
                          <MatchSection
                            title="Autonomous"
                            data={match.autonomous}
                            fields={AUTONOMOUS_FIELDS}
                            theme={theme}
                          />
                          <MatchSection
                            title="Teleop"
                            data={match.teleop}
                            fields={TELEOP_FIELDS}
                            theme={theme}
                          />
                          <MatchSection
                            title="Endgame"
                            data={match.endgame}
                            fields={ENDGAME_FIELDS}
                            theme={theme}
                          />
                          <MatchSection
                            title="Postmatch"
                            data={match.postmatch}
                            fields={POSTMATCH_FIELDS}
                            theme={theme}
                          />
                        </div>
                      </article>
                    ))
                  ) : (
                    <div
                      className="rounded-2xl border border-dashed p-5 text-sm"
                      style={{
                        borderColor: `${theme.primary}35`,
                        color: theme.mutedText,
                      }}
                    >
                      No match scouting data has been recorded for this team
                      yet.
                    </div>
                  )}
                </div>
              </section>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

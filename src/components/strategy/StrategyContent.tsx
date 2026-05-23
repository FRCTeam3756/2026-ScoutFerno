import { Badge } from "../../components/ui/badge";
import type { TeamAllData } from "../../types/strategy";
import { getTeamTheme } from "../../util/teamTheme";
import { MatchSection, PanelFrame, ProfileMetric, KeyValueGrid, SectionTitle } from "./StrategyShared";
import {
  buildVisibleFields,
  INTERVIEW_FIELD_ORDER,
  MATCH_FIELD_ORDER,
  percent,
  type StrategyMetrics,
} from "./utils";

type TeamTheme = ReturnType<typeof getTeamTheme>;

type StrategyContentProps = {
  selectedTeamNumber: number;
  teamLoading: boolean;
  teamError: string | null;
  teamData: TeamAllData | null;
  theme: TeamTheme;
  metrics: StrategyMetrics;
  competitionList: string[];
};

export function StrategyContent({
  selectedTeamNumber,
  teamLoading,
  teamError,
  teamData,
  theme,
  metrics,
  competitionList,
}: StrategyContentProps) {
  if (teamLoading) {
    return (
      <div className="rounded-[32px] border border-zinc-800 bg-zinc-950/80 px-8 py-12 text-center text-zinc-300">
        Loading Team {selectedTeamNumber}…
      </div>
    );
  }

  if (teamError) {
    return (
      <div className="rounded-[32px] border border-red-950 bg-red-950/40 px-8 py-12 text-center text-red-100">
        {teamError}
      </div>
    );
  }

  return (
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
                {metrics.interviewTags.map((tag) => (
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
                {metrics.hasTeamData
                  ? `Coverage spans ${
                      metrics.matchBundles.length
                    } matches with ${
                      metrics.comments.length
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
              value={String(metrics.matchBundles.length)}
              caption="Total matches scouted"
              theme={theme}
            />
            <ProfileMetric
              label="Auto Avg"
              value={
                metrics.averageAuto === null ? "—" : metrics.averageAuto.toFixed(1)
              }
              caption="Average auto score"
              theme={theme}
            />
            <ProfileMetric
              label="Teleop Avg"
              value={
                metrics.averageTeleop === null
                  ? "—"
                  : metrics.averageTeleop.toFixed(1)
              }
              caption="Average teleop score"
              theme={theme}
            />
            <ProfileMetric
              label="Climb Rate"
              value={percent(metrics.climbs, teamData?.match.length || 0)}
              caption={`${metrics.reliabilityEvents} reliability flags`}
              theme={theme}
            />
          </div>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,0.8fr)]">
        <PanelFrame theme={theme}>
          <div className="flex items-center justify-between gap-4">
            <div>
              <SectionTitle theme={theme}>Performance Snapshot</SectionTitle>
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
                    {metrics.averageEfficiency === null
                      ? "—"
                      : metrics.averageEfficiency.toFixed(1)}{" "}
                    / 5
                  </strong>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <span>Defence Played Count</span>
                  <strong>{metrics.defensePlayedCount}</strong>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <span>Average Balls Passed</span>
                  <strong>
                    {metrics.averagePassed === null
                      ? "—"
                      : metrics.averagePassed.toFixed(1)}
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
                  <strong>{metrics.noShowCount}</strong>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <span>Mechanical issues</span>
                  <strong>{metrics.mechanicalIssueCount}</strong>
                </div>
                <div className="flex items-center justify-between gap-4">
                  <span>Knockdowns or deaths</span>
                  <strong>{metrics.knockdownOrDeathCount}</strong>
                </div>
              </div>
            </div>
          </div>
        </PanelFrame>

        <PanelFrame theme={theme}>
          <div className="flex items-center gap-2">
            <SectionTitle theme={theme}>Notes Feed</SectionTitle>
          </div>

          <div className="mt-5 space-y-3">
            {metrics.comments.length ? (
              metrics.comments.map((comment) => (
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
        </PanelFrame>
      </div>

      <PanelFrame theme={theme}>
        <SectionTitle theme={theme}>Interview Profile</SectionTitle>

        <div className="mt-5 space-y-4">
          {teamData?.interview.length ? (
            teamData.interview.map((interview) => (
              <article
                key={`${interview.competition}-${interview.id || interview.team_number}`}
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
                  fields={buildVisibleFields(interview, INTERVIEW_FIELD_ORDER)}
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
      </PanelFrame>

      <PanelFrame theme={theme}>
        <SectionTitle theme={theme}>Match Dossiers</SectionTitle>

        <div className="mt-5 space-y-5">
          {metrics.matchBundles.length ? (
            metrics.matchBundles.map((match) => (
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
                    {match.match?.climbed ? (
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
                    {match.match?.mechanical_issue ? (
                      <Badge variant="destructive">Mechanical Issue</Badge>
                    ) : null}
                    {match.match?.defended_by_opponent ? (
                      <Badge variant="secondary">Faced Defense</Badge>
                    ) : null}
                    {match.match?.no_show ? (
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
                    data={match.match}
                    fields={
                      match.match
                        ? buildVisibleFields(match.match, MATCH_FIELD_ORDER)
                        : []
                    }
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
              No match scouting data has been recorded for this team yet.
            </div>
          )}
        </div>
      </PanelFrame>
    </div>
  );
}

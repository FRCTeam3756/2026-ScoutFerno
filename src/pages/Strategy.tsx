import { startTransition, useDeferredValue, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { StrategyContent } from "../components/strategy/StrategyContent";
import { StrategySidebar } from "../components/strategy/StrategySidebar";
import {
  buildCompetitionList,
  buildStrategyMetrics,
  formatTeamLabel,
  parseTeamNumber,
} from "../components/strategy/utils";
import type { TeamAllData, TeamSummary } from "../types/strategy";
import { fetchTeamData, fetchTeamSummaries } from "../util/strategy";
import { getTeamTheme } from "../util/teamTheme";

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
            : "Unable to load the team directory.",
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
          error instanceof Error ? error.message : "Unable to load team data.",
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
      (team) => team.team_number === selectedTeamNumber,
    );

    if (summary && !query.trim()) {
      setQuery(formatTeamLabel(summary));
    }
  }, [query, selectedTeamNumber, teamSummaries]);

  const filteredTeams = teamSummaries.filter((team) => {
    if (!deferredQuery.trim()) {
      return true;
    }

    const normalizedQuery = deferredQuery.toLowerCase();
    return (
      String(team.team_number).includes(normalizedQuery) ||
      (team.name || "").toLowerCase().includes(normalizedQuery) ||
      team.competitions.some((competition) =>
        competition.toLowerCase().includes(normalizedQuery),
      )
    );
  });

  const selectedSummary = teamSummaries.find(
    (team) => team.team_number === selectedTeamNumber,
  );

  const theme = getTeamTheme(
    selectedSummary
      ? {
          primary: selectedSummary.primary_color,
          secondary: selectedSummary.secondary_color,
        }
      : null,
  );
  const metrics = buildStrategyMetrics(teamData);
  const competitionList = buildCompetitionList(selectedSummary, teamData);

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
      (team) => team.team_number === parsed,
    );

    selectTeam(
      parsed,
      matchingSummary ? formatTeamLabel(matchingSummary) : `${parsed}`,
    );
  };

  return (
    <main className="px-4 py-6 md:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 xl:grid xl:grid-cols-[340px_minmax(0,1fr)]">
        <StrategySidebar
          query={query}
          onQueryChange={setQuery}
          onLookup={onLookup}
          directoryError={directoryError}
          directoryLoading={directoryLoading}
          filteredTeams={filteredTeams}
          selectedTeamNumber={selectedTeamNumber}
          onSelectTeam={selectTeam}
          onClearTeam={() => setSearchParams({})}
          theme={theme}
        />

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
          ) : (
            <StrategyContent
              selectedTeamNumber={selectedTeamNumber}
              teamLoading={teamLoading}
              teamError={teamError}
              teamData={teamData}
              theme={theme}
              metrics={metrics}
              competitionList={competitionList}
            />
          )}
        </section>
      </div>
    </main>
  );
}

import { startTransition } from "react";
import { Search } from "lucide-react";

import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import type { TeamSummary } from "../../types/strategy";
import { getTeamTheme } from "../../util/teamTheme";
import { formatTeamLabel } from "./utils";

type TeamTheme = ReturnType<typeof getTeamTheme>;

type StrategySidebarProps = {
  query: string;
  onQueryChange: (value: string) => void;
  onLookup: () => void;
  directoryError: string | null;
  directoryLoading: boolean;
  filteredTeams: TeamSummary[];
  selectedTeamNumber: number | null;
  onSelectTeam: (teamNumber: number, label?: string) => void;
  onClearTeam: () => void;
  theme: TeamTheme;
};

export function StrategySidebar({
  query,
  onQueryChange,
  onLookup,
  directoryError,
  directoryLoading,
  filteredTeams,
  selectedTeamNumber,
  onSelectTeam,
  onClearTeam,
  theme,
}: StrategySidebarProps) {
  return (
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
              onChange={(event) => onQueryChange(event.target.value)}
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
                    onQueryChange("");
                    startTransition(onClearTeam);
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
                      onSelectTeam(team.team_number, formatTeamLabel(team))
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
  );
}

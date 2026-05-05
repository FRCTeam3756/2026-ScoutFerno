import type { TeamAllData, TeamSummary } from "../types/strategy";
import { apiFetch } from "./api";

async function readApiError(response: Response) {
  try {
    const payload = (await response.json()) as { detail?: string };
    return payload.detail || `Request failed with status ${response.status}.`;
  } catch {
    return `Request failed with status ${response.status}.`;
  }
}

export async function fetchTeamSummaries(signal?: AbortSignal) {
  const response = await apiFetch("/match_data/all_teams", { signal });

  if (!response.ok) {
    throw new Error(await readApiError(response));
  }

  return (await response.json()) as TeamSummary[];
}

export async function fetchTeamData(teamNumber: number, signal?: AbortSignal) {
  const response = await apiFetch(`/match_data/team/${teamNumber}`, {
    signal,
  });

  if (!response.ok) {
    throw new Error(await readApiError(response));
  }

  return (await response.json()) as TeamAllData;
}

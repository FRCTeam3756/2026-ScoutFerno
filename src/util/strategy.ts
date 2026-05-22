import type { TeamAllData, TeamSummary } from "../types/strategy";
import { supabase } from "./supabase";

export async function fetchTeamSummaries(
  _?: AbortSignal,
): Promise<TeamSummary[]> {
  const [teamsRes, matchesRes, interviewsRes] = await Promise.all([
    supabase.from("teams").select("team_number, name, competitions"),
    supabase.from("matches").select("team_number"),
    supabase.from("interviews").select("team_number"),
  ]);

  if (teamsRes.error) throw new Error(teamsRes.error.message);
  if (matchesRes.error) throw new Error(matchesRes.error.message);
  if (interviewsRes.error) throw new Error(interviewsRes.error.message);

  const teams = teamsRes.data ?? [];
  const matches = matchesRes.data ?? [];
  const interviews = interviewsRes.data ?? [];

  const matchCountMap = new Map<number, number>();
  for (const m of matches) {
    matchCountMap.set(
      m.team_number,
      (matchCountMap.get(m.team_number) ?? 0) + 1,
    );
  }

  const interviewCountMap = new Map<number, number>();
  for (const i of interviews) {
    interviewCountMap.set(
      i.team_number,
      (interviewCountMap.get(i.team_number) ?? 0) + 1,
    );
  }

  return teams.map((team: any) => ({
    team_number: team.team_number,
    name: team.name,
    competitions: team.competitions || [],
    match_count: matchCountMap.get(team.team_number) ?? 0,
    interview_count: interviewCountMap.get(team.team_number) ?? 0,
  }));
}

export async function fetchTeamData(
  teamNumber: number,
  _?: AbortSignal,
): Promise<TeamAllData> {
  const [matchResponse, interviewResponse] = await Promise.all([
    supabase
      .from("matches")
      .select("*")
      .eq("team_number", teamNumber),
    supabase
      .from("interviews")
      .select("*")
      .eq("team_number", teamNumber),
  ]);

  if (matchResponse.error) {
    throw new Error(matchResponse.error.message);
  }

  if (interviewResponse.error) {
    throw new Error(interviewResponse.error.message);
  }

  return {
    match: matchResponse.data ?? [],
    interview: interviewResponse.data ?? [],
  };
}
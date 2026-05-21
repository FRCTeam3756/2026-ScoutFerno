import type { TeamAllData, TeamSummary } from "../types/strategy";
import { supabase } from "./supabase";

export async function fetchTeamSummaries(
  signal?: AbortSignal,
): Promise<TeamSummary[]> {
  let query = supabase
    .from("teams")
    .select(`
      team_number,
      name,
      competitions,
      matches:matches(count),
      interviews:interviews(count)
    `);

  if (signal) {
    query = query.abortSignal(signal);
  }

  const { data, error } = await query;

  if (error) {
    throw new Error(error.message);
  }

  return (data || []).map((team: any) => ({
    team_number: team.team_number,
    name: team.name,
    competitions: team.competitions || [],
    match_count: team.matches?.[0]?.count || 0,
    interview_count: team.interviews?.[0]?.count || 0,
  }));
}

export async function fetchTeamData(
  teamNumber: number,
  signal?: AbortSignal,
): Promise<TeamAllData> {
  let matchQuery = supabase.from("matches").select("*").eq("team_number", teamNumber);
  let interviewQuery = supabase
    .from("interview")
    .select("*")
    .eq("team_number", teamNumber);

  if (signal) {
    matchQuery = matchQuery.abortSignal(signal);
    interviewQuery = interviewQuery.abortSignal(signal);
  }

  const [matchResponse, interviewResponse] = await Promise.all([
    matchQuery,
    interviewQuery,
  ]);

  if (matchResponse.error) {
    throw new Error(matchResponse.error.message);
  }

  if (interviewResponse.error) {
    throw new Error(interviewResponse.error.message);
  }

  return {
    match: matchResponse.data || [],
    interview: interviewResponse.data || [],
  };
}

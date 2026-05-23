import type { MatchRecord } from "../../types/strategy";

export type MatchBundle = {
  competition: string;
  matchNumber: number;
  match?: MatchRecord;
};

export type KeyValueField<T extends object> = {
  key: keyof T;
  label: string;
};

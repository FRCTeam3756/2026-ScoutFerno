export interface TeamColorPair {
  primary: string;
  secondary: string;
  label?: string;
}

export const TEAM_COLORS_BY_NUMBER: Record<number, TeamColorPair> = {
  610: {
    primary: "#fff",
    secondary: "#005c09"
  },
  2200: {
    primary: "#fff",
    secondary: "#000000"
  },
  3756: {
    primary: "#ff7700",
    secondary: "#053270"
  },
};

export const DEFAULT_TEAM_COLORS: TeamColorPair = {
  primary: "#858585",
  secondary: "#585656"
}
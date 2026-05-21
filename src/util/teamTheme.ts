import {
  TEAM_COLORS_BY_NUMBER,
  DEFAULT_TEAM_COLORS,
  type TeamColorPair,
} from "../assets/teamColors";

export interface TeamTheme {
  primary: string;
  secondary: string;
  accent: string;
  accentStrong: string;
  surface: string;
  surfaceAlt: string;
  text: string;
  mutedText: string;
  ring: string;
  gradient: string;
  shadow: string;
}

type Rgb = {
  r: number;
  g: number;
  b: number;
};

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

function normalizeHex(hex: string) {
  const trimmed = hex.trim().replace(/^#/, "");

  if (trimmed.length === 3) {
    return trimmed
      .split("")
      .map((character) => `${character}${character}`)
      .join("")
      .toLowerCase();
  }

  if (trimmed.length === 6) {
    return trimmed.toLowerCase();
  }

  throw new Error(`Invalid hex color: ${hex}`);
}

function hexToRgb(hex: string): Rgb {
  const normalized = normalizeHex(hex);

  return {
    r: Number.parseInt(normalized.slice(0, 2), 16),
    g: Number.parseInt(normalized.slice(2, 4), 16),
    b: Number.parseInt(normalized.slice(4, 6), 16),
  };
}

function rgbToHex({ r, g, b }: Rgb) {
  return `#${[r, g, b]
    .map((channel) => clamp(Math.round(channel), 0, 255).toString(16).padStart(2, "0"))
    .join("")}`;
}

function mixColors(left: string, right: string, ratio: number) {
  const leftRgb = hexToRgb(left);
  const rightRgb = hexToRgb(right);
  const mixRatio = clamp(ratio, 0, 1);

  return rgbToHex({
    r: leftRgb.r + (rightRgb.r - leftRgb.r) * mixRatio,
    g: leftRgb.g + (rightRgb.g - leftRgb.g) * mixRatio,
    b: leftRgb.b + (rightRgb.b - leftRgb.b) * mixRatio,
  });
}

function withAlpha(hex: string, alpha: number) {
  const normalized = normalizeHex(hex);
  const alphaHex = clamp(Math.round(alpha * 255), 0, 255)
    .toString(16)
    .padStart(2, "0");

  return `#${normalized}${alphaHex}`;
}

function relativeLuminance(hex: string) {
  const { r, g, b } = hexToRgb(hex);

  const linearize = (channel: number) => {
    const normalized = channel / 255;
    return normalized <= 0.04045
      ? normalized / 12.92
      : ((normalized + 0.055) / 1.055) ** 2.4;
  };

  return (
    0.2126 * linearize(r) +
    0.7152 * linearize(g) +
    0.0722 * linearize(b)
  );
}

function pickTextColor(background: string) {
  return relativeLuminance(background) > 0.42 ? "#111827" : "#f8fafc";
}

function buildTheme(colorPair: TeamColorPair): TeamTheme {
  const primary = colorPair.primary;
  const secondary = colorPair.secondary;
  const accent = mixColors(primary, "#ffffff", 0.82);
  const accentStrong = mixColors(primary, "#ffffff", 0.45);
  const surface = mixColors(secondary, "#000000", 0.16);
  const surfaceAlt = mixColors(secondary, primary, 0.18);
  const text = pickTextColor(surface);
  const mutedText = mixColors(accentStrong, text, 0.2);
  const ring = mixColors(primary, "#ffffff", 0.18);
  const glowColor = hexToRgb(primary);

  return {
    primary,
    secondary,
    accent,
    accentStrong,
    surface,
    surfaceAlt,
    text,
    mutedText,
    ring,
    gradient: `radial-gradient(circle at top left, rgba(${glowColor.r}, ${glowColor.g}, ${glowColor.b}, 0.35), transparent 35%), linear-gradient(135deg, ${surface} 0%, ${surfaceAlt} 58%, ${mixColors(
      secondary,
      "#000000",
      0.35
    )} 100%)`,
    shadow: `0 28px 70px ${withAlpha(primary, 0.28)}`,
  };
}

export function getTeamTheme(teamNumber: number | null) {
  const configuredColors = (teamNumber == null) ? DEFAULT_TEAM_COLORS : (TEAM_COLORS_BY_NUMBER[teamNumber] || DEFAULT_TEAM_COLORS);

  return buildTheme(configuredColors);
}

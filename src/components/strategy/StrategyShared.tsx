import type { ReactNode } from "react";

import { getTeamTheme } from "../../util/teamTheme";
import type { KeyValueField } from "./types";
import { buildVisibleFields, formatValue } from "./utils";

type TeamTheme = ReturnType<typeof getTeamTheme>;

export function PanelFrame({
  children,
  theme,
}: {
  children: ReactNode;
  theme: TeamTheme;
}) {
  return (
    <section
      className="rounded-[28px] border p-6"
      style={{
        borderColor: `${theme.primary}35`,
        backgroundColor: theme.surface,
      }}
    >
      {children}
    </section>
  );
}

export function SectionTitle({
  children,
  theme,
}: {
  children: ReactNode;
  theme: TeamTheme;
}) {
  return (
    <h3
      className="font-sports-ns text-2xl uppercase tracking-[0.18em]"
      style={{ color: theme.accent }}
    >
      {children}
    </h3>
  );
}

export function ProfileMetric({
  label,
  value,
  caption,
  theme,
}: {
  label: string;
  value: string;
  caption: string;
  theme: TeamTheme;
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

export function KeyValueGrid<T extends object>({
  data,
  fields,
  theme,
}: {
  data: T;
  fields?: KeyValueField<T>[];
  theme: TeamTheme;
}) {
  const resolvedFields = fields ?? buildVisibleFields(data, []);

  return (
    <dl className="grid gap-3 sm:grid-cols-2">
      {resolvedFields.map((field) => (
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
              (data as Record<PropertyKey, unknown>)[field.key as PropertyKey],
            )}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function MatchSection<T extends object>({
  title,
  data,
  fields,
  theme,
}: {
  title: string;
  data?: T;
  fields: KeyValueField<T>[];
  theme: TeamTheme;
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

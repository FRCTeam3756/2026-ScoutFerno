import { NavLink } from "react-router-dom";
import { STORE_VERSION } from "../store/store";
import { useEffect, useState } from "react";

type ConnectionStatus = "checking" | "connected" | "disconnected";

function useBackendHealth(url: string, baseIntervalMs = 10000) {
  const [status, setStatus] = useState<ConnectionStatus>("checking");

  useEffect(() => {
    let cancelled = false;
    let interval = baseIntervalMs;

    const check = async () => {
      try {
        const res = await fetch(url, { signal: AbortSignal.timeout(5000) });

        if (cancelled) return;

        if (res.ok) {
          setStatus("connected");
          interval = baseIntervalMs;
        } else {
          setStatus("disconnected");
          interval = Math.min(interval * 2, 60000);
        }
      } catch {
        if (!cancelled) setStatus("disconnected");
      }
    };

    check();

    return () => {
      cancelled = true;
    };
  }, [url, baseIntervalMs]);

  return status;
}

const statusConfig: Record<
  ConnectionStatus,
  { label: string; dot: string; text: string }
> = {
  checking: {
    label: "Checking…",
    dot: "bg-zinc-500 animate-pulse",
    text: "text-zinc-500",
  },
  connected: {
    label: "Connected",
    dot: "bg-emerald-400 shadow-[0_0_6px_1px_#34d399]",
    text: "text-emerald-400",
  },
  disconnected: {
    label: "Disconnected",
    dot: "bg-red-500 shadow-[0_0_6px_1px_#ef4444]",
    text: "text-red-400",
  },
};

export function Header() {
  const status = useBackendHealth("https://api.ramferno.com/health");
  const { label, dot, text } = statusConfig[status];

  return (
    <header className="w-full bg-zinc-900 border-b border-zinc-700 px-8 py-0 flex items-stretch">
      <div className="flex items-center pr-8 border-r border-zinc-700 mr-6">
        <span className="text-white font-mono text-sm font-semibold tracking-widest uppercase">
          Scout<span className="text-orange-400">Ferno</span>
        </span>
      </div>

      <nav className="flex items-stretch gap-1 pt-2">
        {[
          { to: "/scouting", label: "Scouters" },
          { to: "/strategy", label: "Strategists" },
        ].map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              [
                "relative flex items-center px-4 text-sm font-medium tracking-wide transition-colors duration-150",
                "border-b-2",
                isActive
                  ? "text-white border-orange-400"
                  : "text-zinc-400 border-transparent hover:text-zinc-100 hover:border-zinc-500",
              ].join(" ")
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="ml-auto flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className={`inline-block w-2 h-2 rounded-full ${dot}`} />
          <span className={`font-mono text-xs tracking-wider ${text}`}>
            {label}
          </span>
        </div>

        <div className="w-px h-4 bg-zinc-700" />

        <span className="text-zinc-500 font-mono text-xs tracking-wider border border-zinc-700 rounded px-2 py-0.5">
          v{STORE_VERSION}
        </span>
      </div>
    </header>
  );
}

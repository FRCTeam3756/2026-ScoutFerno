import { NavLink, useNavigate } from "react-router-dom";
import { STORE_VERSION } from "../store/store";
import { useEffect, useState } from "react";
import { LogOut } from "lucide-react";

import { useAuth } from "./AuthProvider";
import { GoogleSignInButton } from "./GoogleSignInButton";
import { Modal } from "./core/Modal";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { buildApiUrl } from "../util/api";

type ConnectionStatus = "checking" | "connected" | "disconnected";

const NAV_ITEMS = [
  { to: "/scouting", label: "Scouters" },

  { to: "/strategy", label: "Strategists" },
] as const;

function useBackendHealth(url: string, baseIntervalMs = 10000) {
  const [status, setStatus] = useState<ConnectionStatus>("checking");

  useEffect(() => {
    let cancelled = false;
    let timeoutId: ReturnType<typeof setTimeout> | undefined;

    const check = async () => {
      let nextInterval = baseIntervalMs;

      try {
        const res = await fetch(url, { signal: AbortSignal.timeout(5000) });

        if (cancelled) return;

        if (res.ok) {
          setStatus("connected");
        } else {
          setStatus("disconnected");
          nextInterval = Math.min(baseIntervalMs * 2, 60000);
        }
      } catch {
        if (!cancelled) {
          setStatus("disconnected");
          nextInterval = Math.min(baseIntervalMs * 2, 60000);
        }
      } finally {
        if (!cancelled) {
          timeoutId = setTimeout(check, nextInterval);
        }
      }
    };

    void check();

    return () => {
      cancelled = true;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
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
  const navigate = useNavigate();
  const status = useBackendHealth(buildApiUrl("/api/health"));
  const { label, dot, text } = statusConfig[status];
  const {
    user,
    error,
    clearError,
    isLoading,
    isAuthenticating,
    signInWithGoogleCredential,
    signOut,
  } = useAuth();
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);
  const [pendingPath, setPendingPath] = useState<string | null>(null);

  const userInitial =
    user?.name
      ?.split(" ")
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "?";

  const handleProtectedNavigation = (to: string) => {
    if (user) {
      return;
    }

    setPendingPath(to);
    setShowLoginPrompt(true);
  };

  const handlePromptCredential = async (credential: string) => {
    await signInWithGoogleCredential(credential);

    setShowLoginPrompt(false);

    if (pendingPath) {
      navigate(pendingPath);
      setPendingPath(null);
    }
  };

  return (
    <>
      <header className="w-full border-b border-zinc-700 bg-zinc-900 px-4 py-3 md:px-8">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          <div className="flex items-center gap-6">
          <NavLink key={""} to={""} className="flex items-center">
            <span className="text-white font-mono text-sm font-semibold tracking-widest uppercase">
              Scout<span className="text-orange-400">Ferno</span>
            </span>
          </NavLink>

            <div className="hidden h-4 w-px self-center bg-zinc-700 md:block" />

            <nav className="flex items-stretch gap-1 pt-1 pb-1">
              {NAV_ITEMS.map(({ to, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  onClick={(event) => {
                    if (!user) {
                      event.preventDefault();
                      handleProtectedNavigation(to);
                    }
                  }}
                  className={({ isActive }) =>
                    [
                      "relative flex items-center px-3 md:px-4 text-sm font-medium tracking-wide transition-colors duration-150",
                      "border-b-2",
                      isActive && user
                        ? "text-white border-orange-400"
                        : "text-zinc-400 border-transparent hover:text-zinc-100 hover:border-zinc-500",
                    ].join(" ")
                  }
                >
                  {label}
                </NavLink>
              ))}
            </nav>
          </div>

          <div className="ml-auto flex flex-wrap items-center justify-end gap-3">
            {!isLoading && !user ? (
              <GoogleSignInButton
                disabled={isAuthenticating}
                onCredential={signInWithGoogleCredential}
              />
            ) : null}

            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <button
                    type="button"
                    className="flex items-center gap-3 rounded-full border border-zinc-700 bg-zinc-950/70 px-2 py-1 pr-3 text-left transition-colors hover:border-zinc-500"
                  >
                    {user.picture ? (
                      <img
                        src={user.picture}
                        alt={user.name}
                        className="h-9 w-9 rounded-full border border-zinc-700 object-cover"
                        referrerPolicy="no-referrer"
                      />
                    ) : (
                      <span className="flex h-9 w-9 items-center justify-center rounded-full border border-zinc-700 bg-zinc-800 text-xs font-semibold text-zinc-100">
                        {userInitial}
                      </span>
                    )}
                    <span className="hidden sm:flex sm:flex-col">
                      <span className="text-sm font-medium text-zinc-100">
                        {user.name}
                      </span>
                      <span className="font-mono text-[11px] text-zinc-400">
                        {user.email}
                      </span>
                    </span>
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  align="end"
                  className="w-72 border-zinc-700 bg-zinc-900 text-zinc-100"
                >
                  <DropdownMenuLabel className="space-y-1">
                    <div className="text-sm font-semibold text-zinc-100">
                      {user.name}
                    </div>
                    <div className="font-mono text-xs text-zinc-400">
                      {user.email}
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator className="bg-zinc-700" />
                  <DropdownMenuItem
                    onSelect={() => {
                      void signOut();
                    }}
                    className="cursor-pointer text-zinc-100 focus:bg-zinc-800 focus:text-zinc-100"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : null}

            <div className="flex items-center gap-2">
              <span className={`inline-block h-2 w-2 rounded-full ${dot}`} />
              <span className={`font-mono text-xs tracking-wider ${text}`}>
                {label}
              </span>
            </div>

            <div className="hidden h-4 w-px bg-zinc-700 md:block" />

            <span className="rounded border border-zinc-700 px-2 py-0.5 font-mono text-xs tracking-wider text-zinc-500">
              v{STORE_VERSION}
            </span>
          </div>
        </div>

        {error ? (
          <div className="mt-3 flex items-start justify-between gap-3 rounded-md border border-red-800 bg-red-950/70 px-4 py-3 text-sm text-red-100">
            <p>{error}</p>
            <button
              type="button"
              onClick={clearError}
              className="shrink-0 rounded border border-red-700 px-2 py-1 font-mono text-[11px] uppercase tracking-wide text-red-200 transition-colors hover:bg-red-900"
            >
              Dismiss
            </button>
          </div>
        ) : null}
      </header>

      <Modal
        show={showLoginPrompt}
        onDismiss={() => {
          setShowLoginPrompt(false);
          setPendingPath(null);
        }}
      >
        <div className="space-y-4 px-5 pb-5">
          <div className="space-y-2 text-center">
            <h2 className="font-rhr-ns text-3xl font-semibold tracking-wider text-primary">
              Sign In Required
            </h2>
            <p className="text-sm text-zinc-300">
              Sign in with Google to open
              {" "}
              <span className="font-mono text-zinc-100">
                {pendingPath || "this page"}
              </span>
              .
            </p>
          </div>

          {error ? (
            <p className="rounded border border-red-800 bg-red-950/60 px-3 py-2 text-sm text-red-200">
              {error}
            </p>
          ) : null}

          <div className="flex justify-center">
            <GoogleSignInButton
              disabled={isAuthenticating}
              onCredential={handlePromptCredential}
            />
          </div>
        </div>
      </Modal>
    </>
  );
}

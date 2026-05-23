import { NavLink, useNavigate } from "react-router-dom";
import { STORE_VERSION } from "../../store/store";
import { useState } from "react";
import { LogOut } from "lucide-react";

import { useAuth } from "../authentication/AuthProvider";
import { GoogleSignInButton } from "../authentication/GoogleSignInButton";
import { Modal } from "./Modal";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";

const NAV_ITEMS = [
  { to: "/scouting", label: "Scouters" },

  { to: "/strategy", label: "Strategists" },
] as const;

export function Header() {
  const navigate = useNavigate();
  const {
    user,
    error,
    clearError,
    isLoading,
    isAuthenticating,
    signInWithGoogle,
    signOut,
  } = useAuth();
  const [modalError, setModalError] = useState<string | null>(null);
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

  const handlePromptSignIn = async () => {
    setModalError(null);
    try {
      await signInWithGoogle();
      setShowLoginPrompt(false);
      if (pendingPath) {
        navigate(pendingPath);
        setPendingPath(null);
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Sign-in failed.";
      setModalError(`Couldn't sign you in: ${msg}`);
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
                onClick={signInWithGoogle}
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

            <span className="rounded border border-zinc-700 px-2 py-0.5 font-mono text-xs tracking-wider text-zinc-500">
              v{STORE_VERSION}
            </span>
          </div>
        </div>

        {error ? (
          <div className="mt-3 flex items-start justify-between gap-3 rounded-md border border-red-800 bg-red-950/70 px-4 py-3 text-sm text-red-100">
            <p>
              <span className="font-semibold">Auth error:</span> {error}
            </p>
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
          setModalError(null);
        }}
      >
        <div className="space-y-4 px-5 pb-5">
          <div className="space-y-2 text-center">
            <h2 className="font-rhr-ns text-3xl font-semibold tracking-wider text-primary">
              Sign In Required
            </h2>
            <p className="text-sm text-zinc-300">
              Continue with Google to open{" "}
              <span className="font-mono text-zinc-100">
                {pendingPath || "this page"}
              </span>
              .
            </p>
          </div>

          {modalError ? (
            <p className="...">
              <span className="font-semibold">Sign-in failed:</span>{" "}
              {modalError}
            </p>
          ) : null}

          <div className="flex justify-center">
            <GoogleSignInButton
              disabled={isAuthenticating}
              onClick={handlePromptSignIn}
            />
          </div>
        </div>
      </Modal>
    </>
  );
}

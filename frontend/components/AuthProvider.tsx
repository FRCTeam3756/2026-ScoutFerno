import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import type { AuthSessionResponse, AuthUser } from "../types/auth";
import { apiFetch } from "../util/api";

type AuthContextValue = {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticating: boolean;
  error: string | null;
  clearError: () => void;
  refreshSession: () => Promise<void>;
  signInWithGoogleCredential: (credential: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function getFriendlyAuthErrorMessage(message: string, status?: number) {
  const normalizedMessage = message.toLowerCase();

  if (status === 403 || normalizedMessage.includes("not authorized")) {
    return "This Google account is not authorized to access ScoutFerno. Sign in with an approved account or contact a team admin.";
  }

  if (
    status === 500 &&
    normalizedMessage.includes("allowlist is not configured")
  ) {
    return "ScoutFerno access has not been configured yet. Ask a team admin to set the allowed Google emails or domains.";
  }

  if (status === 401) {
    return "Google sign-in could not be verified. Please try again with your approved account.";
  }

  return message;
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong while contacting the backend.";
}

async function readSessionResponse(
  response: Response,
): Promise<AuthSessionResponse> {
  const payload = (await response.json()) as Partial<AuthSessionResponse> & {
    detail?: string;
  };

  if (!response.ok) {
    throw new Error(
      getFriendlyAuthErrorMessage(
        payload.detail || "Authentication request failed.",
        response.status,
      ),
    );
  }

  return {
    authenticated: Boolean(payload.authenticated),
    user: payload.user ?? null,
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshSession = async () => {
    try {
      const response = await apiFetch("/auth/session");
      const session = await readSessionResponse(response);
      setUser(session.user);
      setError(null);
    } catch (sessionError) {
      setUser(null);
      setError(getErrorMessage(sessionError));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void refreshSession();
  }, []);

  const signInWithGoogleCredential = async (credential: string) => {
    setIsAuthenticating(true);
    setError(null);

    try {
      const response = await apiFetch("/auth/google", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ credential }),
      });

      const session = await readSessionResponse(response);
      setUser(session.user);
      setError(null);
    } catch (authError) {
      setUser(null);
      setError(getErrorMessage(authError));
      throw authError;
    } finally {
      setIsAuthenticating(false);
    }
  };

  const signOut = async () => {
    setIsAuthenticating(true);
    setError(null);

    try {
      const response = await apiFetch("/auth/logout", {
        method: "POST",
      });

      await readSessionResponse(response);
      setUser(null);
      setError(null);
      window.google?.accounts.id.disableAutoSelect();
    } catch (authError) {
      setError(getErrorMessage(authError));
      throw authError;
    } finally {
      setIsAuthenticating(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticating,
        error,
        clearError: () => setError(null),
        refreshSession,
        signInWithGoogleCredential,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider.");
  }

  return context;
}

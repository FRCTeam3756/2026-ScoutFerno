import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { Session } from "@supabase/supabase-js";

import type { AuthUser } from "../../types/auth";
import { supabase } from "../../util/supabase";

type AuthContextValue = {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticating: boolean;
  error: string | null;
  clearError: () => void;
  refreshSession: () => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function getFriendlyAuthErrorMessage(message: string) {
  const normalizedMessage = message.toLowerCase();

  if (
    normalizedMessage.includes("provider is not enabled") ||
    normalizedMessage.includes("unsupported provider")
  ) {
    return "Google OAuth is not enabled in Supabase yet. Turn on the Google provider in your Supabase Auth settings.";
  }

  if (normalizedMessage.includes("popup")) {
    return "The Google sign-in window was blocked. Allow pop-ups for this site and try again.";
  }

  return message;
}

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return getFriendlyAuthErrorMessage(error.message);
  }

  return "Something went wrong while contacting Supabase.";
}

function mapSessionUser(session: Session | null): AuthUser | null {
  const supabaseUser = session?.user;
  if (!supabaseUser?.email) {
    return null;
  }

  const metadata = supabaseUser.user_metadata ?? {};
  const fullName =
    typeof metadata.full_name === "string" && metadata.full_name.trim()
      ? metadata.full_name
      : typeof metadata.name === "string" && metadata.name.trim()
        ? metadata.name
        : supabaseUser.email;

  return {
    email: supabaseUser.email,
    name: fullName,
    picture:
      typeof metadata.avatar_url === "string" ? metadata.avatar_url : null,
    first_name:
      typeof metadata.given_name === "string"
        ? metadata.given_name
        : typeof metadata.first_name === "string"
          ? metadata.first_name
          : fullName.split(" ")[0] || null,
    last_name:
      typeof metadata.family_name === "string"
        ? metadata.family_name
        : typeof metadata.last_name === "string"
          ? metadata.last_name
          : null,
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshSession = async () => {
    try {
      const { data, error: sessionError } = await supabase.auth.getSession();
      if (sessionError) {
        throw sessionError;
      }

      setUser(mapSessionUser(data.session));
      setError(null);
    } catch (sessionError) {
      setUser(null);
      setError(getErrorMessage(sessionError));
    } finally {
      setIsLoading(false);
      setIsAuthenticating(false);
    }
  };

  useEffect(() => {
    void refreshSession();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(mapSessionUser(session));
      setIsLoading(false);
      setIsAuthenticating(false);
      setError(null);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const signInWithGoogle = async () => {
    setIsAuthenticating(true);
    setError(null);

    try {
      const { error: signInError } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
          redirectTo: window.location.href,
          queryParams: {
            access_type: "offline",
            prompt: "select_account",
          },
        },
      });

      if (signInError) {
        throw signInError;
      }
    } catch (authError) {
      setIsAuthenticating(false);
      setError(getErrorMessage(authError));
      throw authError;
    }
  };

  const signOut = async () => {
    setIsAuthenticating(true);
    setError(null);

    try {
      const { error: signOutError } = await supabase.auth.signOut();
      if (signOutError) {
        throw signOutError;
      }

      setUser(null);
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
        signInWithGoogle,
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

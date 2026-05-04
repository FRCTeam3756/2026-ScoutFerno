import { useEffect, useRef, useState } from "react";

type GoogleSignInButtonProps = {
  disabled?: boolean;
  onCredential: (credential: string) => Promise<void> | void;
};

let googleScriptPromise: Promise<void> | null = null;

function loadGoogleScript() {
  if (googleScriptPromise) {
    return googleScriptPromise;
  }

  googleScriptPromise = new Promise((resolve, reject) => {
    const existingScript = document.querySelector<HTMLScriptElement>(
      'script[src="https://accounts.google.com/gsi/client"]'
    );

    if (existingScript) {
      existingScript.addEventListener("load", () => resolve(), { once: true });
      existingScript.addEventListener(
        "error",
        () => reject(new Error("Failed to load Google Sign-In.")),
        { once: true }
      );

      if (window.google) {
        resolve();
      }

      return;
    }

    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Google Sign-In."));
    document.head.appendChild(script);
  });

  return googleScriptPromise;
}

export function GoogleSignInButton({
  disabled = false,
  onCredential,
}: GoogleSignInButtonProps) {
  const buttonRef = useRef<HTMLDivElement | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  useEffect(() => {
    let cancelled = false;

    const initialize = async () => {
      if (!clientId) {
        setLoadError("Set Google Client ID to enable Google sign-in.");
        return;
      }

      try {
        await loadGoogleScript();

        if (cancelled || !buttonRef.current || !window.google) {
          return;
        }

        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: async (response) => {
            if (!response.credential) {
              return;
            }

            try {
              await onCredential(response.credential);
            } catch {
              // AuthProvider surfaces the message in-app.
            }
          },
        });

        buttonRef.current.innerHTML = "";
        window.google.accounts.id.renderButton(buttonRef.current, {
          theme: "filled_black",
          size: "medium",
          type: "standard",
          text: "signin_with",
          shape: "pill",
          width: 230,
        });
      } catch (error) {
        if (!cancelled) {
          setLoadError(
            error instanceof Error ? error.message : "Failed to load Google Sign-In."
          );
        }
      }
    };

    void initialize();

    return () => {
      cancelled = true;
    };
  }, [clientId, onCredential]);

  if (loadError) {
    return (
      <span className="text-xs text-amber-300 font-mono tracking-wide">
        {loadError}
      </span>
    );
  }

  return (
    <div className={disabled ? "pointer-events-none opacity-60" : undefined}>
      <div ref={buttonRef} />
    </div>
  );
}

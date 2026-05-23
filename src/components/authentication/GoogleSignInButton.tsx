type GoogleSignInButtonProps = {
  disabled?: boolean;
  onClick: () => Promise<void> | void;
};

export function GoogleSignInButton({
  disabled = false,
  onClick,
}: GoogleSignInButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => {
        void onClick();
      }}
      className={[
        "inline-flex min-h-11 items-center justify-center rounded-full border border-zinc-700 bg-white px-5 py-2.5 text-sm font-semibold text-zinc-950 transition-colors",
        "hover:bg-zinc-100 disabled:cursor-not-allowed disabled:opacity-60",
      ].join(" ")}
    >
      Continue with Google
    </button>
  );
}

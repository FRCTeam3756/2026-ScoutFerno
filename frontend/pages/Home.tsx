import { FloatingFormValue } from "../components/FloatingFormValue";

export function Home() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center px-4 text-center">
      <FloatingFormValue />
      <h1 className="pt-10 text-3xl font-sans">
        Welcome to ScoutFerno!
      </h1>
    </main>
  );
}
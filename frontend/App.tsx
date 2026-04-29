import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import { Scouting } from "./pages/Scouting";
import { Header } from "./components/Header";
import { ThemeProvider } from "./components/ThemeProvider";
import { Footer } from "./components/Footer";
import { Helmet } from "react-helmet";
import { Home } from "./pages/Home";
import { AuthProvider, useAuth } from "./components/AuthProvider";

function ProtectedRoute() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <main className="flex min-h-[50vh] items-center justify-center px-4">
        <div className="rounded border border-zinc-700 bg-zinc-900/70 px-4 py-3 font-mono text-sm text-zinc-300">
          Checking session...
        </div>
      </main>
    );
  }

  if (!user) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}

export const App = () => (
  <>
    <Helmet>
      <title>ScoutFerno</title>
      <link rel="icon" href="/favicon.ico" />
    </Helmet>

    <AuthProvider>
      <ThemeProvider>
        <div className="min-h-screen">
          <Header />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/scouting" element={<Scouting />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <Footer />
        </div>
      </ThemeProvider>
    </AuthProvider>
  </>
);

import { Route, Routes } from "react-router-dom";
import { Scouting } from "./pages/Scouting";
import { Header } from "./components/Header";
import { ThemeProvider } from "./components/ThemeProvider";
import { Footer } from "./components/Footer";
import { Helmet } from "react-helmet";
import { Home } from "./pages/Home";
import { AuthProvider } from "./components/AuthProvider";

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
            <Route path="/scouting" element={<Scouting />} />
          </Routes>
          <Footer />
        </div>
      </ThemeProvider>
    </AuthProvider>
  </>
);

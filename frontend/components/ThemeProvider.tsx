import { useScoutFernoState } from "../store/store";
import { setColorScheme } from "../util/theme";
import { useEffect } from "react";

type ThemeProviderProps = {
  children: React.ReactNode;
};

export function ThemeProvider({ children }: ThemeProviderProps) {
  const appTheme = useScoutFernoState((state) => state.formData.theme);

  useEffect(() => {
    if (!appTheme) {
      return;
    }

    setColorScheme(appTheme);
  }, [appTheme]);

  return <>{children}</>;
}

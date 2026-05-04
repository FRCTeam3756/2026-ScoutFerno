import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  base: "/",

  plugins: [
    react(),
    tsconfigPaths({
      projects: ["./tsconfig.json"],
    }),
    VitePWA({
      registerType: "autoUpdate",
      manifest: false,
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,json,woff,woff2}"],

        navigateFallback: "/index.html",
        directoryIndex: "index.html",
      },
    }),
  ],
});

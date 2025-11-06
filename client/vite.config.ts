import { defineConfig } from "vite";
import preact from "@preact/preset-vite";

// https://vite.dev/config/
export default defineConfig({
  base: "./",
  plugins: [preact()],
  build: {
    outDir: "../client_build",
    emptyOutDir: true,
    assetsInlineLimit: (filePath) =>
      filePath.endsWith(".svg") &&
      !filePath.includes("/bamboo/01") &&
      !filePath.includes("/flower/") &&
      !filePath.includes("/season/"),
    manifest: true,
    rollupOptions: {
      input: {
        main: "src/main.tsx",
        login: "src/login.tsx",
      },
    },
  },
  server: {
    strictPort: true,
  },
});

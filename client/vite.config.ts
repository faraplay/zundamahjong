import { defineConfig } from "vite";
import preact from "@preact/preset-vite";

// https://vite.dev/config/
export default defineConfig({
  base: "/zundamahjong/",
  plugins: [preact()],
  build: {
    outDir: "../client_build",
    emptyOutDir: true,
    assetsInlineLimit: (filePath) =>
      filePath.endsWith(".svg") &&
      !filePath.includes("/flower/") &&
      !filePath.includes("/season/"),
  },
  server: {
    proxy: {
      "/socket.io": {
        target: "http://localhost:5000",
        ws: true,
      },
    },
  },
});

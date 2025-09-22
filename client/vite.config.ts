import { defineConfig } from "vite";
import preact from "@preact/preset-vite";

// https://vite.dev/config/
export default defineConfig({
  base: "/zundamahjong/",
  plugins: [preact()],
  build: {
    outDir: "../client_build",
    emptyOutDir: true,
    minify: false,
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

import { defineConfig, loadEnv } from "vite";
import preact from "@preact/preset-vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const debug_server_port = env.DEBUG_SERVER_PORT
    ? Number(env.DEBUG_SERVER_PORT)
    : 5000;
  return {
    base: "./",
    plugins: [preact()],
    build: {
      outDir: "../client_build",
      emptyOutDir: true,
      assetsInlineLimit: (filePath) =>
        filePath.endsWith(".svg") &&
        !filePath.includes("/flower/") &&
        !filePath.includes("/season/"),
      rollupOptions: {
        input: {
          main: "index.html",
          login: "login/index.html",
        },
      },
    },
    server: {
      proxy: {
        "/socket.io": {
          target: `http://localhost:${debug_server_port}`,
          ws: true,
        },
      },
    },
  };
});

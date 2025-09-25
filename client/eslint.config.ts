import js from "@eslint/js";
import globals from "globals";
import preact from "eslint-config-preact";
import tseslint from "typescript-eslint";
import { defineConfig } from "eslint/config";
import eslintConfigPrettier from "eslint-config-prettier/flat";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts}"],
    plugins: { js },
    extends: ["js/recommended"],
    languageOptions: { globals: globals.browser },
  },
  ...preact,
  tseslint.configs.recommended,
  eslintConfigPrettier,
]);

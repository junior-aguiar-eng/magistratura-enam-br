import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { singleFileBuild } from "./src/single-file-build";

export default defineConfig({
  plugins: [react(), singleFileBuild()],
  test: { environment: "jsdom", setupFiles: "./src/test-setup.ts", globals: true, include: ["src/**/*.test.{ts,tsx}"] },
  build: { target: "es2022" },
});

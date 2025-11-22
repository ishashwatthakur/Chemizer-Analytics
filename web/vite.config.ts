import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path, { dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig(({ mode }) => {
  const isDev = mode === 'development';

  return {
    server: {
      host: "0.0.0.0",
      port: 5000,
      strictPort: true,
      hmr: {
        clientPort: 443,
      },
      // Proxy only in development
      ...(isDev && {
        proxy: {
          '/api': {
            target: process.env.VITE_API_URL || 'http://localhost:8000',
            changeOrigin: true,
          },
        },
      }),
    },
    plugins: [react()],
    build: {
      outDir: "dist",  // Simplified - Vercel expects 'dist' at root
      emptyOutDir: true,
      sourcemap: false,  // Disable for production
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
        
      },
    },
  };
});
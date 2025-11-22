import { createRoot } from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./App.tsx";
import "./index.css";

// Use Vite environment variable for the Google client ID.
// Create a `.env` with `VITE_GOOGLE_CLIENT_ID=...` or set the variable
// in your environment. Note: Vite env vars prefixed with VITE_ are exposed
// to the client bundle; do not put secrets there.
const clientId = (import.meta.env.VITE_GOOGLE_CLIENT_ID as string) ?? "";

if (!clientId) {
  // Inform developers during development if the client ID is not provided.
  // This avoids silent runtime issues in the Google OAuth provider.
  console.warn("VITE_GOOGLE_CLIENT_ID is not set. Google OAuth may not work.");
}

createRoot(document.getElementById("root")!).render(
  <GoogleOAuthProvider clientId={clientId}>
    <App />
  </GoogleOAuthProvider>
);

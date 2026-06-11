export const appConfig = {
  backendBaseUrl: import.meta.env.VITE_DELPHI_API_BASE_URL ?? "/api",
  environment: import.meta.env.VITE_DELPHI_ENVIRONMENT ?? "local"
} as const;

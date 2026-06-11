/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_DELPHI_API_BASE_URL?: string;
  readonly VITE_DELPHI_ENVIRONMENT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

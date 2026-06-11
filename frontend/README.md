# Delphi Frontend

React/Vite frontend for the Delphi internal data quality tool.

## Local Setup

```bash
npm install
npm run dev
```

The development server defaults to `http://localhost:5173`.

## Backend Configuration

The frontend reads backend and environment settings from `src/config.ts`.

```bash
VITE_DELPHI_API_BASE_URL=http://localhost:8000/api npm run dev
VITE_DELPHI_ENVIRONMENT=local npm run dev
```

If `VITE_DELPHI_API_BASE_URL` is not set, the app uses `/api`.

## Routes

- `#overview`
- `#datasets`
- `#datasets/orders`
- `#violations`

## Checks

```bash
npm run test
npm run build
```

The first shell implementation is static and intentionally focused on shared layout and design primitives. Later slices should wire the typed backend API layer into these surfaces.

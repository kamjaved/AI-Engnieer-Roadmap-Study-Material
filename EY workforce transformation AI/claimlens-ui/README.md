# ClaimLens UI (mock-data prototype)

The complete ClaimLens examiner prototype, split from the original single file into a standard Vite + React project.
All data is mock data. Nothing talks to a backend.

## Run
```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build into dist/
npm run lint     # oxlint
```
Requires Node.js 20.19+ or 22.12+.

## Structure
- `src/data/`        mock data only (users, reason codes, demo script, eval numbers, copilot prompts, one file per claim)
- `src/context/`     application state and action handlers (`ClaimLensProvider`), read with `useClaimLens()`
- `src/screens/`     one folder per screen: queue, submit, verify, detail, supervisor, dashboard (+ LoginScreen)
- `src/components/`  shared pieces (badges, header, nav tab, toast, banner, demo bar)
- `src/features/`    the Ask-ClaimLens copilot drawer
- `src/lib/`         pure helpers (queue filtering)
- `src/AppShell.jsx` maps the active screen name to its component

## Replacing the mock with a real backend
Start with `src/data/claims/index.js` (claims list) and the handlers in `src/context/ClaimLensProvider.jsx`.

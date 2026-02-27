# TODO - Connect Frontend with Backend

## Plan
- [x] Analyze the project structure and understand the issue
- [ ] Add proxy configuration to vite.config.ts to forward /api requests to backend
- [ ] Verify the configuration

## Current Status
Analyzed the project and identified that the frontend makes API calls to `/api/...` but there's no proxy configured to forward these requests to the Flask backend at localhost:5000.

INSIGHT — PS #17 FRONTEND

Frontend-only prototype for the Customer Intelligence / review intelligence problem statement.

FILES
- index.html
- css/style.css
- css/dashboard.css
- js/app.js

RUN
1. Extract this folder.
2. Open index.html directly, or right-click index.html in VS Code and choose "Open with Live Server".
3. Do NOT open the parent directory in the browser. Open index.html itself.

BACKEND HANDOFF
The UI currently uses demo data in js/app.js only so every interaction can be demonstrated.
A backend can later replace the dashboardData object/API calls without changing the UI flow.

INCLUDED UI
- Single shared workspace login (no duplicate role choices)
- Main dashboard
- Theme cards and theme detail
- Review evidence
- Filters drawer
- Emerging issue detection with tile cards
- Alert detail
- Trend comparison with current vs previous period
- Executive summary + Regenerate Summary
- Export Report modal
- PDF via browser print/save
- Excel-compatible .xls export
- Back navigation on secondary screens
- Logout

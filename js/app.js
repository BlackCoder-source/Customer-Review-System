/* =========================================================
   INSIGHT — APPLICATION
   ========================================================= */

"use strict";


/* =========================================================
   APPLICATION STATE
   ========================================================= */

const appState = {
    currentScreen: "login",
    selectedRole: null,

    filters: {
        product: "all",
        region: "all",
        dateRange: "30"
    },

    selectedTheme: null,
    selectedAlert: null
};


/* =========================================================
   SAMPLE APPLICATION DATA
   ========================================================= */

const dashboardData = {

    overview: {
        reviews: 1284,
        positive: 68,
        neutral: 19,
        negative: 13,
        emergingIssues: 4
    },

    themes: [
        {
            id: "delivery",
            name: "Delivery",
            complaints: 142,
            severity: "high",
            change: 34
        },

        {
            id: "pricing",
            name: "Pricing",
            complaints: 87,
            severity: "medium",
            change: 12
        },

        {
            id: "quality",
            name: "Product Quality",
            complaints: 64,
            severity: "medium",
            change: 8
        },

        {
            id: "support",
            name: "Customer Support",
            complaints: 42,
            severity: "low",
            change: -4
        }
    ],

    alerts: [
        {
            id: "delivery-delay",
            title: "Delivery delays",
            growth: 34,
            severity: "high",
            product: "Wireless Earbuds",
            region: "North Region",
            started: "6 days ago",
            reason:
                "Complaint frequency has increased significantly compared with the recent baseline.",
            action:
                "Investigate fulfilment delays affecting the North Region."
        },

        {
            id: "packaging",
            title: "Packaging damage",
            growth: 21,
            severity: "medium",
            product: "Electronics",
            region: "West Region",
            started: "9 days ago",
            reason:
                "Recent reviews show a growing pattern of damaged packaging during delivery.",
            action:
                "Review packaging and handling procedures for affected orders."
        },

        {
            id: "support-response",
            title: "Support response time",
            growth: 17,
            severity: "medium",
            product: "All Products",
            region: "South Region",
            started: "11 days ago",
            reason:
                "Customers are increasingly mentioning longer response times.",
            action:
                "Review support queue volume and response-time targets."
        },

        {
            id: "pricing",
            title: "Pricing complaints",
            growth: 9,
            severity: "low",
            product: "Smart Devices",
            region: "Central Region",
            started: "14 days ago",
            reason:
                "Pricing-related complaints have begun increasing gradually.",
            action:
                "Review recent pricing changes and customer feedback."
        }
    ],

    reviews: [
        {
            text:
                "My order took almost two weeks to arrive even though the estimated delivery date was much earlier.",
            sentiment: "Negative",
            theme: "Delivery",
            region: "North Region",
            product: "Wireless Earbuds"
        },

        {
            text:
                "The product arrived on time and the quality was exactly what I expected.",
            sentiment: "Positive",
            theme: "Product Quality",
            region: "West Region",
            product: "Electronics"
        },

        {
            text:
                "Customer support eventually solved my issue, but I had to wait several days for a response.",
            sentiment: "Negative",
            theme: "Customer Support",
            region: "South Region",
            product: "All Products"
        },

        {
            text:
                "The packaging was damaged when the package arrived, although the product itself was fine.",
            sentiment: "Negative",
            theme: "Delivery",
            region: "West Region",
            product: "Electronics"
        }
    ]
};


/* =========================================================
   APPLICATION INITIALIZATION
   ========================================================= */

function initializeApp() {

    console.log("Insight application initialized.");

    renderLoginScreen();
}


/* =========================================================
   LOGIN SCREEN
   ========================================================= */

function renderLoginScreen() {

    const app = document.getElementById("app");

    app.innerHTML = `
        <main class="login-screen">

            <section class="login-panel">

                <div class="brand-mark">
                    INSIGHT<span>/</span>
                </div>

                <div class="login-content">

                    <p class="eyebrow">
                        CUSTOMER INTELLIGENCE
                    </p>

                    <h1>
                        Understand what your
                        customers are saying.
                    </h1>

                    <p class="login-description">
                        Identify emerging issues, understand customer
                        sentiment, and investigate the evidence behind
                        every signal.
                    </p>

                    <form id="login-form">

                        <label>
                            Customer intelligence workspace
                        </label>

                        <button
                            type="submit"
                            class="btn btn-primary login-button"
                        >
                            Enter workspace
                        </button>

                    </form>

                </div>

                <p class="login-footer">
                    Customer intelligence workspace
                </p>

            </section>

            <section class="login-visual">

                <div class="visual-content">

                    <p class="eyebrow">
                        EARLY SIGNALS
                    </p>

                    <h2>
                        Find the problem
                        before it becomes one.
                    </h2>

                    <div class="signal-preview">

                        <div class="signal-header">
                            <span>Emerging issue</span>

                            <span class="badge badge-high">
                                HIGH
                            </span>
                        </div>

                        <h3>
                            Delivery delays
                        </h3>

                        <div class="signal-growth">
                            <strong>↑ 34%</strong>
                            <span>
                                complaint growth
                            </span>
                        </div>

                        <div class="signal-meta">
                            North Region
                            <span>•</span>
                            6 days ago
                        </div>

                    </div>

                </div>

            </section>

        </main>
    `;

    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", handleLogin);
}


/* =========================================================
   LOGIN HANDLER
   ========================================================= */

function handleLogin(event) {

    event.preventDefault();

    // One shared frontend workspace. Backend authentication/roles can be connected later.
    appState.selectedRole = "workspace";
    appState.currentScreen = "dashboard";

    renderDashboard();
}


/* =========================================================
   DASHBOARD SCREEN
   ========================================================= */

function renderDashboard() {

    const app = document.getElementById("app");

    app.innerHTML = `
        <div class="dashboard-layout">

            <aside class="sidebar">

                <div class="sidebar-brand">
                    INSIGHT<span>/</span>
                </div>

                <div class="workspace-label">
                    CUSTOMER INTELLIGENCE
                </div>

                <nav class="sidebar-nav">

                    <button
                        class="nav-item active"
                        data-screen="dashboard"
                    >
                        <span>01</span>
                        Overview
                    </button>

                    <button
                        class="nav-item"
                        data-screen="themes"
                    >
                        <span>02</span>
                        Themes
                    </button>

                    <button
                        class="nav-item"
                        data-screen="alerts"
                    >
                        <span>03</span>
                        Emerging Issues

                        <span class="nav-count">
                            04
                        </span>
                    </button>

                    <button
                        class="nav-item"
                        data-screen="evidence"
                    >
                        <span>04</span>
                        Evidence
                    </button>

                    <button
                        class="nav-item"
                        data-screen="trends"
                    >
                        <span>05</span>
                        Trends
                    </button>

                </nav>

                <div class="sidebar-bottom">

                    <button class="nav-item" data-screen="summary">
                        <span>06</span>
                        Reports
                    </button>

                    <button class="nav-item" id="logout-button">
                        <span>07</span>
                        Logout
                    </button>

                </div>

            </aside>


            <main class="dashboard-main">

                <header class="topbar">

                    <button
                        class="mobile-menu"
                        aria-label="Open navigation"
                    >
                        ☰
                    </button>

                    <div>
                        <p class="topbar-label">
                            CUSTOMER INTELLIGENCE
                        </p>

                        <h2>
                            Overview
                        </h2>
                    </div>

                    <div class="topbar-actions">

                        <button class="back-top-button" id="back-to-login" type="button">← Exit</button>

                        <button
                            class="icon-button"
                            aria-label="Notifications"
                        >
                            ♢
                        </button>

                        <div class="user-profile">
                            <div class="user-avatar">
                                ${getRoleInitial()}
                            </div>

                            <div>
                                <strong>
                                    ${getRoleName()}
                                </strong>

                                <span>
                                    Workspace
                                </span>
                            </div>
                        </div>

                    </div>

                </header>


                <section class="dashboard-content">

                    <div class="page-introduction">

                        <div>

                            <p class="eyebrow">
                                LAST 30 DAYS
                            </p>

                            <h1>
                                Here's what changed
                                in customer voice.
                            </h1>

                        </div>

                        <div class="page-actions">
                            <button
                                class="btn btn-secondary"
                                id="summary-button"
                            >
                                Executive Summary
                            </button>

                            <button
                                class="btn btn-secondary"
                                id="export-report-button"
                            >
                                Export Report
                            </button>

                            <button
                                class="btn btn-secondary"
                                id="filter-button"
                            >
                                Filters
                            </button>
                        </div>

                    </div>


                    <section class="metric-grid">

                        ${renderMetric(
                            "01",
                            dashboardData.overview.reviews.toLocaleString(),
                            "Customer reviews",
                            "Across all monitored feedback"
                        )}

                        ${renderMetric(
                            "02",
                            `${dashboardData.overview.positive}%`,
                            "Positive sentiment",
                            "Compared with previous period"
                        )}

                        ${renderMetric(
                            "03",
                            dashboardData.overview.emergingIssues,
                            "Emerging issues",
                            "Signals requiring attention"
                        )}

                    </section>


                    <section class="dashboard-grid">

                        <div class="section-block sentiment-section">

                            <div class="section-heading">

                                <div>
                                    <p class="eyebrow">
                                        SENTIMENT
                                    </p>

                                    <h2>
                                        Customer sentiment
                                    </h2>
                                </div>

                                <span class="section-period">
                                    Last 30 days
                                </span>

                            </div>

                            <div class="sentiment-chart">

                                <div class="chart-placeholder">

                                    <div class="chart-line">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>

                                </div>

                            </div>

                            <div class="sentiment-legend">

                                <div>
                                    <span class="legend-dot positive"></span>
                                    Positive
                                    <strong>68%</strong>
                                </div>

                                <div>
                                    <span class="legend-dot neutral"></span>
                                    Neutral
                                    <strong>19%</strong>
                                </div>

                                <div>
                                    <span class="legend-dot negative"></span>
                                    Negative
                                    <strong>13%</strong>
                                </div>

                            </div>

                        </div>


                        <div id="themes-section" class="section-block theme-section">

                            <div class="section-heading">

                                <div>
                                    <p class="eyebrow">
                                        THEMES
                                    </p>

                                    <h2>
                                        What's driving feedback
                                    </h2>
                                </div>

                            </div>

                            <div class="theme-list">

                                ${dashboardData.themes
                                    .map(renderThemeRow)
                                    .join("")}

                            </div>

                        </div>

                    </section>


                    <section class="alerts-section">

                        <div class="section-heading">

                            <div>

                                <p class="eyebrow">
                                    EARLY ISSUE DETECTION
                                </p>

                                <h2>
                                    Emerging signals
                                </h2>

                                <p class="section-description">
                                    Problems gaining momentum before
                                    they become widespread.
                                </p>

                            </div>

                            <button
                                class="btn btn-secondary"
                                id="view-alerts"
                            >
                                View all
                            </button>

                        </div>


                        <div class="alert-list">

                            ${dashboardData.alerts
                                .slice(0, 3)
                                .map(renderAlertRow)
                                .join("")}

                        </div>

                    </section>

                </section>

            </main>

        </div>
    `;

    attachDashboardEvents();
    attachDashboardExtras();
}


/* =========================================================
   EXECUTIVE SUMMARY + EXPORTS
   ========================================================= */

function attachDashboardExtras() {
    const summaryButton = document.getElementById("summary-button");
    if (summaryButton) summaryButton.addEventListener("click", () => renderSummaryScreen());

    const exportButton = document.getElementById("export-report-button");
    if (exportButton) exportButton.addEventListener("click", () => openExportPanel());

    const logout = document.getElementById("logout-button");
    if (logout) logout.addEventListener("click", () => {
        appState.selectedRole = null;
        appState.currentScreen = "login";
        renderLoginScreen();
    });
}

function getExecutiveSummary() {
    const high = dashboardData.alerts.filter(a => a.severity === "high").length;
    return {
        headline: "Customer sentiment remains broadly positive, with a small set of issues requiring attention.",
        points: [
            `${dashboardData.overview.reviews.toLocaleString()} customer reviews are represented in the current workspace.`,
            `${dashboardData.overview.positive}% of feedback is positive, while ${dashboardData.overview.negative}% is negative.`,
            `${dashboardData.overview.emergingIssues} emerging issues are currently being monitored, including ${high} high-severity signal${high === 1 ? "" : "s"}.`,
            `Delivery is the fastest-growing theme at ${dashboardData.themes[0].change}%, making it a key area for investigation.`
        ]
    };
}

function renderSummaryScreen(regenerated = false) {
    appState.currentScreen = "summary";
    const app = document.getElementById("app");
    const summary = getExecutiveSummary();
    const timestamp = new Date().toLocaleString();

    app.innerHTML = `
        <div class="dashboard-layout">
            <aside class="sidebar">
                <div class="sidebar-brand">INSIGHT<span>/</span></div>
                <div class="workspace-label">CUSTOMER INTELLIGENCE</div>
                <nav class="sidebar-nav">
                    <button class="nav-item" data-screen="dashboard"><span>01</span>Overview</button>
                    <button class="nav-item" data-screen="themes"><span>02</span>Themes</button>
                    <button class="nav-item" data-screen="alerts"><span>03</span>Emerging Issues <span class="nav-count">04</span></button>
                    <button class="nav-item" data-screen="evidence"><span>04</span>Evidence</button>
                    <button class="nav-item" data-screen="trends"><span>05</span>Trends</button>
                </nav>
                <div class="sidebar-bottom">
                    <button class="nav-item active" data-screen="summary"><span>06</span>Reports</button>
                    <button class="nav-item" id="logout-button"><span>07</span>Logout</button>
                </div>
            </aside>

            <main class="dashboard-main">
                <header class="topbar">
                    <div class="topbar-leading">
                        <button class="back-top-button" id="back-to-dashboard" type="button">← Back</button>
                        <button class="mobile-menu" aria-label="Open navigation">☰</button>
                        <div><p class="topbar-label">REPORTING</p><h2>Executive Summary</h2></div>
                    </div>
                    <div class="topbar-actions">
                        <div class="user-profile"><div class="user-avatar">${getRoleInitial()}</div><div><strong>${getRoleName()}</strong><span>Workspace</span></div></div>
                    </div>
                </header>

                <section class="dashboard-content">
                    <div class="page-introduction">
                        <div><p class="eyebrow">CUSTOMER VOICE · LAST 30 DAYS</p><h1>Executive summary</h1><p class="section-description">A concise view of the signals, sentiment, and issues visible in the current customer intelligence workspace.</p></div>
                        <div class="page-actions">
                            <button class="btn btn-secondary" id="regenerate-summary">Regenerate Summary</button>
                            <button class="btn btn-primary" id="summary-export">Export Report</button>
                        </div>
                    </div>

                    <section class="summary-hero card card-elevated">
                        <p class="eyebrow">${regenerated ? "REGENERATED SUMMARY" : "EXECUTIVE READOUT"}</p>
                        <h2>${summary.headline}</h2>
                        <span class="summary-timestamp">Generated ${timestamp}</span>
                    </section>

                    <section class="summary-grid">
                        ${summary.points.map((point, i) => `<article class="summary-card card"><span class="summary-number">0${i+1}</span><p>${point}</p></article>`).join("")}
                    </section>

                    <section class="section-block">
                        <div class="section-heading"><div><p class="eyebrow">PRIORITY SIGNALS</p><h2>Issues requiring investigation</h2></div><span class="section-period">${dashboardData.alerts.length} signals</span></div>
                        <div class="alert-list">${dashboardData.alerts.map(renderAlertRow).join("")}</div>
                    </section>
                </section>
            </main>
        </div>`;

    attachDetailNavigation();
    document.getElementById("back-to-dashboard")?.addEventListener("click", renderDashboard);
    document.getElementById("regenerate-summary")?.addEventListener("click", () => renderSummaryScreen(true));
    document.getElementById("summary-export")?.addEventListener("click", openExportPanel);
    document.getElementById("logout-button")?.addEventListener("click", () => { appState.selectedRole = null; renderLoginScreen(); });
}

function openExportPanel() {
    const old = document.getElementById("export-panel");
    if (old) { old.remove(); return; }
    const panel = document.createElement("div");
    panel.id = "export-panel";
    panel.innerHTML = `
        <div class="modal-backdrop" id="export-backdrop"></div>
        <section class="export-modal card">
            <div class="modal-header"><div><p class="eyebrow">REPORT EXPORT</p><h2>Export customer intelligence</h2></div><button class="filter-close" id="export-close" aria-label="Close">×</button></div>
            <p class="section-description">Choose a format. PDF uses your browser print dialog so it can be saved as a PDF. Excel exports the current report as an Excel-compatible workbook.</p>
            <div class="export-options">
                <button class="export-option" id="export-pdf"><strong>PDF</strong><span>Print / Save as PDF</span></button>
                <button class="export-option" id="export-excel"><strong>Excel</strong><span>Download .xls report</span></button>
            </div>
        </section>`;
    document.body.appendChild(panel);
    const close = () => panel.remove();
    document.getElementById("export-close").onclick = close;
    document.getElementById("export-backdrop").onclick = close;
    document.getElementById("export-pdf").onclick = () => { close(); window.print(); };
    document.getElementById("export-excel").onclick = () => { exportExcel(); close(); };
}

function exportExcel() {
    const rows = [
        ["Insight Customer Intelligence Report"],
        ["Metric", "Value"],
        ["Customer reviews", dashboardData.overview.reviews],
        ["Positive sentiment", `${dashboardData.overview.positive}%`],
        ["Neutral sentiment", `${dashboardData.overview.neutral}%`],
        ["Negative sentiment", `${dashboardData.overview.negative}%`],
        ["Emerging issues", dashboardData.overview.emergingIssues],
        [],
        ["Theme", "Complaints", "Change", "Severity"],
        ...dashboardData.themes.map(t => [t.name, t.complaints, `${t.change}%`, t.severity]),
        [],
        ["Emerging issue", "Growth", "Severity", "Product", "Region", "Started"],
        ...dashboardData.alerts.map(a => [a.title, `${a.growth}%`, a.severity, a.product, a.region, a.started])
    ];
    const xmlEscape = value => String(value ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    const table = `<html><head><meta charset="UTF-8"></head><body><table>${rows.map(row => `<tr>${row.map(cell => `<td>${xmlEscape(cell)}</td>`).join("")}</tr>`).join("")}</table></body></html>`;
    const blob = new Blob([table], {type:"application/vnd.ms-excel"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href=url; a.download="Insight_Customer_Intelligence_Report.xls"; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}


/* =========================================================
   METRIC COMPONENT
   ========================================================= */

function renderMetric(number, value, title, description) {

    return `
        <article class="metric-card">

            <span class="metric-number">
                ${number}
            </span>

            <strong class="metric-value">
                ${value}
            </strong>

            <span class="metric-title">
                ${title}
            </span>

            <p>
                ${description}
            </p>

        </article>
    `;
}


/* =========================================================
   THEME COMPONENT
   ========================================================= */

function renderThemeRow(theme) {

    const changeClass =
        theme.change >= 0
            ? "theme-change-up"
            : "theme-change-down";

    return `
        <button
            class="theme-row"
            data-theme="${theme.id}"
        >

            <div class="theme-name">

                <span class="theme-indicator"></span>

                <div>
                    <strong>
                        ${theme.name}
                    </strong>

                    <span>
                        ${theme.complaints} complaints
                    </span>
                </div>

            </div>

            <div class="theme-right">

                <span class="${changeClass}">
                    ${theme.change >= 0 ? "↑" : "↓"}
                    ${Math.abs(theme.change)}%
                </span>

                <span class="badge badge-${theme.severity}">
                    ${theme.severity.toUpperCase()}
                </span>

            </div>

        </button>
    `;
}


/* =========================================================
   ALERT COMPONENT
   ========================================================= */

function renderAlertRow(alert) {

    return `
        <button
            class="alert-row"
            data-alert="${alert.id}"
        >

            <div class="alert-main">

                <div class="alert-status">
                    <span class="alert-dot"></span>
                </div>

                <div>

                    <h3>
                        ${alert.title}
                    </h3>

                    <p>
                        ${alert.product}
                        <span>•</span>
                        ${alert.region}
                    </p>

                </div>

            </div>


            <div class="alert-growth">

                <strong>
                    ↑ ${alert.growth}%
                </strong>

                <span>
                    growth
                </span>

            </div>


            <span class="badge badge-${alert.severity}">
                ${alert.severity.toUpperCase()}
            </span>


            <span class="alert-arrow">
                →
            </span>

        </button>
    `;
}


/* =========================================================
   DASHBOARD EVENTS
   ========================================================= */

function attachDashboardEvents() {

    /* =========================================
       THEME ROWS
       ========================================= */

    const themeRows =
        document.querySelectorAll("[data-theme]");

    themeRows.forEach(row => {

        row.addEventListener("click", () => {

            const themeId = row.dataset.theme;

            const theme =
                dashboardData.themes.find(
                    item => item.id === themeId
                );

            if (!theme) {
                return;
            }

            appState.selectedTheme = theme;

            renderThemeDetail(theme);
        });
    });


    /* =========================================
       ALERT ROWS
       ========================================= */

    const alertRows =
        document.querySelectorAll("[data-alert]");

    alertRows.forEach(row => {

        row.addEventListener("click", () => {

            const alertId = row.dataset.alert;

            const alert =
                dashboardData.alerts.find(
                    item => item.id === alertId
                );

            if (!alert) {
                return;
            }

            appState.selectedAlert = alert;

            renderAlertDetail(alert);
        });
    });


    /* =========================================
       FILTER BUTTON
       ========================================= */

    const filterButton =
    document.getElementById("filter-button");
    if (filterButton) {
         filterButton.addEventListener(
            "click",
             openFilterPanel
             );
            }


    /* =========================================
       VIEW ALL ALERTS
       ========================================= */

    const viewAlerts =
        document.getElementById("view-alerts");

    if (viewAlerts) {

        viewAlerts.addEventListener("click", () => {

            renderAlertsScreen();

        });
    }


    /* =========================================
       SIDEBAR NAVIGATION
       ========================================= */

    const navItems =
        document.querySelectorAll(".sidebar-nav .nav-item");

    navItems.forEach(item => {

        item.addEventListener("click", () => {

            const screen =
                item.dataset.screen;

            if (!screen) {
                return;
            }

            switch (screen) {

                case "dashboard":
                    renderDashboard();
                    break;

                case "themes":
                    renderThemesScreen();
                    break;

                case "alerts":
                    renderAlertsScreen();
                    break;

                case "evidence":
                    renderEvidenceScreen();
                    break;

                case "trends":
                    renderTrendsScreen();
                    break;

                case "summary":
                    renderSummaryScreen();
                    break;

                default:
                    break;
            }
        });
    });
}


/* =========================================================
   THEME DETAIL SCREEN
   ========================================================= */

function renderThemeDetail(theme) {

    const app = document.getElementById("app");

    const relatedReviews =
        dashboardData.reviews.filter(
            review =>
                review.theme.toLowerCase() ===
                theme.name.toLowerCase()
        );

    app.innerHTML = `
        <div class="dashboard-layout">

            <aside class="sidebar">

                <div class="sidebar-brand">
                    INSIGHT<span>/</span>
                </div>

                <div class="workspace-label">
                    CUSTOMER INTELLIGENCE
                </div>

                <nav class="sidebar-nav">

                    <button
                        class="nav-item"
                        data-screen="dashboard"
                    >
                        <span>01</span>
                        Overview
                    </button>

                    <button
                        class="nav-item active"
                        data-screen="themes"
                    >
                        <span>02</span>
                        Themes
                    </button>

                    <button
                        class="nav-item"
                        data-screen="alerts"
                    >
                        <span>03</span>
                        Emerging Issues

                        <span class="nav-count">
                            04
                        </span>
                    </button>

                    <button
                        class="nav-item"
                        data-screen="evidence"
                    >
                        <span>04</span>
                        Evidence
                    </button>

                    <button
                        class="nav-item"
                        data-screen="trends"
                    >
                        <span>05</span>
                        Trends
                    </button>

                </nav>

                <div class="sidebar-bottom">

                    <button class="nav-item" data-screen="summary">
                        <span>06</span>
                        Reports
                    </button>

                    <button class="nav-item" id="logout-button">
                        <span>07</span>
                        Logout
                    </button>

                </div>

            </aside>


            <main class="dashboard-main">

                <header class="topbar">

                    <button
                        class="mobile-menu"
                        aria-label="Open navigation"
                    >
                        ☰
                    </button>

                    <div>

                        <p class="topbar-label">
                            CUSTOMER INTELLIGENCE
                        </p>

                        <h2>
                            Theme Detail
                        </h2>

                    </div>

                    <div class="topbar-actions">

                        <button
                            class="icon-button"
                            aria-label="Notifications"
                        >
                            ♢
                        </button>

                        <div class="user-profile">

                            <div class="user-avatar">
                                ${getRoleInitial()}
                            </div>

                            <div>
                                <strong>
                                    ${getRoleName()}
                                </strong>

                                <span>
                                    Workspace
                                </span>
                            </div>

                        </div>

                    </div>

                </header>


                <section class="dashboard-content">

                    <button
                        class="back-button"
                        id="back-to-dashboard"
                    >
                        ← Back to overview
                    </button>


                    <div class="detail-header">

                        <div>

                            <p class="eyebrow">
                                RECURRING THEME
                            </p>

                            <h1>
                                ${theme.name}
                            </h1>

                            <p class="detail-description">
                                Customer feedback associated with
                                this recurring theme.
                            </p>

                        </div>

                        <span class="badge badge-${theme.severity}">
                            ${theme.severity.toUpperCase()}
                        </span>

                    </div>


                    <section class="detail-metrics">

                        <div class="detail-metric">

                            <span>
                                COMPLAINTS
                            </span>

                            <strong>
                                ${theme.complaints}
                            </strong>

                        </div>


                        <div class="detail-metric">

                            <span>
                                CHANGE
                            </span>

                            <strong class="
                                ${
                                    theme.change >= 0
                                        ? "text-danger"
                                        : "text-success"
                                }
                            ">
                                ${theme.change >= 0 ? "↑" : "↓"}
                                ${Math.abs(theme.change)}%
                            </strong>

                        </div>


                        <div class="detail-metric">

                            <span>
                                SEVERITY
                            </span>

                            <strong>
                                ${theme.severity
                                    .charAt(0)
                                    .toUpperCase() +
                                theme.severity.slice(1)}
                            </strong>

                        </div>

                    </section>


                    <section class="evidence-preview">

                        <div class="section-heading">

                            <div>

                                <p class="eyebrow">
                                    REVIEW PREVIEW
                                </p>

                                <h2>
                                    What customers are saying
                                </h2>

                            </div>

                            <span class="section-period">
                                ${relatedReviews.length}
                                reviews available
                            </span>

                        </div>


                        <div class="review-preview-list">

                            ${
                                relatedReviews.length
                                    ? relatedReviews
                                        .slice(0, 3)
                                        .map(renderReviewPreview)
                                        .join("")
                                    : `
                                        <div class="empty-state">
                                            No review evidence available
                                            for this theme.
                                        </div>
                                    `
                            }

                        </div>


                        <div class="detail-action">

                            <button
                                class="btn btn-primary"
                                id="view-evidence"
                            >
                                View all evidence →
                            </button>

                        </div>

                    </section>

                </section>

            </main>

        </div>
    `;


    /* =========================================
       BACK TO DASHBOARD
       ========================================= */

    const backButton =
        document.getElementById("back-to-dashboard");

    if (backButton) {

        backButton.addEventListener(
            "click",
            () => {
                renderDashboard();
            }
        );
    }


    /* =========================================
       VIEW ALL EVIDENCE
       ========================================= */

    const evidenceButton =
        document.getElementById("view-evidence");

    if (evidenceButton) {

        evidenceButton.addEventListener(
            "click",
            () => {

                renderEvidenceScreen(theme);

            }
        );
    }


    attachDetailNavigation();
}


/* =========================================================
   REVIEW PREVIEW
   ========================================================= */

function renderReviewPreview(review) {

    const sentimentClass =
        review.sentiment.toLowerCase();

    return `
        <article class="review-preview">

            <div class="review-top">

                <span class="
                    review-sentiment
                    ${sentimentClass}
                ">
                    ${review.sentiment}
                </span>

                <span class="review-region">
                    ${review.region}
                </span>

            </div>

            <p>
                "${review.text}"
            </p>

        </article>
    `;
}
function renderThemesScreen() {

    renderDashboard();

    setTimeout(function () {

        const themesSection =
            document.getElementById("themes-section");

        if (themesSection) {

            themesSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

    }, 150);

}
function renderTrendsScreen() {
    appState.currentScreen = "trends";
    const app = document.getElementById("app");
    const period = appState.filters.dateRange || "30";

    app.innerHTML = `
        <div class="dashboard-layout">
            <aside class="sidebar">
                <div class="sidebar-brand">INSIGHT<span>/</span></div>
                <div class="workspace-label">CUSTOMER INTELLIGENCE</div>
                <nav class="sidebar-nav">
                    <button class="nav-item" data-screen="dashboard"><span>01</span>Overview</button>
                    <button class="nav-item" data-screen="themes"><span>02</span>Themes</button>
                    <button class="nav-item" data-screen="alerts"><span>03</span>Emerging Issues <span class="nav-count">04</span></button>
                    <button class="nav-item" data-screen="evidence"><span>04</span>Evidence</button>
                    <button class="nav-item active" data-screen="trends"><span>05</span>Trends</button>
                </nav>
                <div class="sidebar-bottom">
                    <button class="nav-item" data-screen="summary"><span>06</span>Reports</button>
                    <button class="nav-item" id="logout-button" type="button"><span>↪</span>Logout</button>
                </div>
            </aside>

            <main class="dashboard-main">
                <header class="topbar">
                    <div class="topbar-leading">
                        <button class="back-top-button" id="back-to-dashboard" type="button">← Back</button>
                        <div>
                            <p class="topbar-label">CUSTOMER INTELLIGENCE</p>
                            <h2>Trends</h2>
                        </div>
                    </div>
                    <div class="topbar-actions">
                        <button class="icon-button" aria-label="Notifications" type="button">♢</button>
                        <div class="user-profile"><div class="user-avatar">I</div><div><strong>Insight Workspace</strong><span>Workspace</span></div></div>
                    </div>
                </header>

                <section class="dashboard-content">
                    <div class="page-introduction">
                        <div>
                            <p class="eyebrow">TREND COMPARISON</p>
                            <h1>What's changing over time.</h1>
                            <p class="section-description">Compare the current period with the previous period to identify rising themes, improving issues, and sentiment movement.</p>
                        </div>
                        <div class="trend-control-card">
                            <label for="trend-period">Comparison period</label>
                            <select id="trend-period" class="select">
                                <option value="30" ${period === "30" ? "selected" : ""}>Last 30 days vs previous 30 days</option>
                                <option value="14" ${period === "14" ? "selected" : ""}>Last 14 days vs previous 14 days</option>
                                <option value="7" ${period === "7" ? "selected" : ""}>Last 7 days vs previous 7 days</option>
                            </select>
                        </div>
                    </div>

                    <section class="trend-summary-grid">
                        ${dashboardData.themes.map(theme => `
                            <article class="trend-summary-card">
                                <span>${theme.name}</span>
                                <strong class="${theme.change >= 0 ? "trend-up" : "trend-down"}">${theme.change >= 0 ? "+" : ""}${theme.change}%</strong>
                                <small>Complaint volume</small>
                            </article>
                        `).join("")}
                    </section>

                    <section class="trend-panel">
                        <div class="section-heading">
                            <div><p class="eyebrow">THEME MOVEMENT</p><h2>Current vs previous period</h2></div>
                            <span class="section-period">Last ${period} days</span>
                        </div>
                        <div class="trend-table">
                            <div class="trend-row trend-header"><span>Theme</span><span>Previous</span><span>Current</span><span>Change</span></div>
                            ${dashboardData.themes.map(theme => {
                                const previous = Math.max(1, Math.round(theme.complaints / (1 + theme.change / 100)));
                                return `<div class="trend-row"><span class="trend-theme">${theme.name}</span><span>${previous}</span><span>${theme.complaints}</span><span class="${theme.change >= 0 ? "trend-up" : "trend-down"}">${theme.change >= 0 ? "+" : ""}${theme.change}%</span></div>`;
                            }).join("")}
                        </div>
                    </section>

                    <section class="trend-panel">
                        <div class="section-heading">
                            <div><p class="eyebrow">SENTIMENT MOVEMENT</p><h2>Current sentiment split</h2></div>
                            <span class="section-period">Current period</span>
                        </div>
                        <div class="sentiment-trend-grid">
                            <article class="sentiment-trend-item"><span>Positive</span><strong>${dashboardData.overview.positive}%</strong><div class="trend-meter"><span style="width:${dashboardData.overview.positive}%"></span></div></article>
                            <article class="sentiment-trend-item"><span>Neutral</span><strong>${dashboardData.overview.neutral}%</strong><div class="trend-meter neutral-meter"><span style="width:${dashboardData.overview.neutral}%"></span></div></article>
                            <article class="sentiment-trend-item"><span>Negative</span><strong>${dashboardData.overview.negative}%</strong><div class="trend-meter negative-meter"><span style="width:${dashboardData.overview.negative}%"></span></div></article>
                        </div>
                    </section>

                    <section class="trend-panel trend-insight-panel">
                        <p class="eyebrow">READ THE CHANGE</p>
                        <h2>Delivery is the fastest-growing theme.</h2>
                        <p>Use the theme movement table and sentiment split to identify where customer feedback is changing most quickly. Backend trend calculations can replace these demo values later.</p>
                    </section>
                </section>
            </main>
        </div>`;

    document.getElementById("back-to-dashboard")?.addEventListener("click", renderDashboard);
    document.getElementById("trend-period")?.addEventListener("change", event => {
        appState.filters.dateRange = event.target.value;
        renderTrendsScreen();
    });
    attachDetailNavigation();
}

/* =========================================================
   DETAIL PAGE NAVIGATION
   ========================================================= */

function attachDetailNavigation() {

    const navItems = document.querySelectorAll(
        ".sidebar-nav .nav-item"
    );

    navItems.forEach(item => {

        item.addEventListener("click", () => {

            const screen = item.dataset.screen;

            switch (screen) {

                case "dashboard":
                    renderDashboard();
                    break;

                case "themes":
                    renderThemesScreen();
                    break;

                case "alerts":
                    renderAlertsScreen();
                    break;

                case "evidence":
                    renderEvidenceScreen();
                    break;

                case "trends":
                    renderTrendsScreen();
                    break;

                case "summary":
                    renderSummaryScreen();
                    break;

            }

        });

    });

}


/* =========================================================
   REAL REVIEW EVIDENCE SCREEN
   ========================================================= */

function renderEvidenceScreen(theme = appState.selectedTheme) {

    const app = document.getElementById("app");

    /*
     * If the user reaches Evidence from the sidebar
     * without first selecting a theme, show all reviews.
     */

    const reviews = theme
        ? dashboardData.reviews.filter(
            review =>
                review.theme.toLowerCase() ===
                theme.name.toLowerCase()
        )
        : dashboardData.reviews;


    const pageTitle = theme
        ? `${theme.name} evidence`
        : "Review evidence";


    app.innerHTML = `
        <div class="dashboard-layout">

            <aside class="sidebar">

                <div class="sidebar-brand">
                    INSIGHT<span>/</span>
                </div>

                <div class="workspace-label">
                    CUSTOMER INTELLIGENCE
                </div>

                <nav class="sidebar-nav">

                    <button
                        class="nav-item"
                        data-screen="dashboard"
                    >
                        <span>01</span>
                        Overview
                    </button>

                    <button
                        class="nav-item"
                        data-screen="themes"
                    >
                        <span>02</span>
                        Themes
                    </button>

                    <button
                        class="nav-item"
                        data-screen="alerts"
                    >
                        <span>03</span>
                        Emerging Issues

                        <span class="nav-count">
                            04
                        </span>
                    </button>

                    <button
                        class="nav-item active"
                        data-screen="evidence"
                    >
                        <span>04</span>
                        Evidence
                    </button>

                    <button
                        class="nav-item"
                        data-screen="trends"
                    >
                        <span>05</span>
                        Trends
                    </button>

                </nav>

                <div class="sidebar-bottom">

                    <button class="nav-item" data-screen="summary">
                        <span>06</span>
                        Reports
                    </button>

                    <button class="nav-item" id="logout-button">
                        <span>07</span>
                        Logout
                    </button>

                </div>

            </aside>


            <main class="dashboard-main">

                <header class="topbar">

                    <button
                        class="mobile-menu"
                        aria-label="Open navigation"
                    >
                        ☰
                    </button>

                    <div>

                        <p class="topbar-label">
                            CUSTOMER INTELLIGENCE
                        </p>

                        <h2>
                            Evidence
                        </h2>

                    </div>

                    <div class="topbar-actions">

                        <button
                            class="icon-button"
                            aria-label="Notifications"
                        >
                            ♢
                        </button>

                        <div class="user-profile">

                            <div class="user-avatar">
                                ${getRoleInitial()}
                            </div>

                            <div>

                                <strong>
                                    ${getRoleName()}
                                </strong>

                                <span>
                                    Workspace
                                </span>

                            </div>

                        </div>

                    </div>

                </header>


                <section class="dashboard-content">

                    <button
                        class="back-button"
                        id="back-from-evidence"
                    >
                        ← Back
                    </button>


                    <div class="page-introduction evidence-introduction">

                        <div>

                            <p class="eyebrow">
                                REAL REVIEW EVIDENCE
                            </p>

                            <h1>
                                ${pageTitle}
                            </h1>

                            <p class="detail-description">
                                The customer feedback behind this
                                insight.
                            </p>

                        </div>

                        <div class="evidence-count">

                            <strong>
                                ${reviews.length}
                            </strong>

                            <span>
                                reviews
                            </span>

                        </div>

                    </div>


                    <section class="evidence-toolbar">

                        <div>

                            <span class="toolbar-label">
                                FILTER
                            </span>

                            <button
                                class="evidence-filter active"
                                data-sentiment="all"
                            >
                                All
                            </button>

                            <button
                                class="evidence-filter"
                                data-sentiment="Positive"
                            >
                                Positive
                            </button>

                            <button
                                class="evidence-filter"
                                data-sentiment="Neutral"
                            >
                                Neutral
                            </button>

                            <button
                                class="evidence-filter"
                                data-sentiment="Negative"
                            >
                                Negative
                            </button>

                        </div>

                    </section>


                    <section
                        class="evidence-list"
                        id="evidence-list"
                    >

                        ${
                            reviews.length
                                ? reviews
                                    .map(
                                        (review, index) =>
                                            renderFullReview(
                                                review,
                                                index
                                            )
                                    )
                                    .join("")
                                : `
                                    <div class="empty-state">
                                        No review evidence available.
                                    </div>
                                `
                        }

                    </section>

                </section>

            </main>

        </div>
    `;


    /* =========================================
       BACK BUTTON
       ========================================= */

    const backButton =
        document.getElementById(
            "back-from-evidence"
        );

    if (backButton) {

        backButton.addEventListener(
            "click",
            () => {

                if (theme) {
                    renderThemeDetail(theme);
                } else {
                    renderDashboard();
                }

            }
        );
    }


    /* =========================================
       SENTIMENT FILTERS
       ========================================= */

    const filterButtons =
        document.querySelectorAll(
            ".evidence-filter"
        );

    filterButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const sentiment =
                    button.dataset.sentiment;

                filterButtons.forEach(
                    item =>
                        item.classList.remove("active")
                );

                button.classList.add("active");


                const filteredReviews =
                    sentiment === "all"
                        ? reviews
                        : reviews.filter(
                            review =>
                                review.sentiment ===
                                sentiment
                        );


                const evidenceList =
                    document.getElementById(
                        "evidence-list"
                    );


                evidenceList.innerHTML =
                    filteredReviews.length
                        ? filteredReviews
                            .map(
                                (review, index) =>
                                    renderFullReview(
                                        review,
                                        index
                                    )
                            )
                            .join("")
                        : `
                            <div class="empty-state">
                                No ${sentiment.toLowerCase()}
                                reviews found.
                            </div>
                        `;
            }
        );
    });


    attachDetailNavigation();
}


/* =========================================================
   FULL REVIEW COMPONENT
   ========================================================= */

function renderFullReview(review, index) {

    const sentimentClass =
        review.sentiment.toLowerCase();

    return `
        <article class="full-review">

            <div class="review-index">
                ${String(index + 1).padStart(2, "0")}
            </div>


            <div class="full-review-content">

                <div class="full-review-header">

                    <span
                        class="
                            review-sentiment
                            ${sentimentClass}
                        "
                    >
                        ${review.sentiment}
                    </span>

                    <span class="review-theme">
                        ${review.theme}
                    </span>

                    <span class="review-region">
                        ${review.region}
                    </span>

                </div>


                <p class="full-review-text">
                    "${review.text}"
                </p>


                <div class="review-context">

                    <span>
                        Customer feedback
                    </span>

                    <span>
                        •
                    </span>

                    <span>
                        ${review.region}
                    </span>

                </div>

            </div>

        </article>
    `;
}



/* =========================================================
   EARLY ISSUE DETECTION — ALERTS SCREEN
   ========================================================= */

function renderAlertsScreen() {

    const app = document.getElementById("app");

    app.innerHTML = `
        <div class="dashboard-layout">

            <aside class="sidebar">

                <div class="sidebar-brand">
                    INSIGHT<span>/</span>
                </div>

                <div class="workspace-label">
                    CUSTOMER INTELLIGENCE
                </div>

                <nav class="sidebar-nav">

                    <button
                        class="nav-item"
                        data-screen="dashboard"
                    >
                        <span>01</span>
                        Overview
                    </button>

                    <button
                        class="nav-item"
                        data-screen="themes"
                    >
                        <span>02</span>
                        Themes
                    </button>

                    <button
                        class="nav-item active"
                        data-screen="alerts"
                    >
                        <span>03</span>
                        Emerging Issues

                        <span class="nav-count">
                            ${dashboardData.alerts.length
                                .toString()
                                .padStart(2, "0")}
                        </span>
                    </button>

                    <button
                        class="nav-item"
                        data-screen="evidence"
                    >
                        <span>04</span>
                        Evidence
                    </button>

                    <button
                        class="nav-item"
                        data-screen="trends"
                    >
                        <span>05</span>
                        Trends
                    </button>

                </nav>

                <div class="sidebar-bottom">

                    <button class="nav-item" data-screen="summary">
                        <span>06</span>
                        Reports
                    </button>

                    <button class="nav-item" id="logout-button">
                        <span>07</span>
                        Logout
                    </button>

                </div>

            </aside>


            <main class="dashboard-main">

                <header class="topbar">

                    <button
                        class="mobile-menu"
                        aria-label="Open navigation"
                    >
                        ☰
                    </button>

                    <div class="topbar-leading">

                        <button class="back-top-button" id="back-to-dashboard" type="button">← Back</button>

                        <div>
                            <p class="topbar-label">
                                CUSTOMER INTELLIGENCE
                            </p>

                        <h2>
                            Emerging Issues
                        </h2>

                        </div>
                    </div>


                    <div class="topbar-actions">

                        <button
                            class="icon-button"
                            aria-label="Notifications"
                        >
                            ♢
                        </button>

                        <div class="user-profile">

                            <div class="user-avatar">
                                ${getRoleInitial()}
                            </div>

                            <div>

                                <strong>
                                    ${getRoleName()}
                                </strong>

                                <span>
                                    Workspace
                                </span>

                            </div>

                        </div>

                    </div>

                </header>


                <section class="dashboard-content">

                    <button
                        class="back-button"
                        id="back-from-alerts"
                    >
                        ← Back to overview
                    </button>


                    <div class="page-introduction alerts-introduction">

                        <div>

                            <p class="eyebrow">
                                EARLY ISSUE DETECTION
                            </p>

                            <h1>
                                Problems gaining momentum.
                            </h1>

                            <p class="detail-description">
                                Emerging customer issues identified
                                from changes in complaint patterns.
                            </p>

                        </div>


                        <div class="alert-summary">

                            <strong>
                                ${dashboardData.alerts.length}
                            </strong>

                            <span>
                                active signals
                            </span>

                        </div>

                    </div>


                    <section class="alert-overview-strip">

                        <div>

                            <span>
                                HIGH PRIORITY
                            </span>

                            <strong>
                                ${
                                    dashboardData.alerts.filter(
                                        alert =>
                                            alert.severity === "high"
                                    ).length
                                }
                            </strong>

                        </div>


                        <div>

                            <span>
                                MEDIUM PRIORITY
                            </span>

                            <strong>
                                ${
                                    dashboardData.alerts.filter(
                                        alert =>
                                            alert.severity === "medium"
                                    ).length
                                }
                            </strong>

                        </div>


                        <div>

                            <span>
                                LOW PRIORITY
                            </span>

                            <strong>
                                ${
                                    dashboardData.alerts.filter(
                                        alert =>
                                            alert.severity === "low"
                                    ).length
                                }
                            </strong>

                        </div>


                        <div>

                            <span>
                                FASTEST GROWING
                            </span>

                            <strong>
                                ↑ 34%
                            </strong>

                        </div>

                    </section>


                    <section class="alerts-page-list">

                        <div class="alerts-page-heading">

                            <div>

                                <p class="eyebrow">
                                    ACTIVE SIGNALS
                                </p>

                                <h2>
                                    Issues requiring attention
                                </h2>

                            </div>

                            <span>
                                Sorted by growth
                            </span>

                        </div>


                        <div class="alert-tiles-grid">

                            ${dashboardData.alerts
                                .slice()
                                .sort(
                                    (a, b) =>
                                        b.growth - a.growth
                                )
                                .map(
                                    renderDetailedAlertRow
                                )
                                .join("")}

                        </div>

                    </section>

                </section>

            </main>

        </div>
    `;


    document.getElementById("back-to-dashboard")?.addEventListener("click", renderDashboard);

    /* =========================================
       BACK TO DASHBOARD
       ========================================= */

    const backButton =
        document.getElementById(
            "back-from-alerts"
        );

    if (backButton) {

        backButton.addEventListener(
            "click",
            () => {
                renderDashboard();
            }
        );
    }


    /* =========================================
       ALERT CLICK
       ========================================= */

    const alertRows =
        document.querySelectorAll(
            "[data-detailed-alert]"
        );

    alertRows.forEach(row => {

        row.addEventListener(
            "click",
            () => {

                const alertId =
                    row.dataset.detailedAlert;

                const alert =
                    dashboardData.alerts.find(
                        item =>
                            item.id === alertId
                    );

                if (!alert) {
                    return;
                }

                appState.selectedAlert = alert;

                renderAlertDetail(alert);
            }
        );
    });


    /* =========================================
       SIDEBAR NAVIGATION
       ========================================= */

    attachDetailNavigation();
}


/* =========================================================
   DETAILED ALERT ROW
   ========================================================= */

function renderDetailedAlertRow(alert) {

    return `
        <button
            class="detailed-alert-row"
            data-detailed-alert="${alert.id}"
        >

            <div class="detailed-alert-number">
                ${String(
                    dashboardData.alerts.indexOf(alert) + 1
                ).padStart(2, "0")}
            </div>


            <div class="detailed-alert-main">

                <div class="detailed-alert-title">

                    <span class="alert-dot"></span>

                    <h3>
                        ${alert.title}
                    </h3>

                </div>

                <p>
                    ${alert.product}
                    <span>•</span>
                    ${alert.region}
                </p>

            </div>


            <div class="detailed-alert-growth">

                <strong>
                    ↑ ${alert.growth}%
                </strong>

                <span>
                    complaint growth
                </span>

            </div>


            <div class="detailed-alert-started">

                <span>
                    DETECTED
                </span>

                <strong>
                    ${alert.started}
                </strong>

            </div>


            <div>

                <span
                    class="
                        badge
                        badge-${alert.severity}
                    "
                >
                    ${alert.severity.toUpperCase()}
                </span>

            </div>


            <div class="detailed-alert-arrow">
                →
            </div>

        </button>
    `;
}


/* =========================================================
   ALERT DETAIL SCREEN
   ========================================================= */

function renderAlertDetail(alert) {

    const app = document.getElementById("app");

    const relatedReviews =
        dashboardData.reviews.filter(review =>
            review.theme.toLowerCase() ===
            (
                alert.theme ||
                alert.title
            ).toLowerCase()
        );


    /*
     * These values will eventually come from the backend.
     * For now we use the available demo data.
     */

    const started =
        alert.started || "6 days ago";

    const product =
        alert.product || "All Products";

    const region =
        alert.region || "All Regions";

    const growth =
        alert.growth || 0;

    const severity =
        alert.severity || "medium";

    const reason =
        alert.reason ||
        `Customer complaints related to ${alert.title.toLowerCase()}
        have increased during the current period.`;

    const recommendation =
        alert.recommendation ||
        `Investigate the ${alert.title.toLowerCase()} pattern,
        review the affected customer feedback, and identify
        the operational cause before the issue becomes widespread.`;


    app.innerHTML = `

        <div class="dashboard-layout">


            <!-- =========================================
                 SIDEBAR
                 ========================================= -->

            <aside class="sidebar">

                <div class="sidebar-brand">
                    INSIGHT<span>/</span>
                </div>


                <div class="workspace-label">
                    CUSTOMER INTELLIGENCE
                </div>


                <nav class="sidebar-nav">

                    <button
                        class="nav-item"
                        data-screen="dashboard"
                    >
                        <span>01</span>
                        Overview
                    </button>


                    <button
                        class="nav-item"
                        data-screen="themes"
                    >
                        <span>02</span>
                        Themes
                    </button>


                    <button
                        class="nav-item active"
                        data-screen="alerts"
                    >
                        <span>03</span>
                        Emerging Issues

                        <span class="nav-count">
                            ${dashboardData.alerts.length
                                .toString()
                                .padStart(2, "0")}
                        </span>
                    </button>


                    <button
                        class="nav-item"
                        data-screen="evidence"
                    >
                        <span>04</span>
                        Evidence
                    </button>


                    <button
                        class="nav-item"
                        data-screen="trends"
                    >
                        <span>05</span>
                        Trends
                    </button>

                </nav>


                <div class="sidebar-bottom">

                    <button class="nav-item" data-screen="summary">
                        <span>06</span>
                        Reports
                    </button>

                    <button class="nav-item" id="logout-button">
                        <span>07</span>
                        Logout
                    </button>

                </div>

            </aside>


            <!-- =========================================
                 MAIN
                 ========================================= -->

            <main class="dashboard-main">


                <!-- TOPBAR -->

                <header class="topbar">

                    <button
                        class="mobile-menu"
                        aria-label="Open navigation"
                    >
                        ☰
                    </button>


                    <div>

                        <p class="topbar-label">
                            CUSTOMER INTELLIGENCE
                        </p>

                        <h2>
                            Alert Detail
                        </h2>

                    </div>


                    <div class="topbar-actions">

                        <button
                            class="icon-button"
                            aria-label="Notifications"
                        >
                            ♢
                        </button>


                        <div class="user-profile">

                            <div class="user-avatar">
                                ${getRoleInitial()}
                            </div>

                            <div>

                                <strong>
                                    ${getRoleName()}
                                </strong>

                                <span>
                                    Workspace
                                </span>

                            </div>

                        </div>

                    </div>

                </header>


                <!-- CONTENT -->

                <section class="dashboard-content">


                    <button
                        class="back-button"
                        id="back-to-alerts"
                    >
                        ← Back to emerging issues
                    </button>


                    <!-- =================================
                         ALERT HEADER
                         ================================= -->

                    <div class="alert-detail-header">

                        <div>

                            <p class="eyebrow">
                                EMERGING ISSUE
                            </p>


                            <div class="alert-detail-title-row">

                                <h1>
                                    ${alert.title}
                                </h1>


                                <span
                                    class="
                                        badge
                                        badge-${severity}
                                    "
                                >
                                    ${severity.toUpperCase()}
                                </span>

                            </div>


                            <p class="alert-detail-description">
                                A customer issue showing
                                increasing momentum.
                            </p>

                        </div>


                        <div class="alert-growth-large">

                            <strong>
                                ↑ ${growth}%
                            </strong>

                            <span>
                                complaint growth
                            </span>

                        </div>

                    </div>


                    <!-- =================================
                         KEY INFORMATION
                         ================================= -->

                    <section class="alert-detail-grid">


                        <!-- WHEN -->

                        <article class="alert-detail-card">

                            <p class="eyebrow">
                                WHEN IT STARTED
                            </p>

                            <h2>
                                ${started}
                            </h2>

                            <p>
                                First detected through
                                changing customer feedback.
                            </p>

                        </article>


                        <!-- AFFECTED AREA -->

                        <article class="alert-detail-card">

                            <p class="eyebrow">
                                AFFECTED AREA
                            </p>

                            <h2>
                                ${product}
                            </h2>

                            <p>
                                ${region}
                            </p>

                        </article>


                        <!-- GROWTH -->

                        <article class="alert-detail-card">

                            <p class="eyebrow">
                                CURRENT SIGNAL
                            </p>

                            <h2 class="text-danger">
                                ↑ ${growth}%
                            </h2>

                            <p>
                                Compared with the previous
                                period.
                            </p>

                        </article>


                    </section>


                    <!-- =================================
                         WHY IT IS INCREASING
                         ================================= -->

                    <section class="alert-explanation">

                        <div class="alert-section-label">

                            <p class="eyebrow">
                                WHY IT'S INCREASING
                            </p>

                            <h2>
                                What's behind the signal?
                            </h2>

                        </div>


                        <div class="alert-explanation-content">

                            <p>
                                ${reason}
                            </p>

                        </div>

                    </section>


                    <!-- =================================
                         EVIDENCE
                         ================================= -->

                    <section class="alert-evidence-section">

                        <div class="section-heading">

                            <div>

                                <p class="eyebrow">
                                    EVIDENCE
                                </p>

                                <h2>
                                    Customer feedback behind
                                    the alert
                                </h2>

                            </div>


                            <span class="section-period">
                                ${relatedReviews.length}
                                related reviews
                            </span>

                        </div>


                        <div class="alert-evidence-list">

                            ${
                                relatedReviews.length
                                    ? relatedReviews
                                        .slice(0, 3)
                                        .map(
                                            renderAlertEvidence
                                        )
                                        .join("")
                                    : `
                                        <div class="empty-state">
                                            No related evidence
                                            available.
                                        </div>
                                    `
                            }

                        </div>


                        ${
                            relatedReviews.length
                                ? `
                                    <div class="detail-action">

                                        <button
                                            class="btn btn-primary"
                                            id="view-alert-evidence"
                                        >
                                            View all evidence →
                                        </button>

                                    </div>
                                  `
                                : ""
                        }

                    </section>


                    <!-- =================================
                         RECOMMENDED ACTION
                         ================================= -->

                    <section class="recommended-action">

                        <div class="recommendation-icon">
                            →
                        </div>


                        <div>

                            <p class="eyebrow">
                                RECOMMENDED ACTION
                            </p>

                            <h2>
                                Investigate before the
                                signal becomes widespread.
                            </h2>

                            <p>
                                ${recommendation}
                            </p>

                        </div>

                    </section>


                </section>

            </main>

        </div>
    `;


    /* =========================================
       BACK TO ALERTS
       ========================================= */

    const backButton =
        document.getElementById(
            "back-to-alerts"
        );

    if (backButton) {

        backButton.addEventListener(
            "click",
            () => {
                renderAlertsScreen();
            }
        );
    }


    /* =========================================
       VIEW RELATED EVIDENCE
       ========================================= */

    const evidenceButton =
        document.getElementById(
            "view-alert-evidence"
        );

    if (evidenceButton) {

        evidenceButton.addEventListener(
            "click",
            () => {

                const themeName =
                    alert.theme ||
                    alert.title;

                const theme =
                    dashboardData.themes.find(
                        item =>
                            item.name.toLowerCase() ===
                            themeName.toLowerCase()
                    );

                renderEvidenceScreen(theme);

            }
        );
    }


    attachDetailNavigation();
}


/* =========================================================
   ALERT EVIDENCE PREVIEW
   ========================================================= */

function renderAlertEvidence(review) {

    return `
        <article class="alert-evidence-item">

            <div>

                <span
                    class="
                        review-sentiment
                        ${review.sentiment.toLowerCase()}
                    "
                >
                    ${review.sentiment}
                </span>

            </div>


            <p>
                "${review.text}"
            </p>


            <div class="alert-evidence-meta">

                <span>
                    ${review.region}
                </span>

                <span>
                    •
                </span>

                <span>
                    ${review.theme}
                </span>

            </div>

        </article>
    `;
}

/* =========================================================
   FILTER PANEL
   ========================================================= */

function openFilterPanel() {

    const existingPanel =
        document.getElementById("filter-panel");

    if (existingPanel) {
        existingPanel.remove();
        return;
    }


    const products = [
        "All Products",
        ...new Set(
            dashboardData.reviews.map(
                review => review.product
            ).filter(Boolean)
        )
    ];


    const regions = [
        "All Regions",
        ...new Set(
            dashboardData.reviews.map(
                review => review.region
            ).filter(Boolean)
        )
    ];


    const panel = document.createElement("div");

    panel.id = "filter-panel";

    panel.innerHTML = `

        <div class="filter-backdrop"
             id="filter-backdrop">
        </div>


        <aside class="filter-drawer">

            <div class="filter-drawer-header">

                <div>

                    <p class="eyebrow">
                        DASHBOARD FILTERS
                    </p>

                    <h2>
                        Refine customer voice
                    </h2>

                </div>


                <button
                    class="filter-close"
                    id="filter-close"
                    aria-label="Close filters"
                >
                    ×
                </button>

            </div>


            <div class="filter-drawer-body">


                <!-- PRODUCT -->

                <div class="filter-field">

                    <label for="filter-product">
                        Product
                    </label>

                    <select id="filter-product">

                        ${products.map(
                            product => `
                                <option value="${product}">
                                    ${product}
                                </option>
                            `
                        ).join("")}

                    </select>

                </div>


                <!-- DATE RANGE -->

                <div class="filter-field">

                    <label for="filter-date">
                        Date range
                    </label>

                    <select id="filter-date">

                        <option value="30">
                            Last 30 days
                        </option>

                        <option value="14">
                            Last 14 days
                        </option>

                        <option value="7">
                            Last 7 days
                        </option>

                        <option value="90">
                            Last 90 days
                        </option>

                    </select>

                </div>


                <!-- REGION -->

                <div class="filter-field">

                    <label for="filter-region">
                        Region
                    </label>

                    <select id="filter-region">

                        ${regions.map(
                            region => `
                                <option value="${region}">
                                    ${region}
                                </option>
                            `
                        ).join("")}

                    </select>

                </div>


            </div>


            <div class="filter-drawer-footer">

                <button
                    class="btn btn-secondary"
                    id="clear-filters"
                >
                    Clear
                </button>


                <button
                    class="btn btn-primary"
                    id="apply-filters"
                >
                    Apply filters
                </button>

            </div>

        </aside>
    `;


    document.body.appendChild(panel);


    /* =========================================
       OPEN / CLOSE
       ========================================= */

    requestAnimationFrame(() => {
        panel.classList.add("open");
    });


    const closePanel = () => {

        panel.classList.remove("open");

        setTimeout(() => {
            panel.remove();
        }, 220);
    };


    document
        .getElementById("filter-close")
        .addEventListener(
            "click",
            closePanel
        );


    document
        .getElementById("filter-backdrop")
        .addEventListener(
            "click",
            closePanel
        );


    /* =========================================
       CLEAR
       ========================================= */

    document
        .getElementById("clear-filters")
        .addEventListener(
            "click",
            () => {

                document.getElementById(
                    "filter-product"
                ).value = "All Products";


                document.getElementById(
                    "filter-date"
                ).value = "30";


                document.getElementById(
                    "filter-region"
                ).value = "All Regions";

            }
        );


    /* =========================================
       APPLY
       ========================================= */

    document
        .getElementById("apply-filters")
        .addEventListener(
            "click",
            () => {

                const product =
                    document.getElementById(
                        "filter-product"
                    ).value;


                const dateRange =
                    document.getElementById(
                        "filter-date"
                    ).value;


                const region =
                    document.getElementById(
                        "filter-region"
                    ).value;


                appState.filters = {
                    product,
                    dateRange,
                    region
                };


                closePanel();

                renderDashboard();

            }
        );
}
/* =========================================================
   USER INFORMATION
   ========================================================= */


function getRoleName() {
    return "Insight Workspace";
}

function getRoleInitial() {
    return "I";
}

/* =========================================================
   THEMES NAVIGATION
   ========================================================= */

document.addEventListener("click", function (event) {

    const clickedElement = event.target.closest("#themes-button");

    if (!clickedElement) {
        return;
    }

    renderDashboard();

    setTimeout(() => {

        const themesSection =
            document.getElementById("themes-section");

        if (themesSection) {
            themesSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }

    }, 100);

});

/* =========================================================
   GLOBAL SIDEBAR NAVIGATION
   ========================================================= */

/* =========================================================
   GLOBAL SIDEBAR NAVIGATION
   ========================================================= */

document.addEventListener("click", function (event) {

    const navItem = event.target.closest(
        ".sidebar-nav .nav-item"
    );

    if (!navItem) {
        return;
    }

    const screen = navItem.getAttribute("data-screen");

    if (!screen) {
        return;
    }

    event.preventDefault();

    console.log("Navigation clicked:", screen);

    switch (screen) {

        case "dashboard":
            renderDashboard();
            break;

        case "themes":

            renderDashboard();

            setTimeout(function () {

                const themesSection =
                    document.getElementById("themes-section");

                if (themesSection) {
                    themesSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }

            }, 150);

            break;

        case "alerts":
            renderAlertsScreen();
            break;

        case "evidence":
            renderEvidenceScreen();
            break;

        case "trends":
            renderTrendsScreen();
            break;

        default:
            console.log(
                "Navigation not implemented:",
                screen
            );
    }

}, true);
/* =========================================================
   GLOBAL REPORT / LOGOUT HANDLERS
   ========================================================= */

document.addEventListener("click", function (event) {
    const report = event.target.closest('.sidebar-nav .nav-item[data-screen="summary"], .sidebar-bottom .nav-item[data-screen="summary"]');
    if (report) { event.preventDefault(); renderSummaryScreen(); return; }
    const logout = event.target.closest("#logout-button");
    if (logout) { event.preventDefault(); appState.selectedRole = null; appState.currentScreen = "login"; renderLoginScreen(); return; }
    const menu = event.target.closest(".mobile-menu");
    if (menu) {
        const sidebar = document.querySelector(".sidebar");
        if (sidebar) sidebar.classList.toggle("mobile-open");
    }
});

/* =========================================================
   START APPLICATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeApp
);
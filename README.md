# 🛡️ SENTINEL
### Climate-Aware Autonomous Investing System

<img width="1200" height="400" alt="image" src="https://github.com/user-attachments/assets/e6196cb4-26ee-4cce-b337-b84f36f1272b" />


> **An ESG-intelligent multi-agent investment platform that analyzes, simulates, validates, and executes trades — with built-in safety rails and full explainability.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Hackathon%20Demo-brightgreen?style=for-the-badge)]()

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Live Demo Screenshots](#-live-demo-screenshots)
- [Architecture](#-architecture)
- [Agent Roles](#-agent-roles)
- [Tech Stack](#-tech-stack)
- [File Structure](#-file-structure)
- [API Reference](#-api-reference)
- [Setup & Installation](#-setup--installation)
- [Demo Flow](#-demo-flow)
- [Key Features](#-key-features)
- [Roadmap](#-roadmap)

---

## 🌍 Overview

**Sentinel** is a hackathon project built as a fully autonomous, ESG-aware investment system. It uses an **OpenClaw-inspired multi-agent architecture** where a dynamic orchestrator coordinates 8 specialized AI agents — each responsible for a distinct step in the investment decision pipeline.

Unlike traditional robo-advisors that optimize purely for financial return, Sentinel integrates **climate risk scoring**, **ESG compliance filtering**, and **policy-enforced trade validation** (via the ArmourIQ Guard layer) into every investment decision. Every trade is explainable, every constraint is enforced, and every step is visualized.

---

## 🔴 Problem Statement

Modern investment platforms have two critical blind spots:

1. **Climate Ignorance** — They optimize for financial returns while ignoring ESG exposure, carbon risk, and transition risk under scenarios like Paris 1.5°C alignment.
2. **Black-Box AI** — Automated systems make decisions without transparency, making them hard to audit, trust, or regulate.

Sentinel solves both by making every investment decision **climate-aware**, **policy-constrained**, and **fully explainable**.

---

## 📸 Live Demo Screenshots

### Dashboard
The main interface shows portfolio value, risk tolerance settings, ESG constraints, and the Climate Resilience score with ArmourIQ Shield active.

<img width="1919" height="970" alt="Screenshot 2026-04-03 185021" src="https://github.com/user-attachments/assets/651244b9-28a0-4cd7-a473-2d660e262b67" />

<img width="1919" height="967" alt="Screenshot 2026-04-03 185040" src="https://github.com/user-attachments/assets/fa1984c7-1698-45bf-ab5e-07558c7d36a9" />

> Portfolio: $284,500.73 (+14.2% 30D) | Climate Resilience: 72/100 | ArmourIQ Shield: ACTIVE

---

### Analysis Pipeline (OpenClaw Multi-Agent)
Displays the live agent execution trace: Climate → Financial → Simulation → Portfolio → Trade → Guard → Trader → Explain. Each step is labeled Completed, Skipped, or Blocked.

<img width="1919" height="970" alt="Screenshot 2026-04-03 185133" src="https://github.com/user-attachments/assets/00e0a9e5-3502-452f-9004-899324355669" />

<img width="1919" height="966" alt="Screenshot 2026-04-03 185150" src="https://github.com/user-attachments/assets/8ac57fa6-4631-487a-a1eb-bfb7f4830621" />

---

### Simulator
Monte Carlo simulation engine with configurable investment amount, stock ticker, duration (1M–5Y), and risk appetite. Shows Best Case / Median / Worst Case trajectories with Sharpe Ratio, Sortino Ratio, Beta, and Value at Risk.

<img width="1919" height="973" alt="Screenshot 2026-04-03 185214" src="https://github.com/user-attachments/assets/9fdc6a7c-e8df-4588-bd15-c997aec56666" />

---

### Guard & Policies (Trade Enforcement)
Visual flowchart of the trade validation logic: Size OK? → Climate Risk? → Execute/Block. Includes a real-time Trade Testing Tool with APPROVE/REJECT output.

<img width="1919" height="966" alt="Screenshot 2026-04-03 185243" src="https://github.com/user-attachments/assets/6785c1c7-75d9-492d-a6de-ec7e3017fe76" />

---

### Insights / Impact (Portfolio Climate Intelligence)
Asset ESG Profiles (NVDA, MSFT, AAPL, CVX, XOM), Sector Exposure Limits with carbon-heavy flags, Climate Risk Matrix across Carbon/Water/Waste/Trans/Phys axes, and overall Portfolio Rating gauge.

<img width="1919" height="968" alt="Screenshot 2026-04-03 185258" src="https://github.com/user-attachments/assets/787ab9c7-7c77-4046-91a0-5161f4ddc59c" />

---

## 🏗️ Architecture

Sentinel uses a **dynamic orchestrator** (not a static pipeline) that decides which agents to invoke, skip, or block based on real-time conditions.

```
User Input (Constraints)
        │
        ▼
  ┌─────────────┐
  │ Orchestrator │  ← Master coordinator (OpenClaw-style)
  └──────┬───────┘
         │
  ┌──────▼────────────────────────────────────────────────┐
  │                  Agent Pipeline                        │
  │                                                        │
  │  [1] Climate Agent  ──→  ESG filter & scoring         │
  │  [2] Financial Agent ──→ Market trend analysis         │
  │  [3] Simulation Agent ──→ Monte Carlo (conditional)   │
  │  [4] Portfolio Agent ──→ Allocation generation        │
  │  [5] Trade Agent ──→ Trade signal from allowed assets │
  │  [6] Guard Agent ──→ Policy validation (ArmourIQ)     │
  │  [7] Trader Agent ──→ Execute if approved             │
  │  [8] Explain Agent ──→ Human-readable reasoning       │
  └────────────────────────────────────────────────────────┘
         │
         ▼
  Frontend Visualization
```

Each agent reports one of three statuses: `completed` | `skipped` | `blocked`

---

## 🤖 Agent Roles

| Agent | Role | Triggers |
|---|---|---|
| **Climate** | Filters assets based on ESG/climate data; assigns green scores | Always runs |
| **Financial** | Analyzes market trends, expected return, volatility | Always runs |
| **Simulation** | Runs Monte Carlo risk-return simulations | Conditional (moderate/high risk) |
| **Portfolio** | Generates allocation weights using real stock prices | Always runs |
| **Trade** | Generates trade signals ONLY from ESG-allowed assets | Always runs |
| **Guard** | Validates trades against all user constraints (ArmourIQ) | Always runs |
| **Trader** | Executes trade via Alpaca API if Guard approves | Conditional on Guard pass |
| **Explain** | Generates natural language reasoning for the decision | Always runs |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — High-performance REST API framework
- **Python 3.10+** — Core orchestration logic
- **NumPy** — Monte Carlo simulation engine
- **yfinance** — Real-time stock prices and ESG data (free API)

### Frontend
- **HTML5 / CSS3 / JavaScript** — Static multi-page frontend
- **Chart.js** — Portfolio and simulation visualizations
- **Vanilla JS** — Fetch API calls to FastAPI backend

### AI Orchestration
- **OpenClaw-inspired orchestrator** — Dynamic agent sequencing with conditional routing
- **Custom multi-agent framework** — Each agent is a modular Python class

### Safety Layer
- **ArmourIQ Guard** — Policy enforcement engine
  - Blocks trades in avoided sectors
  - Enforces max trade size limits
  - Validates allocation constraints
  - Logs all decisions with timestamps

### Trading Integration
- **Alpaca API** (Paper trading mode) — Simulated trade execution

### Data Sources
- **yfinance** — Stock prices, ESG scores, market data (100% free)
- **Fallback climate data** — Static mapping for ESG scoring when live data unavailable

---

## 📁 File Structure

```
Sentinel/
├── backend/
│   └── app/
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── climate.py          # ESG scoring & sector filtering
│       │   ├── explain.py          # Human-readable decision reasoning
│       │   ├── financial.py        # Market analysis & sentiment
│       │   ├── guard.py            # ArmourIQ trade validation
│       │   ├── master.py           # Master coordination agent
│       │   ├── orchestrator.py     # Dynamic pipeline orchestrator ⭐
│       │   ├── portfolio.py        # Portfolio allocation engine
│       │   ├── simulation.py       # Monte Carlo simulation agent
│       │   └── trader.py           # Trade execution agent
│       ├── api/
│       │   └── routes.py           # FastAPI route definitions
│       ├── core/
│       │   ├── config.py           # App configuration
│       │   ├── constants.py        # System-wide constants
│       │   └── logger.py           # Logging setup
│       ├── data/
│       │   ├── climate_data.json   # ESG fallback dataset
│       │   └── sample_stocks.json  # Stock universe
│       ├── models/
│       │   ├── request_models.py   # Pydantic request schemas
│       │   └── response_models.py  # Pydantic response schemas
│       ├── services/
│       │   ├── climate_data.py     # Climate data service
│       │   ├── market_data.py      # Market data fetcher
│       │   ├── optimizer.py        # Portfolio optimizer
│       │   ├── policy_service.py   # Policy management
│       │   ├── risk.py             # Risk calculations
│       │   ├── simulation_engine.py # Core simulation logic
│       │   └── trading_service.py  # Alpaca integration
│       ├── utils/
│       │   ├── helpers.py
│       │   └── validators.py
│       └── main.py                 # FastAPI app entry point
│
├── frontend/
│   ├── dashboard.html              # Main dashboard (index)
│   ├── guard.html                  # Trade Enforcement & Policies
│   ├── index.html                  # Entry / login page
│   ├── insights.html               # Portfolio Climate Intelligence
│   ├── pipeline.html               # Analysis Pipeline (agent flow)
│   ├── simulator.html              # Monte Carlo Simulator
│   ├── script.js                   # Shared JS / API calls
│   ├── styles.css                  # Global styles
│   └── package.json
│
├── requirements.txt
├── README.md
└── .gitattributes
```

---

## 🌐 API Reference

### Core Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | **Main pipeline** — runs the full multi-agent flow |
| `POST` | `/portfolio` | Generate portfolio allocation |
| `GET` | `/climate-scores` | Fetch ESG/climate scores for assets |
| `POST` | `/simulate` | Run Monte Carlo simulation |

### Guard (ArmourIQ) Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/validate-trade` | Validate a trade against active policies |
| `GET` | `/policies` | List all active constraint policies |

### Trading Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/execute-trade` | Execute approved trade via Alpaca |

### Utility Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/explain` | Generate human-readable explanation |
| `GET` | `/health` | Server health check |

### Example: `/analyze` Request

```json
{
  "budget": 100000,
  "risk_level": "moderate",
  "max_trade": 50000,
  "avoid_sectors": ["coal", "fossil"]
}
```

### Example: `/analyze` Response

```json
{
  "pipeline": [
    { "agent": "climate", "status": "completed" },
    { "agent": "financial", "status": "completed" },
    { "agent": "simulation", "status": "completed" },
    { "agent": "portfolio", "status": "completed" },
    { "agent": "trade", "status": "completed" },
    { "agent": "guard", "status": "completed" },
    { "agent": "trader", "status": "completed" },
    { "agent": "explain", "status": "completed" }
  ],
  "climate": { "green_score": 83.5, "eligible_assets": ["AAPL", "MSFT", "TSLA"] },
  "financial": { "sentiment": "cautiously optimistic", "expected_return": 8.83, "volatility": 10.0 },
  "portfolio": { "AAPL": 0.34, "MSFT": 0.36, "TSLA": 0.30 },
  "trade": { "action": "BUY", "ticker": "TSLA", "quantity": 138 },
  "guard": { "approved": true, "violations": [] },
  "explanation": "The TSLA trade was APPROVED as it passed all fiscal limits and rigorously respected sector restrictions."
}
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- pip
- (Optional) Alpaca paper trading account for execution simulation

### 1. Clone the Repository

```bash
git clone https://github.com/TopGnextdoor/Sentinel-Climate-Aware-Autonomous-Investing-System-1.0.git
cd Sentinel-Climate-Aware-Autonomous-Investing-System-1.0
```

### 2. Set Up the Backend

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in `backend/`:

```env
# Optional: Alpaca API (paper trading)
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# App settings
DEBUG=true
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

> **Note:** Alpaca keys are optional. The system runs in simulation mode without them.

### 4. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### 5. Launch the Frontend

Open `frontend/dashboard.html` directly in your browser, or serve it with:

```bash
# Using VS Code Live Server, or:
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500/dashboard.html`

---

## 🎬 Demo Flow

Here's the intended walkthrough for a live demo:

```
1. Open Dashboard → Set budget, risk tolerance, ESG constraints
2. Click "RUN ANALYSIS" → Watch agent pipeline execute in real-time
3. Navigate to Analysis Pipeline → See each agent step: Completed / Skipped / Blocked
4. Check Portfolio Allocation → AAPL / MSFT / TSLA distribution
5. View Trade Recommendation → e.g., "BUY 138 shares TSLA"
6. See Guard Decision → APPROVED or BLOCKED with violation details
7. Read AI Decision Summary → Human-readable explanation of the full decision
8. Go to Simulator → Run Monte Carlo on any ticker with custom params
9. Go to Guard & Policies → Test a custom trade (e.g., XOM in fossil sector → BLOCKED)
10. Go to Insights → Portfolio Climate Intelligence — ESG profiles, sector exposure, risk matrix
```

---

## ✨ Key Features

### 🌿 ESG-Aware Investing
Every asset in the portfolio is scored on Carbon, Water, Waste, Transition Risk, and Physical Risk. Fossil stocks and carbon-heavy sectors are automatically filtered out based on user-defined constraints.

### 🤖 Dynamic Multi-Agent Orchestration
The pipeline is not static. The orchestrator conditionally skips or triggers agents (e.g., simulation only runs for moderate/high risk, trader only runs if guard approves). Real-time execution logs are shown in the UI.

### 🛡️ ArmourIQ Guard Rails
Every generated trade passes through a policy enforcement engine before execution. Constraints include:
- **Sector Avoidance** — Blocks assets matching avoided sectors
- **Max Drawdown Cap** — Blocks trades if simulation predicts excessive drawdown
- **Allocation Constraint** — Prevents any single asset from exceeding 20% of net

### 📊 Monte Carlo Simulation
Configurable simulation engine with Best Case / Median / Worst Case trajectory visualization. Outputs Sharpe Ratio, Sortino Ratio, Beta, VaR, and drawdown probability.

### 🧠 Explainable AI
Every decision generates a structured explanation covering Portfolio Context, Trade Intent, Decision Reasoning, and Simulation Validation in plain English.

### 📡 Real-Time Data
All stock prices and ESG data are pulled live from Yahoo Finance (yfinance) — no paid API required.

---

## 🗺️ Roadmap

| Status | Feature |
|---|---|
| ✅ | Multi-agent orchestration (OpenClaw-style) |
| ✅ | ESG-aware portfolio generation |
| ✅ | Monte Carlo simulation engine |
| ✅ | ArmourIQ Guard with policy enforcement |
| ✅ | Explainable AI decision summaries |
| ✅ | Frontend visualization of agent flow |
| ✅ | Alpaca paper trading integration |
| 🔄 | Full live real-time API integration |
| 🔄 | API response caching for performance |
| ⬜ | Advanced charting and portfolio analytics |
| ⬜ | Personalized AI investment strategies |
| ⬜ | Mobile application |
| ⬜ | Expanded ESG datasets (beyond yfinance) |
| ⬜ | Live trading (non-paper) integration |

---

> *"Every investment decision should be intelligent, transparent, and safe — for people and the planet."*

Sentinel AI – Climate-Aware Autonomous Investing

OVERVIEW

•	Sentinel AI is a multi-agent autonomous investment system that combines financial analysis with climate risk intelligence. It uses OpenClaw for orchestration and ArmourIQ for enforcing safe and compliant decisions.

•	The system does not just predict returns, it ensures that every investment is explainable, risk-aware, and policy-compliant.
________________________________________

PROBLEM STATEMENT

•	Traditional investment platforms focus only on financial returns while ignoring climate risks such as environmental exposure, regulatory changes, and sustainability impact.

•	Additionally, AI-driven systems often lack transparency and safety, making their decisions hard to trust.
________________________________________

SOLUTION

Sentinel AI introduces a multi-agent architecture where each agent performs a specific role:

•	Financial Analysis Agent evaluates market trends

•	Climate Risk Agent assesses ESG and environmental exposure

•	Simulation Agent predicts future performance

•	Portfolio Agent generates optimized allocations

•	Trader Agent executes trades

•	Guard Agent (powered by ArmourIQ) enforces safety and policy constraints

•	Explain Agent provides clear reasoning behind decisions
This ensures decisions are intelligent, transparent, and safe.

________________________________________

KEY FEATURES

MULTI AGENT DECISION SYSTEM

•	Each step of investment is handled by specialized AI agents coordinated using OpenClaw.

CLIMATE RISK INTEGRATION

•	Every stock is evaluated not only financially but also based on environmental and sustainability risks.
Guardrails with ArmourIQ

ALL TRADES PASS THROUGH A POLICY ENFORCEMENT LAYER:

•	Blocks high-risk or non-compliant trades

•	Enforces user-defined constraints

•	Ensures safe AI behavior

EXPLAINABLE AI

•	Every decision includes a human-readable explanation.
Simulation Engine

•	Monte Carlo simulations predict possible future outcomes and risk probabilities.
________________________________________

TECH STACK

FRONTEND

•	HTML

•	CSS

•	JavaScript

•	Chart.js for visualizations

BACKEND

•	Python (FastAPI)

•	REST API architecture

•	Modular agent-based system

AI ORCHESTRATION

•	OpenClaw for managing multi-agent workflows

•	Handles sequencing: Climate → Financial → Simulation → Portfolio → Trade

SAFETY LAYER

•	ArmourIQ for policy enforcement

•	Validates every trade before execution

•	Maintains decision logs and constraints

DATA AND PROCESSING

•	NumPy for simulations

•	External APIs for market and climate data

Trading Integration

•	Alpaca API (paper trading) for executing trades

________________________________________

API ENDPOINTS

CORE

•	POST /analyze – Main pipeline execution
Supporting

•	POST /portfolio – Portfolio generation

•	GET /climate-scores – Climate data

•	POST /simulate – Run simulations
Guard (ArmourIQ)

•	POST /validate-trade – Check trade safety

•	GET /policies – Active constraints
Trading

•	POST /execute-trade – Execute via Alpaca
Utility

•	POST /explain – Generate explanation

•	GET /health – Server status
________________________________________

SYSTEM FLOW

Frontend → /analyze → Master Agent
→ Climate Analysis
→ Financial Analysis
→ Simulation
→ Portfolio Generation
→ Trader Agent
→ Guard Agent (ArmourIQ)
→ Execute / Block
→ Explain Agent
→ Response to UI
________________________________________

UNIQUE VALUES

•	Combines finance + climate intelligence

•	Transparent AI decision-making

•	Built-in safety with ArmourIQ

•	Real-time explainable pipeline

•	Multi-agent architecture using OpenClaw
________________________________________

FUTURE SCOPE

•	Real-time live trading integration

•	Personalized AI strategies

•	Advanced ESG datasets
•	Mobile application


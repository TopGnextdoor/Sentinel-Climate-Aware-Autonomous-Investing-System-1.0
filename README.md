Sentinel AI – Climate-Aware Autonomous Investing
Overview
Sentinel AI is a multi-agent autonomous investment system that combines financial analysis with climate risk intelligence. It uses OpenClaw for orchestration and ArmourIQ for enforcing safe and compliant decisions.

The system does not just predict returns, it ensures that every investment is explainable, risk-aware, and policy-compliant.

Problem Statement
Traditional investment platforms focus only on financial returns while ignoring climate risks such as environmental exposure, regulatory changes, and sustainability impact.

Additionally, AI-driven systems often lack transparency and safety, making their decisions hard to trust.

Solution
Sentinel AI introduces a multi-agent architecture where each agent performs a specific role:

Financial Analysis Agent evaluates market trends

Climate Risk Agent assesses ESG and environmental exposure

Simulation Agent predicts future performance

Portfolio Agent generates optimized allocations

Trader Agent executes trades

Guard Agent (powered by ArmourIQ) enforces safety and policy constraints

Explain Agent provides clear reasoning behind decisions

This ensures decisions are intelligent, transparent, and safe.

Key Features
Multi-Agent Decision System
Each step of investment is handled by specialized AI agents coordinated using OpenClaw.

Climate Risk Integration
Every stock is evaluated not only financially but also based on environmental and sustainability risks.

Guardrails with ArmourIQ
All trades pass through a policy enforcement layer:

Blocks high-risk or non-compliant trades

Enforces user-defined constraints

Ensures safe AI behavior

Explainable AI
Every decision includes a human-readable explanation.

Simulation Engine
Monte Carlo simulations predict possible future outcomes and risk probabilities.

Tech Stack
Frontend
HTML

CSS

JavaScript

Chart.js for visualizations

Backend
Python (FastAPI)

REST API architecture

Modular agent-based system

AI Orchestration
OpenClaw for managing multi-agent workflows

Handles sequencing: Climate → Financial → Simulation → Portfolio → Trade

Safety Layer
ArmourIQ for policy enforcement

Validates every trade before execution

Maintains decision logs and constraints

Data & Processing
NumPy for simulations

External APIs for market and climate data

Trading Integration
Alpaca API (paper trading) for executing trades

API Endpoints
Core
POST /analyze – Main pipeline execution

Supporting
POST /portfolio – Portfolio generation

GET /climate-scores – Climate data

POST /simulate – Run simulations

Guard (ArmourIQ)
POST /validate-trade – Check trade safety

GET /policies – Active constraints

Trading
POST /execute-trade – Execute via Alpaca

Utility
POST /explain – Generate explanation

GET /health – Server status

System Flow
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

Unique Value
Combines finance + climate intelligence

Transparent AI decision-making

Built-in safety with ArmourIQ

Real-time explainable pipeline

Multi-agent architecture using OpenClaw

Future Scope
Real-time live trading integration

Personalized AI strategies

Advanced ESG datasets

Mobile application

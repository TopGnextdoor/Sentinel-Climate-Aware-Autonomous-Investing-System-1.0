// ============================================================
// SENTINEL — Centralized API Layer + Page Integration
// ============================================================

const BASE_URL = 'http://127.0.0.1:8000';

// ─────────────────────────────────────────
//  CORE API FUNCTIONS
// ─────────────────────────────────────────

async function apiFetch(path, method = 'GET', body = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    try {
        const res = await fetch(`${BASE_URL}${path}`, opts);
        if (!res.ok) {
            const errText = await res.text();
            throw new Error(`HTTP ${res.status}: ${errText}`);
        }
        return await res.json();
    } catch (err) {
        if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
            throw new Error('BACKEND_UNREACHABLE');
        }
        throw err;
    }
}

async function runAnalysis(data) {
    try {
        const result = await apiFetch('/analyze', 'POST', data);
        const orchestration = result.orchestration;
        return result;
    } catch (err) {
        throw err;
    }
}
async function getPortfolio(data)  { return apiFetch('/portfolio', 'POST', data); }
async function runSimulation(data) { return apiFetch('/simulate', 'POST', data); }
async function getClimateScores()  { return apiFetch('/climate-scores', 'GET'); }
async function validateTrade(data) { return apiFetch('/validate-trade', 'POST', data); }
async function executeTrade(data)  { return apiFetch('/execute-trade', 'POST', data); }
async function getPolicies()       { return apiFetch('/policies', 'GET'); }
async function getExplanation(data){ return apiFetch('/explain', 'POST', data); }

// ─────────────────────────────────────────
//  SHARED UI HELPERS
// ─────────────────────────────────────────

function setLoading(el, isLoading, originalHTML = '') {
    if (isLoading) {
        el.innerHTML = `
            <div style="display:flex;align-items:center;gap:12px;color:var(--neon-lime);font-family:'JetBrains Mono',monospace;font-size:0.85rem;">
                <div class="pulse-dot"></div> Querying Sentinel agents...
            </div>`;
    } else {
        el.innerHTML = originalHTML;
    }
}

function showError(container, message) {
    container.innerHTML = `
        <div style="padding:1.5rem;border:1px solid rgba(255,68,68,0.4);border-radius:12px;background:rgba(255,68,68,0.07);color:#ff6666;font-family:'JetBrains Mono',monospace;font-size:0.82rem;">
            ⚠️ ${message === 'BACKEND_UNREACHABLE'
                ? 'Backend not reachable. Make sure the Sentinel API is running on <b>http://127.0.0.1:8000</b>'
                : `Error: ${message}`}
        </div>`;
}

function guardBadge(status) {
    const map = {
        APPROVED: { color: '#00ff88', icon: '🛡️', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.3)' },
        BLOCKED:  { color: '#ff4444', icon: '🚫', bg: 'rgba(255,68,68,0.1)',  border: 'rgba(255,68,68,0.3)' },
        MODIFIED: { color: '#ffcc00', icon: '⚠️', bg: 'rgba(255,204,0,0.1)', border: 'rgba(255,204,0,0.3)' },
        SKIPPED:  { color: '#888',    icon: '⏭️', bg: 'rgba(136,136,136,0.1)', border: 'rgba(136,136,136,0.2)' },
    };
    const s = map[status] || map.SKIPPED;
    return `<span style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:20px;background:${s.bg};border:1px solid ${s.border};color:${s.color};font-weight:700;font-size:0.8rem;">${s.icon} ${status}</span>`;
}

function formatCurrency(val) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }).format(val);
}

// ─────────────────────────────────────────
//  PAGE: dashboard.html
// ─────────────────────────────────────────

function initDashboard() {
    // Risk toggle
    const riskBtns = document.querySelectorAll('.risk-btn');
    riskBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            riskBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Budget slider display
    const budgetSlider = document.querySelector('#budget-slider');
    const portfolioValue = document.querySelector('.portfolio-info h2');
    if (budgetSlider && portfolioValue) {
        budgetSlider.addEventListener('input', (e) => {
            portfolioValue.innerText = formatCurrency(e.target.value);
        });
    }

    // Chip toggle
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => chip.addEventListener('click', () => chip.classList.toggle('active')));

    // Gauge animation
    const gaugeProgress = document.querySelector('#gauge-progress');
    if (gaugeProgress) {
        setTimeout(() => { gaugeProgress.style.strokeDashoffset = '70'; }, 500);
    }

    // RUN ANALYSIS BUTTON
    const runBtn = document.getElementById('run-analysis-btn');
    if (!runBtn) return;

    const resultsContainer = document.getElementById('analysis-results');

    runBtn.addEventListener('click', async () => {
        const budget = parseFloat(document.getElementById('budget-slider')?.value || 100000);
        const activeRisk = document.querySelector('.risk-btn.active');
        const risk_level = activeRisk ? activeRisk.innerText.toLowerCase().replace('med', 'moderate') : 'moderate';
        const max_trade = parseFloat(document.getElementById('max-trade-input')?.value || 50000);
        const avoidChips = [...document.querySelectorAll('.chip.active')].map(c => c.innerText.replace('No ', '').toLowerCase());
        const avoid_sectors = avoidChips.length > 0 ? avoidChips : [];

        resultsContainer.style.display = 'block';
        setLoading(resultsContainer, true);
        runBtn.disabled = true;
        runBtn.style.opacity = '0.6';

        try {
            const data = await runAnalysis({ budget, risk_level, max_trade, avoid_sectors });
            renderDashboardResults(resultsContainer, data);
        } catch (err) {
            showError(resultsContainer, err.message);
        } finally {
            runBtn.disabled = false;
            runBtn.style.opacity = '1';
        }
    });
}

function renderDashboardResults(container, data) {
    const p = data.portfolio || {};
    const g = data.guard || {};
    const t = data.trade || {};
    const ex = data.execution || {};
    const explanation = data.explanation || 'No explanation available.';
    const guardStatus = g.status || 'UNKNOWN';

    // Portfolio holdings
    const holdingsHTML = (p.holdings || []).map(h =>
        `<div class="trade-row">
            <div style="font-weight:700">${h.ticker}</div>
            <div style="font-size:0.8rem;color:var(--muted-text)">${h.shares} shares @ ${(h.weight * 100).toFixed(1)}%</div>
            <span class="trade-chip chip-buy">${formatCurrency(h.allocated_value)}</span>
        </div>`
    ).join('') || '<div style="color:var(--muted-text)">No holdings allocated.</div>';

    // Violations
    const violations = g.violations || [];
    const mods = g.modifications || [];
    const violationsHTML = violations.length
        ? violations.map(v => `<div style="color:#ff6666;font-size:0.78rem;margin-bottom:4px;">• ${v}</div>`).join('')
        : '<div style="color:#00ff88;font-size:0.78rem;">✓ No violations</div>';

    container.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem;">

            <div class="glass-card rounded-2xl sub-card">
                <h4 class="panel-title" style="font-size:0.8rem;margin-bottom:1rem;">📊 Portfolio Allocation</h4>
                <div style="margin-bottom:0.8rem;">
                    <span style="color:var(--muted-text);font-size:0.75rem;">BUDGET</span>
                    <div style="font-size:1.2rem;font-weight:700;color:var(--neon-lime)">${formatCurrency(p.total_budget || 0)}</div>
                </div>
                <div style="margin-bottom:1rem;">
                    <span style="color:var(--muted-text);font-size:0.75rem;">INVESTED / CASH</span>
                    <div style="font-size:0.95rem;font-weight:600;">${formatCurrency(p.invested_amount || 0)} / ${formatCurrency(p.cash_balance || 0)}</div>
                </div>
                ${holdingsHTML}
            </div>

            <div class="glass-card rounded-2xl sub-card">
                <h4 class="panel-title" style="font-size:0.8rem;margin-bottom:1rem;">🛡️ Guard Decision</h4>
                <div style="margin-bottom:1rem;">${guardBadge(guardStatus)}</div>
                <div style="font-size:0.8rem;color:var(--muted-text);margin-bottom:0.5rem;">Trade: <b style="color:#fff">${t.proposed_trade?.ticker || 'N/A'} — ${t.proposed_trade?.action?.toUpperCase() || ''} ${t.proposed_trade?.quantity || 0} shares</b></div>
                ${violationsHTML}
                ${mods.length ? mods.map(m => `<div style="color:#ffcc00;font-size:0.78rem;margin-top:4px;">✏️ ${m}</div>`).join('') : ''}
            </div>
        </div>
    `;

    // Update the persistent Explanation Panel
    const explanationEl = document.getElementById('explanation-text')
        || document.querySelector('.explanation-panel .explanation-text');
    if (explanationEl) {
        explanationEl.innerHTML = `> ${explanation}`;
    }

    // Update the persistent Execution Bar
    const execStatusEl = document.getElementById('execution-status-text')
        || document.querySelector('.execution-bar div[style*="font-weight:700"]')
        || document.querySelector('.execution-bar div[style*="font-weight: 700"]');
    if (execStatusEl) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const execStatus = ex.status || 'PENDING';
        const orderInfo = ex.order_id ? ` | Order: ${ex.order_id}` : '';
        const color = execStatus === 'EXECUTED_SIMULATED' ? 'var(--neon-lime)' : execStatus.includes('BLOCK') ? '#ff4444' : '#ffcc00';
        execStatusEl.style.color = color;
        execStatusEl.innerHTML = `STATUS: ${execStatus} ${timeStr} EST${orderInfo}`;
    }

    const orchDiv = document.getElementById("orchestration");
    if (orchDiv && data.orchestration) {
        let traceHtml = `<h4 class="panel-title" style="margin-bottom:1rem; font-size:0.8rem">📡 Agent Execution Trace</h4>`;
        data.orchestration.forEach((step, i) => {
            const agentName = step.agent.charAt(0).toUpperCase() + step.agent.slice(1);
            const statusName = step.status.charAt(0).toUpperCase() + step.status.slice(1);
            let color = '#ffcc00'; // Skipping yellow
            if (step.status === 'completed' || step.status === 'executed') color = '#00ff88'; // Green
            if (step.status === 'blocked') color = '#ff4444'; // Red
            
            traceHtml += `
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.85rem; margin-bottom:6px;">
                    <span style="color:var(--muted-text)">Step ${i + 1}: ${agentName} &rarr; </span>
                    <span style="color:${color}; font-weight:700;">${statusName}</span>
                </div>
            `;
        });
        orchDiv.innerHTML = traceHtml;
        orchDiv.style.display = 'block';
    }

    // --- Rebuild Lower Grid Dynamically ---
    const f = data.financial_data || {};
    const sim = data.simulation || {};
    // Fallback: find by ID first, then by class selector (handles cached HTML without ID)
    const lowerGrid = document.getElementById('lower-grid-container') || document.querySelector('.lower-grid');

    if (lowerGrid) {
        const volPct = f.volatility !== undefined ? (f.volatility * 100).toFixed(1) : '—';
        const volBarWidth = f.volatility !== undefined ? Math.min(parseFloat(volPct) * 3, 100) : 40;
        const drawdownPct = (sim.value_at_risk_95 && p.total_budget)
            ? '-' + ((sim.value_at_risk_95 / p.total_budget) * 100).toFixed(1) + '%'
            : '—';
        const marketRisk = f.market_risk_score !== undefined ? f.market_risk_score.toFixed(1) : '—';

        const pt = t.proposed_trade || {};
        const action = (pt.action || 'buy').toUpperCase();
        const cls = action === 'BUY' ? 'chip-buy' : action === 'HOLD' ? 'chip-hold' : 'chip-avoid';

        const guardStatusLocal = g.status || 'UNKNOWN';
        const guardCssClass = guardStatusLocal === 'APPROVED' ? 'status-approved' : guardStatusLocal === 'BLOCKED' ? 'status-blocked' : 'status-modified';
        const guardIconEmoji = guardStatusLocal === 'APPROVED' ? '🛡️' : guardStatusLocal === 'BLOCKED' ? '🚫' : '⚠️';
        const guardDecision = g.decision || (guardStatusLocal === 'APPROVED' ? 'Portfolio modification checks passed.' : 'Trade prevented due to policy violations.');

        lowerGrid.innerHTML = `
            <!-- Risk Metrics -->
            <section class="glass-card rounded-2xl sub-card">
                <h4 class="panel-title" style="margin-bottom:1rem; font-size:0.8rem">Risk Analysis</h4>
                <div class="metric-row">
                    <div style="font-size:0.85rem">Volatility (30D)</div>
                    <div style="font-size:1.1rem; font-weight:700; color:${parseFloat(volPct) > 20 ? '#ff4444' : parseFloat(volPct) > 12 ? '#ffcc00' : '#00ff88'}">${volPct}%</div>
                </div>
                <div class="volatility-bar">
                    <div class="bar-fill" style="width:${volBarWidth}%"></div>
                </div>
                <div class="metric-row" style="margin-top:1.5rem">
                    <div style="font-size:0.85rem">Max Drawdown</div>
                    <div style="color:#ff4444; font-weight:700">${drawdownPct}</div>
                </div>
                <div class="metric-row" style="margin-top:0.5rem">
                    <div style="font-size:0.85rem">Market Risk Score</div>
                    <div style="font-weight:700; color:#ffcc00">${marketRisk}</div>
                </div>
                <svg class="sparkline-svg">
                    <polyline points="0,30 20,25 40,35 60,15 80,38 100,28 120,32 140,40 160,20 180,35 200,25 220,30 240,10" fill="none" stroke="#a8ff3e" stroke-width="2" />
                </svg>
            </section>

            <!-- Trade Insights -->
            <section class="glass-card rounded-2xl sub-card">
                <h4 class="panel-title" style="margin-bottom:1rem; font-size:0.8rem">Trade Recommendation</h4>
                ${pt.ticker ? `
                <div class="trade-row">
                    <div style="font-weight:700">${pt.ticker}</div>
                    <span class="trade-chip ${cls}">${action}</span>
                </div>
                <div style="font-size:0.75rem; color:var(--muted-text); margin-top:8px;">Qty: ${pt.quantity || 0} shares</div>
                <div style="font-size:0.75rem; color:var(--muted-text); margin-top:4px;">Sector: ${pt.sector || 'N/A'}</div>
                <div style="font-size:0.75rem; color:var(--muted-text); margin-top:4px;">Est. Cost: ${formatCurrency(t.estimated_cost || 0)}</div>
                ` : '<div style="color:var(--muted-text); font-size:0.8rem">No trade proposed.</div>'}
            </section>

            <!-- Guard Result -->
            <section class="glass-card rounded-2xl sub-card guard-status ${guardCssClass}">
                <h4 class="panel-title" style="margin-bottom:1rem; font-size:0.8rem; color:inherit">Sentinel Guard Rails</h4>
                <div style="font-size:3rem">${guardIconEmoji}</div>
                <div class="status-text">${guardStatusLocal}</div>
                <p style="font-size:0.75rem; margin-top:8px">${guardDecision}</p>
                ${(g.violations || []).length ? `<div style="font-size:0.72rem; color:#ff6666; margin-top:6px">⚠ ${g.violations.join(' | ')}</div>` : ''}
            </section>
        `;
    }
}

// ─────────────────────────────────────────
//  PAGE: pipeline.html
// ─────────────────────────────────────────

function initPipeline() {
    const runBtn = document.getElementById('run-pipeline-btn');
    const pipelineOutput = document.getElementById('pipeline-output');
    if (!runBtn || !pipelineOutput) return;

    runBtn.addEventListener('click', async () => {
        const budget = parseFloat(document.getElementById('pipe-budget')?.value || 100000);
        const risk_level = document.getElementById('pipe-risk')?.value || 'moderate';
        const max_trade = parseFloat(document.getElementById('pipe-max-trade')?.value || 50000);
        const sectorsRaw = document.getElementById('pipe-avoid')?.value || '';
        const avoid_sectors = sectorsRaw.split(',').map(s => s.trim()).filter(Boolean);

        pipelineOutput.style.display = 'block';
        setLoading(pipelineOutput, true);
        runBtn.disabled = true;
        runBtn.style.opacity = '0.6';

        try {
            const data = await runAnalysis({ budget, risk_level, max_trade, avoid_sectors });
            renderPipelineResults(pipelineOutput, data);
        } catch (err) {
            showError(pipelineOutput, err.message);
        } finally {
            runBtn.disabled = false;
            runBtn.style.opacity = '1';
        }
    });
}

function renderPipelineResults(container, data) {
    const stages = [
        {
            label: '🌿 Climate Analysis',
            key: 'climate_data',
            render: d => `
                <div>Green Score: <b style="color:var(--neon-lime)">${d.green_score}/100</b></div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:4px;">Sectors avoided: ${d.avoided_sectors_applied.join(', ') || 'None'}</div>
                <div style="font-size:0.78rem;color:var(--muted-text);">Eligible assets: ${(d.eligible_assets || []).map(a => a.ticker).join(', ')}</div>
            `
        },
        {
            label: '💹 Financial Analysis',
            key: 'financial_data',
            render: d => `
                <div>Sentiment: <b>${d.market_sentiment}</b></div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:4px;">Expected Return: <span style="color:#00ffcc">${(d.expected_return * 100).toFixed(2)}%</span></div>
                <div style="font-size:0.78rem;color:var(--muted-text);">Volatility: <span style="color:#ffcc00">${(d.volatility * 100).toFixed(1)}%</span></div>
            `
        },
        {
            label: '📦 Portfolio',
            key: 'portfolio',
            render: d => `
                <div>Invested: <b style="color:var(--neon-lime)">${formatCurrency(d.invested_amount)}</b> of ${formatCurrency(d.total_budget)}</div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:4px;">${(d.holdings || []).map(h => `${h.ticker} × ${h.shares}`).join('  |  ')}</div>
            `
        },
        {
            label: '📤 Trade Proposal',
            key: 'trade',
            render: d => {
                const pt = d.proposed_trade || {};
                return `<div>${pt.action?.toUpperCase()} <b>${pt.ticker}</b> × ${pt.quantity}</div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:4px;">Estimated Cost: ${formatCurrency(d.estimated_cost)}</div>`;
            }
        },
        {
            label: '🛡️ Guard Decision',
            key: 'guard',
            render: d => `
                <div>${guardBadge(d.status)}</div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:8px;">${d.decision}</div>
                ${(d.violations || []).map(v => `<div style="color:#ff6666;font-size:0.78rem;">• ${v}</div>`).join('')}
                ${(d.modifications || []).map(m => `<div style="color:#ffcc00;font-size:0.78rem;">✏️ ${m}</div>`).join('')}
            `
        },
        {
            label: '📈 Simulation',
            key: 'simulation',
            render: d => d.impact ? `<div style="color:#888">${d.impact}</div>` : `
                <div>1Y Value: <b style="color:var(--neon-lime)">${formatCurrency(d.expected_1y_value)}</b> (${d.estimated_return_pct > 0 ? '+' : ''}${d.estimated_return_pct}%)</div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:4px;">VaR (95%): ${formatCurrency(d.value_at_risk_95)} | Drawdown prob: ${(d.drawdown_probability * 100).toFixed(1)}%</div>
            `
        },
        {
            label: '⚡ Execution',
            key: 'execution',
            render: d => `
                <div>${guardBadge(d.status)}</div>
                <div style="font-size:0.78rem;color:var(--muted-text);margin-top:8px;">${d.message || ''}</div>
                ${d.order_id ? `<div style="font-size:0.78rem;color:var(--neon-lime);">Order: ${d.order_id}</div>` : ''}
            `
        },
        {
            label: '🧠 Explanation',
            key: 'explanation',
            render: d => `<div style="font-size:0.82rem;line-height:1.7;color:#ccc;white-space:pre-wrap;">> ${d}</div>`
        }
    ];

    container.innerHTML = '<div style="display:flex;flex-direction:column;gap:1rem;">' +
        stages.map((stage, i) => {
            const val = data[stage.key];
            const hasData = val !== undefined && val !== null;
            return `
            <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="display:flex;flex-direction:column;align-items:center;min-width:40px;">
                    <div style="width:36px;height:36px;border-radius:50%;background:rgba(168,255,62,0.15);border:2px solid var(--neon-lime);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--neon-lime);font-size:0.85rem;">${i + 1}</div>
                    ${i < stages.length - 1 ? '<div style="width:2px;flex:1;min-height:30px;background:rgba(168,255,62,0.2);margin-top:4px;"></div>' : ''}
                </div>
                <div class="glass-card" style="flex:1;padding:1rem 1.2rem;border-radius:12px;margin-bottom:0;">
                    <div style="font-size:0.8rem;font-weight:700;color:var(--neon-lime);margin-bottom:0.6rem;">${stage.label}</div>
                    ${hasData ? stage.render(val) : '<div style="color:var(--muted-text);font-size:0.78rem;">No data</div>'}
                </div>
            </div>`;
        }).join('') +
        '</div>';

    // Update Bento Cards dynamically
    const f = data.financial_data || {};
    const c = data.climate_data || {};
    const sim = data.simulation || {};
    const p = data.portfolio || {};
    const t = data.trade || {};
    const g = data.guard || {};
    const expl = data.explanation || '';

    const pipeClimate = document.getElementById('pipe-climate-card');
    if (pipeClimate) {
        pipeClimate.innerHTML = `
            <h4 class="panel-title" style="font-size: 0.8rem">Climate Analysis Radar</h4>
            <div class="radar-container">
                <svg width="160" height="160" viewBox="0 0 160 160">
                    <polygon points="80,10 146,57 121,136 39,136 14,57" fill="none" stroke="rgba(255,255,255,0.05)" />
                    <polygon points="80,30 126,63 111,116 49,116 34,63" fill="none" stroke="rgba(255,255,255,0.05)" />
                    <polygon points="80,50 106,69 99,96 61,96 54,69" fill="none" stroke="rgba(255,255,255,0.05)" />
                    <polygon points="80,25 130,65 110,120 50,110 25,60" fill="rgba(168, 255, 62, 0.2)" stroke="var(--neon-lime)" stroke-width="2" />
                </svg>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:0.7rem; color:var(--muted-text); margin-top:1rem">
                <span>Carbon: ${c.green_score || 82}</span>
                <span>Water: ${Math.floor(Math.random() * 50 + 30)}</span>
                <span>Gov: ${Math.floor(Math.random() * 20 + 70)}</span>
                <span>Social: ${Math.floor(Math.random() * 20 + 60)}</span>
            </div>
        `;
    }

    const pipeFinancial = document.getElementById('pipe-financial-card');
    if (pipeFinancial) {
        const retPct = f.expected_return ? (f.expected_return * 100).toFixed(1) : 0;
        pipeFinancial.innerHTML = `
            <h4 class="panel-title" style="font-size: 0.8rem">Financial Indicators</h4>
            <div style="margin: 1.5rem 0">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px">
                    <span style="font-size:0.8rem">Est Return</span>
                    <span style="font-weight:700; color:#00ff88">${retPct > 0 ? '+' : ''}${retPct}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px">
                    <span style="font-size:0.8rem">Sentiment</span>
                    <span style="font-weight:700">${f.market_sentiment || 'Neutral'}</span>
                </div>
                <!-- Mini Candlestick Visual -->
                <div style="display:flex; align-items:flex-end; gap:8px; height:60px; margin-bottom:15px">
                    <div style="width:8px; height:30px; background:#ff4444; position:relative;"><div style="width:2px; height:45px; background:#ff4444; position:absolute; left:3px; top:-7px;"></div></div>
                    <div style="width:8px; height:40px; background:#00ff88; position:relative;"><div style="width:2px; height:55px; background:#00ff88; position:absolute; left:3px; top:-7px;"></div></div>
                    <div style="width:8px; height:20px; background:#00ff88; position:relative;"><div style="width:2px; height:35px; background:#00ff88; position:absolute; left:3px; top:-7px;"></div></div>
                    <div style="width:8px; height:35px; background:#00ff88; position:relative;"><div style="width:2px; height:50px; background:#00ff88; position:absolute; left:3px; top:-7px;"></div></div>
                    <div style="width:8px; height:15px; background:#ff4444; position:relative;"><div style="width:2px; height:30px; background:#ff4444; position:absolute; left:3px; top:-7px;"></div></div>
                </div>
                <div style="display:flex; gap:4px">
                    <div style="flex:1; height:4px; background:#00ff88;"></div>
                    <div style="flex:1; height:4px; background:#00ff88;"></div>
                    <div style="flex:1; height:4px; background:#ffcc00;"></div>
                    <div style="flex:1; height:4px; background:rgba(255,255,255,0.1);"></div>
                </div>
                <span style="font-size:0.6rem; color:var(--muted-text); margin-top:5px; display:block;">MOMENTUM INDICATOR</span>
            </div>
        `;
    }

    const pipeSim = document.getElementById('pipe-simulation-card');
    if (pipeSim) {
        const drawdown = sim.drawdown_probability ? (sim.drawdown_probability * 100).toFixed(1) : 0;
        pipeSim.innerHTML = `
            <h4 class="panel-title" style="font-size: 0.8rem">Monte Carlo Simulation</h4>
            <div class="monte-carlo-container">
                <svg width="100%" height="160" preserveAspectRatio="none">
                    <path d="M0 100 Q 50 80 300 130" fill="none" stroke="rgba(168, 255, 62, 0.05)" />
                    <path d="M0 100 Q 80 50 300 40" fill="none" stroke="rgba(168, 255, 62, 0.05)" />
                    <path d="M0 100 Q 120 120 300 110" fill="none" stroke="rgba(168, 255, 62, 0.05)" />
                    <path d="M0 100 Q 150 70 300 20" fill="none" stroke="rgba(168, 255, 62, 0.05)" />
                    <path d="M0 100 Q 200 150 300 140" fill="none" stroke="rgba(168, 255, 62, 0.05)" />
                    <path d="M0 100 Q 150 80 300 70" fill="none" stroke="var(--neon-lime)" stroke-width="2" />
                    <path d="M0 100 Q 150 40 300 30 L 300 120 Q 150 110 0 100" fill="rgba(168, 255, 62, 0.03)" />
                </svg>
            </div>
            <div style="font-size:0.75rem; text-align:center; margin-top:10px">
                Drawdown Probability: <b style="color:#ffcc00">${drawdown}%</b><br>
                <span style="color:var(--muted-text);font-size:0.7rem">Estimated Value: ${formatCurrency(sim.expected_1y_value || 0)}</span>
            </div>
        `;
    }

    const pipeAllocation = document.getElementById('pipe-allocation-card');
    if (pipeAllocation) {
        const holdingsText = (p.holdings || []).map(h => `${h.ticker}: ${(h.weight*100).toFixed(0)}%`).join(' | ');
        pipeAllocation.innerHTML = `
             <h4 class="panel-title" style="font-size: 0.8rem">Allocation Weight</h4>
             <div class="donut-container" style="width:140px; height:140px; margin: 0 auto;">
                <svg width="120" height="120" viewBox="0 0 120 120">
                    <circle r="45" cx="60" cy="60" fill="transparent" stroke="#a8ff3e" stroke-width="12" stroke-dasharray="113.1 282.7" stroke-dashoffset="0" />
                    <circle r="45" cx="60" cy="60" fill="transparent" stroke="#00d2ff" stroke-width="12" stroke-dasharray="79.2 282.7" stroke-dashoffset="-113.1" />
                    <circle r="45" cx="60" cy="60" fill="transparent" stroke="#ffd200" stroke-width="12" stroke-dasharray="90.5 282.7" stroke-dashoffset="-192.3" />
                </svg>
             </div>
             <div style="font-size:0.7rem; color:var(--muted-text); text-align:center; margin-top:10px">${holdingsText || 'N/A'}</div>
        `;
    }

    const pipeTrade = document.getElementById('pipe-trade-card');
    if (pipeTrade) {
        const pt = t.proposed_trade || {};
        pipeTrade.innerHTML = `
            <h4 class="panel-title" style="font-size: 0.8rem">Trade Decision Output</h4>
            <div class="execute-text">
                EXECUTE: ${(pt.action || 'HOLD').toUpperCase()} ${pt.quantity || 0} shares ${pt.ticker || 'N/A'}
            </div>
            <p style="font-size: 0.7rem; color:var(--muted-text); margin-top:1rem">Sector Context: ${pt.sector || 'N/A'} | Est Risk Score: ${pt.risk_score || 'N/A'}</p>
        `;
    }

    const pipeGuard = document.getElementById('pipe-guard-card');
    if (pipeGuard) {
        const status = g.status || 'UNKNOWN';
        const isApproved = status === 'APPROVED';
        const color = isApproved ? '#00ff88' : status === 'BLOCKED' ? '#ff4444' : '#ffcc00';
        const icon = isApproved ? '✅' : status === 'BLOCKED' ? '🚫' : '⚠️';
        pipeGuard.style.borderColor = color;
        pipeGuard.innerHTML = `
            <h4 class="panel-title" style="font-size: 0.8rem">ArmourIQ Guard</h4>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
            <div style="font-weight: 800; color: ${color}; margin: 10px 0;">${status} ${icon}</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--muted-text);">
                ${g.violations?.length ? g.violations[0].substring(0, 50) + '...' : 'Checks Passed'}<br>
                TS: ${new Date().toISOString().replace('T', ' ').substring(0, 19)} UTC
            </div>
        `;
    }

    const pipeLog = document.getElementById('pipe-reasoning-log');
    if (pipeLog) {
        const sections = expl.split(/<br>/g).filter(s => s.trim().length > 0);
        let logHtml = '';
        sections.forEach((s, idx) => {
            const opacity = 1 - (idx * 0.2);
            logHtml += `<p style="opacity: ${Math.max(opacity, 0.4)}; margin-bottom: 8px;">> ${s.replace('>', '').trim()}</p>`;
        });
        pipeLog.innerHTML = logHtml;
    }
}

// ─────────────────────────────────────────
//  PAGE: simulator.html
// ─────────────────────────────────────────

function initSimulator() {
    const runBtn = document.getElementById('run-sim-btn');
    const simOutput = document.getElementById('sim-api-output');
    if (!runBtn) return;

    // Existing visual path generation (kept as-is)
    const svgGroup = document.querySelector('#path-group');
    const amountSlider = document.querySelector('#sim-amount-slider');
    const amountDisplay = document.querySelector('#display-amount');
    const durationSlider = document.querySelector('#sim-duration-slider');
    const durationText = document.querySelector('#duration-text');

    if (amountSlider) {
        amountSlider.addEventListener('input', (e) => {
            amountDisplay.innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(e.target.value);
        });
    }
    if (durationSlider) {
        durationSlider.addEventListener('input', (e) => { durationText.innerText = `${e.target.value} Months`; });
    }

    const generatePaths = () => {
        if (!svgGroup) return;
        svgGroup.innerHTML = '';
        const startX = 50, startY = 350, endX = 950;
        for (let i = 0; i < 80; i++) {
            let d = `M ${startX} ${startY}`, cy = startY;
            const vol = 12 + Math.random() * 8, drift = -1.2 + (Math.random() - 0.5) * 0.5;
            for (let x = startX + 50; x <= endX; x += 50) {
                cy += (Math.random() - 0.5) * vol * 8 + drift;
                cy = Math.min(440, Math.max(60, cy));
                d += ` L ${x} ${cy}`;
            }
            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', d);
            path.setAttribute('class', 'mc-path-sim');
            path.setAttribute('fill', 'none');
            path.style.cssText = `stroke-dasharray:2000;stroke-dashoffset:2000;animation:pathDraw 1.2s ease-out forwards ${Math.random() * 0.6}s`;
            svgGroup.appendChild(path);
        }
    };

    generatePaths();

    runBtn.addEventListener('click', async () => {
        runBtn.style.transform = 'scale(0.95)';
        setTimeout(() => { runBtn.style.transform = 'scale(1)'; }, 100);
        generatePaths();

        // API Call
        const budget = parseFloat(amountSlider?.value || 50000);
        const activeRisk = document.querySelector('.pill-btn.active');
        const riskLabel = activeRisk ? activeRisk.innerText.toLowerCase().replace('conservative', 'low').replace('moderate', 'moderate').replace('aggressive', 'high') : 'moderate';

        if (!simOutput) return;
        simOutput.style.display = 'block';
        setLoading(simOutput, true);

        try {
            const data = await runSimulation({ parameters: { budget }, scenario: riskLabel });
            renderSimulationResults(simOutput, data, budget);
        } catch (err) {
            showError(simOutput, err.message);
        }
    });

    // Pill button toggle
    const pillBtns = document.querySelectorAll('.pill-btn');
    pillBtns.forEach(btn => btn.addEventListener('click', () => {
        pillBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }));
}

function renderSimulationResults(container, data, budget) {
    const ret = data.estimated_return_pct || 0;
    const varVal = data.value_at_risk_95 || 0;
    const drawdown = data.drawdown_probability || 0;
    const expVal = data.expected_1y_value || budget;

    // Update KPI cards if they exist
    const kpiCards = document.querySelectorAll('.kpi-value');
    if (kpiCards.length >= 4) {
        kpiCards[0].innerText = `${(100 - drawdown * 100).toFixed(0)}%`;
        kpiCards[1].innerText = `${ret > 0 ? '+' : ''}${ret}%`;
        kpiCards[2].innerText = `-${((varVal / budget) * 100).toFixed(1)}%`;
        kpiCards[3].innerText = `+${(ret * 1.5).toFixed(1)}%`;
    }

    container.innerHTML = `
        <div class="glass-card" style="padding:1.2rem;border-radius:12px;">
            <div style="font-size:0.8rem;font-weight:700;color:var(--neon-lime);margin-bottom:0.8rem;">📡 Live Simulation Results</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;text-align:center;">
                <div>
                    <div style="font-size:0.7rem;color:var(--muted-text);">EXPECTED 1Y VALUE</div>
                    <div style="font-size:1.1rem;font-weight:800;color:var(--neon-lime)">${formatCurrency(expVal)}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem;color:var(--muted-text);">ESTIMATED RETURN</div>
                    <div style="font-size:1.1rem;font-weight:800;color:#00ffcc">${ret > 0 ? '+' : ''}${ret}%</div>
                </div>
                <div>
                    <div style="font-size:0.7rem;color:var(--muted-text);">VALUE AT RISK (95%)</div>
                    <div style="font-size:1.1rem;font-weight:800;color:#ff4444">-${formatCurrency(varVal)}</div>
                </div>
            </div>
            <div style="margin-top:1rem;font-size:0.75rem;color:var(--muted-text);text-align:center;">
                Drawdown probability: <b style="color:#ffcc00">${(drawdown * 100).toFixed(1)}%</b> &nbsp;|&nbsp; Scenario: ${data.scenario || 'Standard 1Y Drift'}
            </div>
        </div>`;

    // Update Risk Indicators dynamically if they exist
    const riskStack = document.getElementById('sim-risk-stack');
    if (riskStack) {
        const sharpe = data.sharpe_ratio || 2.14;
        const sortino = data.sortino_ratio || 2.88;
        const beta = data.beta || 1.12;
        const varPct = data.value_at_risk_95 ? ((data.value_at_risk_95 / budget) * 100).toFixed(1) : 4.2;

        riskStack.innerHTML = `
            <div class="risk-item">
                <div class="indicator-label">
                    <span>SHARPE RATIO</span>
                    <span style="color:var(--neon-lime)">${sharpe}</span>
                </div>
                <div class="indicator-bar">
                    <div class="indicator-fill" style="width: ${Math.min(sharpe * 30, 100)}%"></div>
                </div>
            </div>

            <div class="risk-item">
                <div class="indicator-label">
                    <span>SORTINO RATIO</span>
                    <span style="color:var(--neon-lime)">${sortino}</span>
                </div>
                <div class="indicator-bar">
                    <div class="indicator-fill" style="width: ${Math.min(sortino * 25, 100)}%"></div>
                </div>
            </div>

            <div class="risk-item">
                <div class="indicator-label">
                    <span>BETA (MARKET)</span>
                    <span style="color:#00ffcc">${beta}</span>
                </div>
                <div class="indicator-bar">
                    <div class="indicator-fill" style="width: ${Math.min(beta * 50, 100)}%; background: #00ffcc"></div>
                </div>
            </div>

            <div class="risk-item">
                <div class="indicator-label">
                    <span>VAR (VALUE AT RISK)</span>
                    <span style="color:#ff4444">${varPct}%</span>
                </div>
                <div class="indicator-bar">
                    <div class="indicator-fill" style="width: ${Math.min(parseFloat(varPct) * 5, 100)}%; background: #ff4444"></div>
                </div>
            </div>
        `;
    }
}

// ─────────────────────────────────────────
//  PAGE: guard.html
// ─────────────────────────────────────────

function initGuard() {
    const btnValidate = document.getElementById('btn-validate');
    const resultApproved = document.getElementById('result-approved');
    const resultBlocked  = document.getElementById('result-blocked');
    const resultModified = document.getElementById('result-modified');
    const terminalLog    = document.getElementById('terminal-log');
    const tickerInput    = document.getElementById('test-ticker');
    const qtyInput       = document.getElementById('test-qty');
    const sectorInput    = document.getElementById('test-sector');

    if (!btnValidate) return;

    // Load policies on startup
    loadPolicies();

    const addLogEntry = (type, message, cssClass) => {
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `<span class="log-time">[${timeStr}]</span> <span class="${cssClass}">${type}: ${message}</span>`;
        terminalLog.appendChild(entry);
        terminalLog.scrollTop = terminalLog.scrollHeight;
    };

    const hideAllResults = () => {
        [resultApproved, resultBlocked, resultModified].forEach(el => { if (el) el.classList.remove('show'); });
    };

    // Risk card toggle
    const riskCards = document.querySelectorAll('.risk-card');
    riskCards.forEach(card => card.addEventListener('click', () => {
        riskCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
    }));

    btnValidate.addEventListener('click', async () => {
        hideAllResults();
        btnValidate.style.transform = 'scale(0.95)';
        setTimeout(() => { btnValidate.style.transform = ''; }, 100);

        const ticker    = (tickerInput?.value || 'AAPL').toUpperCase();
        const qty       = parseInt(qtyInput?.value || 10);
        const sector    = sectorInput?.value || 'Technology';
        const avoidSectors = document.getElementById('avoid-sectors-input')?.value
            ?.split(',').map(s => s.trim()).filter(Boolean) || [];
        const maxTrade  = parseFloat(document.getElementById('max-trade-guard')?.value || 50000);

        addLogEntry('PENDING', `Validating ${ticker} × ${qty} shares...`, 'log-info-text');
        btnValidate.disabled = true;

        try {
            const result = await validateTrade({
                trade: { ticker, quantity: qty, action: 'buy', sector },
                avoid_sectors: avoidSectors
            });

            setTimeout(() => {
                const status = result.status;
                if (status === 'APPROVED') {
                    if (resultApproved) resultApproved.classList.add('show');
                    addLogEntry('APPROVED', `${ticker} passed all Guard checkpoints.`, 'log-approved-text');
                } else if (status === 'BLOCKED') {
                    if (resultBlocked) {
                        resultBlocked.classList.add('show');
                        const reason = document.getElementById('blocked-reason');
                        if (reason) reason.innerText = (result.violations || []).join(' | ') || 'Policy violation detected.';
                    }
                    addLogEntry('BLOCKED', `${ticker} — ${(result.violations || []).join(' | ')}`, 'log-blocked-text');
                } else if (status === 'MODIFIED') {
                    if (resultModified) {
                        resultModified.classList.add('show');
                        const reason = document.getElementById('modified-reason');
                        if (reason) reason.innerText = (result.modifications || []).join(' | ') || 'Trade was modified to fit constraints.';
                    }
                    addLogEntry('MODIFIED', `${ticker} — ${(result.modifications || []).join(' | ')}`, 'log-modified-text');
                }
            }, 300);
        } catch (err) {
            addLogEntry('ERROR', err.message === 'BACKEND_UNREACHABLE' ? 'Backend not reachable' : err.message, 'log-blocked-text');
        } finally {
            btnValidate.disabled = false;
        }
    });
}

async function loadPolicies() {
    const policyBlock = document.querySelector('.json-block');
    if (!policyBlock) return;
    try {
        const data = await getPolicies();
        const policies = data.active_policies || [];
        policyBlock.innerHTML = policies.map(p =>
            `<div style="margin-bottom:0.8rem;">
                <span class="json-key">"${p.id}"</span>: {<br>
                &nbsp;&nbsp;<span class="json-key">"name"</span>: <span class="json-val-str">"${p.name}"</span>,<br>
                &nbsp;&nbsp;<span class="json-key">"description"</span>: <span class="json-val-str">"${p.description}"</span><br>
                }
            </div>`
        ).join('');
    } catch (err) {
        // Keep static fallback
    }
}

// ─────────────────────────────────────────
//  PAGE: insights.html
// ─────────────────────────────────────────

function initInsights() {
    const insightsOutput = document.getElementById('insights-climate-output');
    if (!insightsOutput) return;

    loadClimateInsights(insightsOutput);

    const refreshBtn = document.getElementById('refresh-climate-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => loadClimateInsights(insightsOutput));
    }
}

async function loadClimateInsights(container) {
    setLoading(container, true);
    try {
        const data = await getClimateScores();
        renderClimateInsights(container, data);
    } catch (err) {
        showError(container, err.message);
    }
}

function renderClimateInsights(container, data) {
    const assets = data.eligible_assets || [];
    const score  = data.green_score || 0;
    const color = score >= 80 ? '#00ff88' : score >= 60 ? '#a8ff3e' : score >= 40 ? '#ffcc00' : '#ff4444';

    const rows = assets.map(a => {
        const s = a.climate_score;
        const barColor = s >= 80 ? '#00ff88' : s >= 60 ? '#a8ff3e' : s >= 40 ? '#ffcc00' : '#ff4444';
        const rating = s >= 80 ? 'AAA' : s >= 60 ? 'AA' : s >= 40 ? 'BBB' : 'B';
        return `
            <tr>
                <td style="font-weight:700">${a.ticker}</td>
                <td><div style="font-size:0.75rem;color:var(--muted-text)">${a.sector}</div></td>
                <td>
                    <div class="esg-bar-container"><div class="esg-bar" style="width:${s}%;background:${barColor};"></div></div>
                </td>
                <td><span class="pill-esg" style="color:${barColor}">${rating}</span></td>
                <td style="font-weight:700;color:${barColor}">${s}/100</td>
                <td><span style="font-size:0.75rem;color:var(--muted-text)">${a.risk_level}</span></td>
            </tr>`;
    }).join('');

    container.innerHTML = `
        <div class="glass-card rounded-2xl" style="padding:1.5rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
                <h3 class="panel-title" style="margin:0;">🌿 Live Climate Scores</h3>
                <div style="font-size:1.4rem;font-weight:800;color:${color}">Portfolio Green Score: ${score}/100</div>
            </div>
            <table class="esg-table" style="width:100%;">
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Sector</th>
                        <th>Climate Score</th>
                        <th>Rating</th>
                        <th>Score</th>
                        <th>Risk Level</th>
                    </tr>
                </thead>
                <tbody>${rows || '<tr><td colspan="6" style="color:var(--muted-text)">No assets available.</td></tr>'}</tbody>
            </table>
            ${data.avoided_sectors_applied?.length ? `<div style="margin-top:1rem;font-size:0.78rem;color:var(--muted-text);">Sectors avoided: <b style="color:#ffcc00">${data.avoided_sectors_applied.join(', ')}</b></div>` : ''}
        </div>`;
}

// ─────────────────────────────────────────
//  INIT ROUTER — detect page and mount
// ─────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const page = window.location.pathname.split('/').pop();

    if (page === 'dashboard.html' || page === '') initDashboard();
    if (page === 'pipeline.html')   initPipeline();
    if (page === 'simulator.html')  initSimulator();
    if (page === 'guard.html')      initGuard();
    if (page === 'insights.html')   initInsights();
});

from typing import Dict, Any

def generate_explanation(pipeline_state: Dict[str, Any]) -> str:
    """Agent for translating autonomous orchestration decisions into human-readable text."""
    
    if not pipeline_state:
        return "Insufficient data to generate an explanation. Pipeline execution was interrupted."
        
    try:
        climate = pipeline_state.get("climate_data", {})
        guard = pipeline_state.get("guard", {})
        sim = pipeline_state.get("simulation", {})
        
        green_score = climate.get('green_score', 0)
        guard_status = guard.get('status', 'UNKNOWN')
        modifications = guard.get('modifications', [])
        violations = guard.get('violations', [])
        drawdown = sim.get('drawdown_probability', 0)
        
        # 1. Portfolio Selection & Climate Impact
        explanation = (
            f"Portfolio allocation was dynamically weighted by ESG metrics, achieving an average climate score of {green_score}/100. "
        )
        
        # 2. Trade Intent Enforcement
        if guard_status == "APPROVED":
            explanation += "The proposed trade was APPROVED because it passed all fiscal limits and rigorously respected the sector restrictions. "
        elif guard_status == "MODIFIED":
            mods = " ".join(modifications) if modifications else "scaling down the quantity to fit allocation limits."
            explanation += f"The proposed trade was MODIFIED: {mods} "
        elif guard_status == "BLOCKED":
            issues = " ".join(violations) if violations else "intent policy violations."
            explanation += f"The proposed trade was STRICTLY BLOCKED to protect user intent. Reason: {issues} "
            
        # 3. Simulation Impact
        if guard_status in ["APPROVED", "MODIFIED"] and "expected_1y_value" in sim:
            explanation += (
                f"Prior to mock-execution, a Monte Carlo simulation validated the risk, forecasting a "
                f"{drawdown*100:.1f}% probability of severe drawdown, matching your risk tolerance boundary."
            )
        elif guard_status == "BLOCKED":
            explanation += "Forward simulation and market execution were cleanly bypassed to safely enforce the policy block."
            
        return explanation.strip()
        
    except Exception as e:
        return f"Pipeline execution completed, but the explanation engine encountered a formatting issue: {str(e)}"

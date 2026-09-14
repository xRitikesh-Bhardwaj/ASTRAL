from fastapi import APIRouter
from schemas import SimulationRequest

router = APIRouter(prefix="/api/digital-twin", tags=["Digital Twin"])

@router.post("/simulate")
def simulate_scenario(req: SimulationRequest):
    base_revenue = 124000000.0  # 12.4 Cr
    base_orders = 48250
    base_profit = 31000000.0   # 3.1 Cr
    base_customers = 14120
    
    # Calculate simulation factors
    sales_factor = 1.0 + (req.sales_growth / 100.0)
    customer_factor = 1.0 + (req.customer_growth / 100.0)
    discount_factor = 1.0 - (req.discount_rate / 100.0 * 0.4)
    mktg_roi_boost = (req.marketing_spend / 500000.0) * 0.02
    
    sim_revenue = base_revenue * sales_factor * discount_factor * (1.0 + mktg_roi_boost)
    sim_orders = int(base_orders * sales_factor * (1.0 + (req.order_volume / 100.0)))
    sim_customers = int(base_customers * customer_factor)
    
    # Profit adjusts based on discount margin and marketing cost subtraction
    raw_profit = sim_revenue * 0.25 * discount_factor - req.marketing_spend
    sim_profit = max(base_profit * 0.5, raw_profit)
    
    rev_diff_pct = round(((sim_revenue - base_revenue) / base_revenue) * 100, 1)
    orders_diff_pct = round(((sim_orders - base_orders) / base_orders) * 100, 1)
    profit_diff_pct = round(((sim_profit - base_profit) / base_profit) * 100, 1)
    cust_diff_pct = round(((sim_customers - base_customers) / base_customers) * 100, 1)
    
    return {
        "status": "success",
        "current_scenario": {
            "revenue": base_revenue,
            "formatted_revenue": "₹12.4 Cr",
            "orders": base_orders,
            "profit": base_profit,
            "formatted_profit": "₹3.1 Cr",
            "customers": base_customers
        },
        "simulated_scenario": {
            "revenue": round(sim_revenue, 2),
            "formatted_revenue": f"₹{round(sim_revenue/10000000, 2)} Cr",
            "orders": sim_orders,
            "profit": round(sim_profit, 2),
            "formatted_profit": f"₹{round(sim_profit/10000000, 2)} Cr",
            "customers": sim_customers
        },
        "impact_analysis": {
            "revenue_change_pct": f"{'+' if rev_diff_pct >= 0 else ''}{rev_diff_pct}%",
            "orders_change_pct": f"{'+' if orders_diff_pct >= 0 else ''}{orders_diff_pct}%",
            "profit_change_pct": f"{'+' if profit_diff_pct >= 0 else ''}{profit_diff_pct}%",
            "customers_change_pct": f"{'+' if cust_diff_pct >= 0 else ''}{cust_diff_pct}%"
        },
        "recommendation": (
            f"Increasing sales volume by {req.sales_growth}% alongside a {req.discount_rate}% discount rate "
            f"yields a net profit adjustment of {profit_diff_pct}%. Ensure marketing ROI maintains a 3.5x multiplier."
        )
    }

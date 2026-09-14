/* ==========================================================================
   ASTRAL PREDICTIONS JAVASCRIPT - Machine Learning Forecast Visualizations
   ========================================================================== */

document.addEventListener("DOMContentLoaded", async () => {
  // 1. Fetch Revenue Predictions
  const revData = await apiFetch("/api/predictions/revenue");
  if (revData && revData.forecast && document.getElementById("forecastChart")) {
    renderForecastChart(revData.history, revData.forecast);
    const targetEl = document.getElementById("forecast-7d-target");
    if (targetEl) targetEl.textContent = `₹${(revData.next_7_days_total / 10000000).toFixed(2)} Cr`;
  }

  // 2. Fetch Customer Churn Predictions
  const churnData = await apiFetch("/api/predictions/churn");
  if (churnData && churnData.customers) {
    document.getElementById("high-risk-count").textContent = churnData.high_risk_count || 23;
    document.getElementById("med-risk-count").textContent = churnData.medium_risk_count || 41;
    document.getElementById("low-risk-count").textContent = churnData.low_risk_count || 792;

    const churnTableBody = document.getElementById("churn-table-body");
    if (churnTableBody) {
      churnTableBody.innerHTML = churnData.customers.map(c => `
        <tr>
          <td style="font-weight: 600;">${c.name}</td>
          <td>${c.company}</td>
          <td>₹${(c.total_spent / 100000).toFixed(1)} Lakhs</td>
          <td>${c.last_order_days_ago} days ago</td>
          <td>
            <span class="badge ${c.risk_level === 'High Risk' ? 'badge-red' : c.risk_level === 'Medium Risk' ? 'badge-amber' : 'badge-green'}">
              ${c.churn_probability}% (${c.risk_level})
            </span>
          </td>
          <td style="font-size: 0.825rem; color: var(--color-navy-muted);">${c.recommended_action}</td>
        </tr>
      `).join("");
    }
  }

  // 3. Fetch Anomaly Detection Data
  const anomalyData = await apiFetch("/api/anomalies");
  if (anomalyData && anomalyData.anomalies) {
    const anomalyContainer = document.getElementById("anomaly-cards-container");
    if (anomalyContainer) {
      anomalyContainer.innerHTML = anomalyData.anomalies.map(a => `
        <div class="attention-card ${a.severity === 'High' ? 'attention-high' : a.severity === 'Positive' ? 'attention-positive' : 'attention-medium'}">
          <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <h4 style="font-size: 0.925rem;">${a.issue}</h4>
            <span class="badge ${a.severity === 'High' ? 'badge-red' : a.severity === 'Positive' ? 'badge-green' : 'badge-amber'}">${a.date}</span>
          </div>
          <p style="font-size: 0.85rem;">${a.impact}</p>
        </div>
      `).join("");
    }
  }
});

function renderForecastChart(history, forecast) {
  const ctx = document.getElementById("forecastChart").getContext("2d");
  
  const histLabels = history.map(h => h.date.substring(5));
  const histValues = history.map(h => (h.actual_revenue / 100000).toFixed(2));
  
  const foreLabels = forecast.map(f => f.date.substring(5) + " (Pred)");
  const foreValues = forecast.map(f => (f.predicted_revenue / 100000).toFixed(2));
  const lowerValues = forecast.map(f => (f.lower_bound / 100000).toFixed(2));
  const upperValues = forecast.map(f => (f.upper_bound / 100000).toFixed(2));
  
  // Combine labels
  const allLabels = [...histLabels, ...foreLabels];
  const historicalDataset = [...histValues, ...Array(forecast.length).fill(null)];
  
  // Connect historical and predicted line smoothly
  const lastHistVal = histValues[histValues.length - 1];
  const predictedDataset = [...Array(histValues.length - 1).fill(null), lastHistVal, ...foreValues];

  new Chart(ctx, {
    type: "line",
    data: {
      labels: allLabels,
      datasets: [
        {
          label: "Historical Revenue (₹ Lakhs)",
          data: historicalDataset,
          borderColor: "#2563EB",
          borderWidth: 2.5,
          tension: 0.3,
          pointRadius: 3
        },
        {
          label: "Random Forest Forecast (₹ Lakhs)",
          data: predictedDataset,
          borderColor: "#006B50",
          borderDash: [5, 5],
          borderWidth: 2.5,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: "#006B50"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { font: { family: "Inter", size: 12 } } },
        tooltip: {
          callbacks: { label: (ctx) => `${ctx.dataset.label}: ₹${ctx.raw} Lakhs` }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: "#F1F5F9" } }
      }
    }
  });
}

/* ==========================================================================
   ASTRAL DASHBOARD JAVASCRIPT - Business Overview Data & Chart.js Rendering
   ========================================================================== */

let revenueChartInstance = null;

document.addEventListener("DOMContentLoaded", async () => {
  await loadDashboardData();
  setupFilterTabs();
});

async function loadDashboardData() {
  const data = await apiFetch("/api/dashboard");
  if (!data) return;

  // 1. Populate Business Health Card
  const healthScoreEl = document.getElementById("health-score-val");
  const healthStatusEl = document.getElementById("health-status-val");
  if (healthScoreEl) healthScoreEl.textContent = `${data.business_health.score} / 100`;
  if (healthStatusEl) healthStatusEl.textContent = data.business_health.status;

  // 2. Populate KPI Cards
  if (data.kpis) {
    document.getElementById("kpi-revenue-val").textContent = data.kpis.revenue.value;
    document.getElementById("kpi-revenue-change").textContent = `↑ ${data.kpis.revenue.change} vs last period`;
    
    document.getElementById("kpi-orders-val").textContent = data.kpis.orders.value;
    document.getElementById("kpi-orders-change").textContent = `↑ ${data.kpis.orders.change} vs last period`;
    
    document.getElementById("kpi-customers-val").textContent = data.kpis.customers.value;
    document.getElementById("kpi-customers-change").textContent = `↑ ${data.kpis.customers.change} vs last period`;
    
    document.getElementById("kpi-profit-val").textContent = data.kpis.profit.value;
    document.getElementById("kpi-profit-change").textContent = `↑ ${data.kpis.profit.change} vs last period`;
  }

  // 3. Render Revenue Trend Chart with Chart.js
  if (data.chart_data && document.getElementById("revenueTrendChart")) {
    renderRevenueChart(data.chart_data.labels, data.chart_data.values);
  }

  // 3b. Render Category Doughnut Chart if present
  if (document.getElementById("categoryDoughnutChart")) {
    renderCategoryDoughnutChart();
  }

  // 4. Daily AI Summary
  const summaryEl = document.getElementById("today-summary-text");
  if (summaryEl) summaryEl.textContent = data.daily_summary;

  // 5. Key Insights List
  const insightsListEl = document.getElementById("insights-list-container");
  if (insightsListEl && data.key_insights) {
    insightsListEl.innerHTML = data.key_insights.map(item => `
      <div class="insight-item">
        <span class="badge ${item.type === 'positive' ? 'badge-green' : item.type === 'warning' ? 'badge-amber' : 'badge-blue'}">Insight</span>
        <span style="color: var(--color-navy-dark); font-weight: 500;">${item.text}</span>
      </div>
    `).join("");
  }

  // 6. Attention Required Items
  const attentionContainer = document.getElementById("attention-items-container");
  if (attentionContainer && data.attention_required) {
    attentionContainer.innerHTML = data.attention_required.map(item => {
      const severityClass = item.severity === 'High' ? 'attention-high' : item.severity === 'Medium' ? 'attention-medium' : 'attention-positive';
      const badgeClass = item.severity === 'High' ? 'badge-red' : item.severity === 'Medium' ? 'badge-amber' : 'badge-green';
      return `
        <div class="attention-card ${severityClass}">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <h4 style="font-size: 0.95rem;">${item.title}</h4>
            <span class="badge ${badgeClass}">${item.badge}</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--color-navy-muted);">${item.desc}</p>
        </div>
      `;
    }).join("");
  }
}

function renderRevenueChart(labels, values) {
  const ctx = document.getElementById("revenueTrendChart").getContext("2d");
  if (revenueChartInstance) revenueChartInstance.destroy();

  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(0, 107, 80, 0.25)");
  gradient.addColorStop(1, "rgba(0, 107, 80, 0.0)");

  revenueChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Revenue (₹ Lakhs)",
        data: values,
        borderColor: "#006B50",
        borderWidth: 2.5,
        backgroundColor: gradient,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: "#006B50",
        pointRadius: 3,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#101828",
          padding: 12,
          titleFont: { family: "Inter", size: 13 },
          bodyFont: { family: "Inter", size: 12 },
          displayColors: false,
          callbacks: {
            label: (context) => `Revenue: ₹${context.raw} Lakhs`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: "Inter", size: 11 }, color: "#64748B" }
        },
        y: {
          grid: { color: "#F1F5F9" },
          ticks: { font: { family: "Inter", size: 11 }, color: "#64748B" }
        }
      }
    }
  });
}

function setupFilterTabs() {
  const tabBtns = document.querySelectorAll(".timeframe-tab");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      // Simulate data slice based on tab
      loadDashboardData();
    });
  });
}

function renderCategoryDoughnutChart() {
  const canvas = document.getElementById("categoryDoughnutChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Electronics & Software", "Home & Living", "Fashion & Apparel", "Beauty & Personal Care", "Others"],
      datasets: [{
        data: [42, 18, 15, 13, 12],
        backgroundColor: ["#006B50", "#3B82F6", "#8B5CF6", "#F97316", "#94A3B8"],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "75%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0F172A",
          padding: 10,
          callbacks: {
            label: (context) => `${context.label}: ${context.raw}%`
          }
        }
      }
    }
  });
}


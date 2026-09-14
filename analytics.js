/* ==========================================================================
   ASTRAL ANALYTICS JAVASCRIPT - Multi-dimensional Data Visualizations
   ========================================================================== */

document.addEventListener("DOMContentLoaded", async () => {
  const data = await apiFetch("/api/analytics");
  if (!data) return;

  // 1. Render Category Doughnut Chart
  if (data.category_distribution && document.getElementById("categoryDoughnutChart")) {
    const ctx = document.getElementById("categoryDoughnutChart").getContext("2d");
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: Object.keys(data.category_distribution),
        datasets: [{
          data: Object.values(data.category_distribution),
          backgroundColor: ["#006B50", "#2563EB", "#059669", "#D97706", "#64748B"],
          borderWidth: 2,
          borderColor: "#FFFFFF"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { font: { family: "Inter", size: 12 } } }
        },
        cutout: "68%"
      }
    });
  }

  // 2. Render Order Trend Bar Chart
  if (data.order_trend && document.getElementById("orderTrendChart")) {
    const ctx = document.getElementById("orderTrendChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.order_trend.labels,
        datasets: [{
          label: "Daily Order Volume",
          data: data.order_trend.values,
          backgroundColor: "#2563EB",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: "#F1F5F9" } }
        }
      }
    });
  }

  // 3. Populate Top Products Table
  const tableBody = document.getElementById("products-table-body");
  if (tableBody && data.top_products) {
    tableBody.innerHTML = data.top_products.map(prod => `
      <tr>
        <td style="font-weight: 600;">${prod.name}</td>
        <td><span class="badge badge-blue">${prod.category}</span></td>
        <td>${prod.sales_count.toLocaleString()} units</td>
        <td style="font-weight: 700; color: var(--color-navy-dark);">₹${(prod.revenue_generated / 10000000).toFixed(2)} Cr</td>
        <td><span class="badge badge-green">+${prod.growth_rate}% YoY</span></td>
      </tr>
    `).join("");
  }
});

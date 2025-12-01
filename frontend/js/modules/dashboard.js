let salesChartInstance = null;
let itemsChartInstance = null;

async function fetchReports() {
  const [salesData, menuData] = await Promise.all([
    api("/reports/daily-sales"),
    api("/menus"),
  ]);

  let totalSales = 0;
  let totalOrders = 0;

  const safeSalesData = Array.isArray(salesData) ? salesData : [];

  if (safeSalesData.length > 0) {
    totalSales = safeSalesData.reduce(
      (acc, curr) => acc + (curr.total_sales || 0),
      0
    );
    totalOrders = safeSalesData.length;
  }

  updateDashboardStats(totalSales, totalOrders);

  renderCharts(safeSalesData, Array.isArray(menuData) ? menuData : []);
}

function updateDashboardStats(sales, orders) {
  const salesEl = document.getElementById("dash-total-sales");
  const ordersEl = document.getElementById("dash-total-orders");

  if (salesEl) salesEl.innerText = formatCurrency(sales);
  if (ordersEl) ordersEl.innerText = orders;
}

function renderCharts(salesData, menuData) {
  const ctxSales = document.getElementById("salesChart");
  const ctxItems = document.getElementById("itemsChart");

  if (salesChartInstance) salesChartInstance.destroy();
  if (itemsChartInstance) itemsChartInstance.destroy();

  const salesLabels = salesData.map((_, index) => `Order #${index + 1}`);
  const salesValues = salesData.map((item) => item.total_sales);

  if (ctxSales) {
    salesChartInstance = new Chart(ctxSales, {
      type: "line",
      data: {
        labels: salesLabels,
        datasets: [
          {
            label: "Transaction Value",
            data: salesValues,
            borderColor: "#0f172a", // Primary Color
            backgroundColor: "rgba(15, 23, 42, 0.1)",
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointBackgroundColor: "#fff",
            pointBorderColor: "#0f172a",
            pointRadius: 5,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (context) {
                return formatCurrency(context.parsed.y);
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return "Rp " + value / 1000 + "k";
              },
            },
            grid: { borderDash: [2, 4] },
          },
          x: {
            display: salesData.length > 0,
          },
        },
      },
    });
  }

  const sortedMenus = [...menuData]
    .sort((a, b) => b.price - a.price)
    .slice(0, 10);

  const menuLabels = sortedMenus.map((m) => m.name);
  const menuPrices = sortedMenus.map((m) => m.price);

  if (ctxItems) {
    itemsChartInstance = new Chart(ctxItems, {
      type: "bar",
      data: {
        labels: menuLabels,
        datasets: [
          {
            label: "Price",
            data: menuPrices,
            backgroundColor: "#334155",
            borderRadius: 4,
            hoverBackgroundColor: "#0f172a",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (context) {
                return formatCurrency(context.parsed.y);
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { display: false },
          },
          x: {
            grid: { display: false },
            ticks: {
              autoSkip: false,
              maxRotation: 45,
              minRotation: 45,
              font: { size: 10 },
            },
          },
        },
      },
    });
  }
}

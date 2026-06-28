const API = "http://localhost:8000";

let equityChart = null;
let currentAccount = 1;

// -----------------------------
// INIT
// -----------------------------
async function init() {

    await loadAccount();
    await loadAnalytics(currentAccount);
}

// -----------------------------
// ACCOUNT DATA
// -----------------------------
async function loadAccount() {

    try {

        const res = await fetch(`${API}/account`);
        const data = await res.json();

        console.log("ACCOUNT RESPONSE:", data);

        setText("balance", formatMoney(data.balance));
        setText("equity", formatMoney(data.equity));
        setText("margin", formatMoney(data.free_margin));

    } catch (err) {

        console.log("Account error:", err);

        setText("balance", "Error");
        setText("equity", "Error");
        setText("margin", "Error");
    }
}

// -----------------------------
// ANALYTICS
// -----------------------------
async function loadAnalytics(accountId) {

    try {

        const res = await fetch(`${API}/analytics?account_id=${accountId}`);
        const data = await res.json();

        console.log("ANALYTICS RESPONSE:", data);

        setText("totalTrades", data.total_trades);
        setText("totalProfit", formatMoney(data.total_profit));
        setText("winRate", `${data.win_rate}%`);
        setText("profitFactor", data.profit_factor);

        updateChart(data.equity_curve);

    } catch (err) {

        console.log("Analytics error:", err);
    }
}

// -----------------------------
// SAFE TEXT UPDATE
// -----------------------------
function setText(id, value) {

    const el = document.getElementById(id);

    if (!el) {
        console.log("Missing element:", id);
        return;
    }

    el.textContent = value ?? "0";
}

// -----------------------------
// MONEY FORMAT
// -----------------------------
function formatMoney(value) {

    if (value === null || value === undefined) return "$0.00";
    return `$${Number(value).toFixed(2)}`;
}

// -----------------------------
// EQUITY CHART
// -----------------------------
function updateChart(curve) {

    if (!curve || curve.length === 0) return;

    const labels = curve.map((_, i) => i + 1);
    const values = curve.map(p => p.equity);

    const ctx = document.getElementById("equityChart")?.getContext("2d");

    if (!ctx) return;

    if (equityChart) {

        equityChart.data.labels = labels;
        equityChart.data.datasets[0].data = values;
        equityChart.update();
        return;
    }

    equityChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Equity Curve",
                data: values,
                borderWidth: 2,
                tension: 0.3
            }]
        }
    });
}

// -----------------------------
// START APP
// -----------------------------
document.addEventListener("DOMContentLoaded", init);
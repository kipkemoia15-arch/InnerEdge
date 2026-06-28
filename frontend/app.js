const API = "http://127.0.0.1:8000";

let equityChart = null;

// --------------------
// Account
// --------------------

async function loadAccount() {
    try {
        const res = await fetch(`${API}/account`);
        const data = await res.json();

        document.getElementById("balance").textContent =
            `$${Number(data.balance).toFixed(2)}`;

        document.getElementById("equity").textContent =
            `$${Number(data.equity).toFixed(2)}`;

        document.getElementById("margin").textContent =
            `$${Number(data.free_margin).toFixed(2)}`;

    } catch (err) {
        console.error("Account error:", err);
    }
}

// --------------------
// Analytics
// --------------------

async function loadAnalytics() {

    try {

        const res = await fetch(`${API}/analytics`);
        const data = await res.json();

        document.getElementById("totalTrades").textContent =
            data.total_trades;

        document.getElementById("totalProfit").textContent =
            `$${Number(data.total_profit).toFixed(2)}`;

        loadChart(data);

    } catch (err) {

        console.error("Analytics error:", err);

    }

}

// --------------------
// Positions
// --------------------

async function loadPositions() {

    try {

        const res = await fetch(`${API}/positions`);
        const positions = await res.json();

        const tbody = document.getElementById("positions");

        tbody.innerHTML = "";

        if (positions.length === 0) {

            tbody.innerHTML =
                `<tr>
                    <td colspan="3">No open positions</td>
                </tr>`;

            return;
        }

        positions.forEach(position => {

            tbody.innerHTML += `
                <tr>
                    <td>${position.symbol}</td>
                    <td>${position.volume}</td>
                    <td>${Number(position.profit).toFixed(2)}</td>
                </tr>
            `;

        });

    } catch (err) {

        console.error("Positions error:", err);

    }

}

// --------------------
// Chart
// --------------------

function loadChart(data) {

    const labels = data.equity_curve.map(p => p.time);
    const values = data.equity_curve.map(p => p.equity);

    const ctx = document
        .getElementById("equityChart")
        .getContext("2d");

    if (equityChart) {
        equityChart.destroy();
    }

    equityChart = new Chart(ctx, {

        type: "line",

        data: {

            labels,

            datasets: [

                {

                    label: "Equity Curve",

                    data: values,

                    borderColor: "lime",

                    tension: 0.3,

                    fill: false

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}

// --------------------
// Refresh
// --------------------

async function refreshDashboard() {

    await Promise.all([
        loadAccount(),
        loadAnalytics(),
        loadPositions()
    ]);

}

refreshDashboard();

// Refresh every 10 seconds
setInterval(refreshDashboard, 10000);
async function loadChart() {
    try {
        const res = await fetch(`${API}/analytics`);
        const data = await res.json();

        const labels = data.equity_curve.map(p => p.time);
        const values = data.equity_curve.map(p => p.equity);

        const ctx = document.getElementById("equityChart").getContext("2d");

        if (equityChart) equityChart.destroy();

        equityChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Equity Curve",
                    data: values,
                    borderColor: "lime",
                    tension: 0.3
                }]
            }
        });

    } catch (err) {
        console.log("Chart error:", err);
    }
}
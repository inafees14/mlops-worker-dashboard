let eventsChart = null;
let workerChart = null;
let productChart = null;
let idlePieChart = null;

/* ---------------- Filters ---------------- */

function buildQuery() {
    const hours = document.getElementById("hours").value;
    const worker = document.getElementById("worker").value;

    let params = [];
    if (hours) params.push(`hours=${hours}`);
    if (worker) params.push(`worker_id=${worker}`);

    return params.length ? "?" + params.join("&") : "";
}

/* ---------------- KPI ---------------- */

async function loadSummary() {
    const res = await fetch("/api/metrics/summary" + buildQuery());
    const data = await res.json();

    document.getElementById("total_events").innerText = data.total_events;
    document.getElementById("total_products").innerText = data.total_products;
    document.getElementById("active_events").innerText = data.active_events;
    document.getElementById("idle_events").innerText = data.idle_events;
}

/* ---------------- Business + Ops Analytics ---------------- */

async function loadAnalytics() {
    const res = await fetch("/api/metrics/analytics" + buildQuery());
    const data = await res.json();

    document.getElementById("kpi_throughput").innerText =
        data.throughput_units_per_hour;
    
        document.getElementById("kpi_rate").innerText =
        data.production_rate ?? "-";
    document.getElementById("kpi_active").innerText =
        data.total_active_minutes?.toFixed(1) ?? "-";

    document.getElementById("kpi_idle").innerText =
        data.total_idle_minutes?.toFixed(1) ?? "-";

    document.getElementById("kpi_idle_ratio").innerText =
        data.idle_ratio_percent + "%";

    document.getElementById("kpi_yield").innerText =
        data.yield_units_per_event;

    document.getElementById("kpi_bottleneck").innerText =
        data.bottleneck_worker || "-";

    document.getElementById("kpi_utilization").innerText =
        data.avg_utilization + "%";

    document.getElementById("kpi_mtbf").innerText =
        data.mtbf_minutes + " min";

    document.getElementById("kpi_mttr").innerText =
        data.mttr_minutes + " min";
}

/* ---------------- Workers ---------------- */

async function loadWorkers() {
    const res = await fetch("/api/metrics/workers" + buildQuery());
    const data = await res.json();

    const tbody = document.querySelector("#workers_table tbody");
    tbody.innerHTML = "";

    const workerDropdown = document.getElementById("worker");
    const seen = new Set();

    data.forEach(w => {
        tbody.innerHTML += `
            <tr>
                <td>${w.worker_id}</td>
                <td>${w.events}</td>
                <td>${w.products}</td>
                <td>${w.productivity_score}</td>
            </tr>
        `;
        seen.add(w.worker_id);
    });

    if (workerDropdown.options.length <= 1) {
        [...seen].forEach(w => {
            const opt = document.createElement("option");
            opt.value = w;
            opt.text = w;
            workerDropdown.appendChild(opt);
        });
    }

    updateWorkerChart(data);
}

/* ---------------- Timeseries ---------------- */

async function loadTimeseries() {
    const res = await fetch("/api/metrics/timeseries" + buildQuery());
    const data = await res.json();

    const labels = data.map(d => d.minute);
    const events = data.map(d => d.events);
    const products = data.map(d => d.products);

    // Events chart
    if (!eventsChart) {
        eventsChart = new Chart(
            document.getElementById("eventsChart"),
            {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "Events",
                        data: events,
                        tension: 0.3
                    }]
                }
            }
        );
    } else {
        eventsChart.data.labels = labels;
        eventsChart.data.datasets[0].data = events;
        eventsChart.update();
    }

    // Product chart
    if (!productChart) {
        productChart = new Chart(
            document.getElementById("productChart"),
            {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "Products",
                        data: products,
                        tension: 0.3
                    }]
                }
            }
        );
    } else {
        productChart.data.labels = labels;
        productChart.data.datasets[0].data = products;
        productChart.update();
    }

    // Idle vs Active Pie
    const totalIdle = data.reduce((a, b) => a + (b.events === 0 ? 1 : 0), 0);
    const totalActive = data.length - totalIdle;

    if (!idlePieChart) {
        idlePieChart = new Chart(
            document.getElementById("idlePie"),
            {
                type: "pie",
                data: {
                    labels: ["Active", "Idle"],
                    datasets: [{
                        data: [totalActive, totalIdle]
                    }]
                }
            }
        );
    } else {
        idlePieChart.data.datasets[0].data = [totalActive, totalIdle];
        idlePieChart.update();
    }
}

/* ---------------- Worker Chart ---------------- */

function updateWorkerChart(data) {
    const labels = data.map(w => w.worker_id);
    const scores = data.map(w => w.productivity_score);

    if (!workerChart) {
        workerChart = new Chart(
            document.getElementById("workerChart"),
            {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Productivity Score",
                        data: scores
                    }]
                }
            }
        );
    } else {
        workerChart.data.labels = labels;
        workerChart.data.datasets[0].data = scores;
        workerChart.update();
    }
}


/* ---------------- Workstations ---------------- */

async function loadStations() {
    const res = await fetch("/api/metrics/workstations" + buildQuery());
    const data = await res.json();

    const tbody = document.querySelector("#stations_table tbody");
    tbody.innerHTML = "";

    data.forEach(s => {
        tbody.innerHTML += `
            <tr>
                <td>${s.workstation_id}</td>
                <td>${s.events}</td>
                <td>${s.products}</td>
            </tr>
        `;
    });
}

/** Filters outputs */
function updateFilterInfo() {
    const h = document.getElementById("hours").value || "All time";
    const w = document.getElementById("worker").value || "All workers";

    document.getElementById("filterInfo").innerText =
        `Showing data for: ${h} | ${w}`;
}


/* ---------------- Refresh ---------------- */

async function refreshDashboard() {
    await loadSummary();
    await loadAnalytics();
    await loadWorkers();
    await loadStations();
    await loadTimeseries();
    await updateFilterInfo();
}

document.getElementById("refreshBtn").onclick = refreshDashboard;
refreshDashboard();
setInterval(refreshDashboard, 5000);

document.getElementById("lastUpdated").innerText =
    "Last Updated: " + new Date().toLocaleString();


document.addEventListener("DOMContentLoaded", function () {

    // ================= Expense Doughnut Chart =================

    const expenseCanvas = document.getElementById("expenseChart");

    if (expenseCanvas && typeof Chart !== "undefined") {
        new Chart(expenseCanvas, {
            type: "doughnut",
            data: {
                labels: dashboardLabels,
                datasets: [{
                    data: dashboardValues,
                    backgroundColor: [
                        "#2563eb",
                        "#22c55e",
                        "#ef4444",
                        "#f59e0b",
                        "#8b5cf6",
                        "#06b6d4",
                        "#ec4899",
                        "#14b8a6"
                    ],
                    borderWidth: 0,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "68%",
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

    // ================= Monthly Trend =================

    const monthlyCanvas = document.getElementById("monthlyChart");

    if (monthlyCanvas && typeof Chart !== "undefined") {
        new Chart(monthlyCanvas, {
            type: "line",
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: "Expenses",
                    data: monthlyValues,
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37,99,235,0.12)",
                    fill: true,
                    tension: 0.45,
                    pointRadius: 5,
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    }

    // ================= Asset Allocation =================

    const allocationCanvas = document.getElementById("allocationChart");

    if (
        allocationCanvas &&
        typeof Chart !== "undefined" &&
        typeof allocationLabels !== "undefined" &&
        typeof allocationValues !== "undefined"
    ) {
        new Chart(allocationCanvas, {
            type: "doughnut",
            data: {
                labels: allocationLabels,
                datasets: [{
                    data: allocationValues,
                    backgroundColor: [
                        "#2563eb",
                        "#22c55e",
                        "#f59e0b",
                        "#ef4444",
                        "#8b5cf6",
                        "#06b6d4"
                    ],
                    borderWidth: 0,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 1,
                cutout: "65%",
                radius: "65%",
                plugins: {
                    legend: {
                        position: "bottom"
                    },
                    title: {
                        display: true,
                        text: "Investment Distribution",
                        font: {
                            size: 18
                        }
                    }
                }
            }
        });
    }

    // ================= Portfolio Performance =================

    const portfolioCanvas = document.getElementById("portfolioChart");

    if (
        portfolioCanvas &&
        typeof Chart !== "undefined" &&
        typeof portfolioMonths !== "undefined" &&
        typeof portfolioValues !== "undefined"
    ) {
        new Chart(portfolioCanvas, {
            type: "line",
            data: {
                labels: portfolioMonths,
                datasets: [{
                    label: "Portfolio Value",
                    data: portfolioValues,
                    borderColor: "#16a34a",
                    backgroundColor: "rgba(22,163,74,0.15)",
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // ================= Last 6 Months Expense =================

    const last6Canvas = document.getElementById("last6Chart");

    if (
        last6Canvas &&
        typeof Chart !== "undefined" &&
        typeof last6Labels !== "undefined" &&
        typeof last6Values !== "undefined"
    ) {
        new Chart(last6Canvas, {
            type: "bar",
            data: {
                labels: last6Labels,
                datasets: [{
                    label: "Last 6 Months Expense",
                    data: last6Values,
                    backgroundColor: "#3b82f6",
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // ================= Income vs Expense =================

    const incomeExpenseCanvas = document.getElementById("incomeExpenseChart");

    if (
        incomeExpenseCanvas &&
        typeof Chart !== "undefined" &&
        typeof incomeExpense !== "undefined"
    ) {
        new Chart(incomeExpenseCanvas, {
            type: "pie",
            data: {
                labels: ["Income", "Expense"],
                datasets: [{
                    data: incomeExpense,
                    backgroundColor: [
                        "#22c55e",
                        "#ef4444"
                    ],
                    borderWidth: 0,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

});
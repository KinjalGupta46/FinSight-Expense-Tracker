// =========================
// Monthly Expense Line Chart
// =========================

const expenseCtx = document.getElementById("expenseChart");

if (expenseCtx) {

    new Chart(expenseCtx, {

        type: "line",

        data: {

            labels: chartLabels,

            datasets: [{

                label: "Monthly Expense",

                data: chartValues,

                borderWidth: 3,

                tension: 0.4,

                fill: true

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: true

                }

            }

        }

    });

}


// =========================
// Expense Category Pie Chart
// =========================

const categoryCtx = document.getElementById("categoryChart");

if (categoryCtx) {

    new Chart(categoryCtx, {

        type: "pie",

        data: {

            labels: categoryLabels,

            datasets: [{

                data: categoryValues

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}
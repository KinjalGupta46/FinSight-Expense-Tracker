document.addEventListener("DOMContentLoaded", function () {

    // Expense Distribution

    const expenseChart = document.getElementById("expenseChart");

    if (expenseChart && typeof Chart !== "undefined") {

        new Chart(expenseChart, {

            type: "doughnut",

            data: {

                labels: ["Food", "Travel", "Shopping", "Bills", "Others"],

                datasets: [{

                    data: [30, 20, 18, 22, 10],

                    backgroundColor: [

                        "#2563eb",

                        "#16a34a",

                        "#f59e0b",

                        "#ef4444",

                        "#8b5cf6"

                    ],

                    borderWidth: 0

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

    // Cash Flow

    const cashFlowChart = document.getElementById("cashFlowChart");

    if (cashFlowChart && typeof Chart !== "undefined") {

        new Chart(cashFlowChart, {

            type: "line",

            data: {

                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],

                datasets: [

                    {

                        label: "Income",

                        data: [50000, 52000, 51000, 55000, 56000, 60000],

                        borderColor: "#16a34a",

                        backgroundColor: "transparent",

                        tension: 0.4,

                        fill: false

                    },

                    {

                        label: "Expense",

                        data: [30000, 34000, 31000, 36000, 35000, 38000],

                        borderColor: "#ef4444",

                        backgroundColor: "transparent",

                        tension: 0.4,

                        fill: false

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "top"

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

});
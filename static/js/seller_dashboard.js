
    document.addEventListener("DOMContentLoaded", function () {
        const ctx = document.getElementById('salesChart').getContext('2d');

        // Grab dynamic data from the view
        const chartLabels = JSON.parse(document.getElementById('chartLabels').textContent);
        const chartValues = JSON.parse(document.getElementById('chartValues').textContent);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,  // Dynamic labels
                datasets: [{
                    label: 'Total Sales',
                    data: chartValues,  // Dynamic values
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    borderWidth: 2,
                    pointRadius: 5,
                    pointBackgroundColor: '#4CAF50',
                    pointHoverRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#E5E7EB'
                        }
                    }
                }
            }
        });
    });

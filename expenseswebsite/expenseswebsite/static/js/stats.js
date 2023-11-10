const renderChart = (data, labels) => {
    const ctx = document.getElementById('myChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months expenses',
                data: data,
                borderWidth: 1,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',   // Red
                    'rgba(54, 162, 235, 0.2)',   // Blue
                    'rgba(255, 206, 86, 0.2)',   // Yellow
                    'rgba(75, 192, 192, 0.2)',   // Green
                    'rgba(153, 102, 255, 0.2)',  // Purple
                    'rgba(255, 159, 64, 0.2)'    // Orange
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',  // Red
                    'rgba(54, 162, 235, 1)',  // Blue
                    'rgba(255, 206, 86, 1)',  // Yellow
                    'rgba(75, 192, 192, 1)',  // Green
                    'rgba(153, 102, 255, 1)', // Purple
                    'rgba(255, 159, 64, 1)'   // Orange
                ]
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Expenses per Category'
                }
            }
        }
    });
};

const getChartData = () => {
    fetch('/expense_category_summary')
        .then((response) => response.json())
        .then((data) => {
            const labels = Object.keys(data.expense_category_data);
            const values = Object.values(data.expense_category_data);
            renderChart(values, labels);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
};

window.addEventListener('load', getChartData);

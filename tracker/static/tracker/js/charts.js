// Data arrays passed from Django context
const incomeCategoryNames = JSON.parse('{{ income_category_names|safe|escapejs }}');
const incomeCategoryTotals = JSON.parse('{{ income_category_totals|safe|escapejs }}');
const categoryNames = JSON.parse('{{ category_names|safe|escapejs }}');
const categoryTotals = JSON.parse('{{ category_totals|safe|escapejs }}');

// Initialize the pie chart with default data (Expense)
const pieChart = new Chart(document.getElementById("pieChart"), {
    type: 'pie',
    data: {
        labels: categoryNames,  // Default to Expense categories
        datasets: [{
            label: 'Expense Breakdown',
            data: categoryTotals,
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#FF5733'],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ₱' + tooltipItem.raw;
                    }
                }
            }
        }
    }
});

// Function to switch between Income and Expense charts
function switchChart(type) {
    const title = document.getElementById("pieChartTitle");  // Reference to the pie chart header

    if (type === 'income') {
        pieChart.data.labels = incomeCategoryNames;  // Update labels for Income
        pieChart.data.datasets[0].data = incomeCategoryTotals;  // Update data for Income
        pieChart.data.datasets[0].label = 'Income Breakdown';  // Update the label for the chart
        title.textContent = 'Income Breakdown by Category';  // Change the header to 'Income'
    } else {
        pieChart.data.labels = categoryNames;  // Default to Expense categories
        pieChart.data.datasets[0].data = categoryTotals;  // Default to Expense data
        pieChart.data.datasets[0].label = 'Expense Breakdown';  // Default label for Expense
        title.textContent = 'Expense Breakdown by Category';  // Keep the header as 'Expense'
    }

    pieChart.update();  // Re-render the chart with updated data
}


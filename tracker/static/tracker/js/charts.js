// Pie Chart for Expense Breakdown by Category
var categoryNames = JSON.parse(document.getElementById('category_names').textContent);
var categoryTotals = JSON.parse(document.getElementById('category_totals').textContent);

// Pie chart for Income Breakdown by Category
var incomeCategoryNames = JSON.parse(document.getElementById('income_category_names').textContent);
var incomeCategoryTotals = JSON.parse(document.getElementById('income_category_totals').textContent);

var ctxPie = document.getElementById('pieChart').getContext('2d');

// Create Expense Pie Chart initially
var pieChart = new Chart(ctxPie, {
    type: 'doughnut',
    data: {
        labels: categoryNames,
        datasets: [{
            label: 'Expense Breakdown',
            data: categoryTotals,
            backgroundColor: ['#FF6347', '#FF9F40', '#FFCD47', '#FF6A6A', '#FFC0CB'],
            borderColor: 'transparent',
        }]
    },
    options: {
        cutout: '50%', // size of the hole in the center


        plugins: {
            legend: {
                position: 'left',
                labels: {
                    font: {
                        size: 18 // controls legend text size
                    }
                }
            }
        }
    }
});


// Bar Chart for Monthly Income vs Expenses
var monthlyIncome = JSON.parse(document.getElementById('income').textContent);
var monthlyExpense = JSON.parse(document.getElementById('expense').textContent);

var ctxBar = document.getElementById('barChart').getContext('2d');
var barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: ['Income', 'Expense'],
        datasets: [{
            label: 'Amount',
            data: [monthlyIncome, monthlyExpense],
            backgroundColor: ['#4CAF50', '#F44336'],
            borderColor: ['#388E3C', '#D32F2F'],
            borderWidth: 0
        }]
    },
    options: {
        cutout: '20%',
        plugins: {
            legend: {
                position: 'left' // ← Puts the legend on the left side
            }
        },
        scales: {
            y: {
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    
            
        
    }
});

// Function to switch charts
function switchChart(chartType) {
    const title = document.getElementById("pieChartTitle");

    if (chartType === 'income') {
        pieChart.data.labels = incomeCategoryNames;
        pieChart.data.datasets[0].data = incomeCategoryTotals;
        pieChart.data.datasets[0].label = 'Income Breakdown';
        title.textContent = 'Income Breakdown by Category';
        pieChart.update();
    } else if (chartType === 'expense') {
        pieChart.data.labels = categoryNames;
        pieChart.data.datasets[0].data = categoryTotals;
        pieChart.data.datasets[0].label = 'Expense Breakdown';
        title.textContent = 'Expense Breakdown by Category';
        pieChart.update();
    }
}


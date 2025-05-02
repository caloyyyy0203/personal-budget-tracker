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
            backgroundColor: ['#0D4AAC', '#EC1824', '#FEBD01', '#FF5448', '#005EF6', '#FFD14D'],
            borderColor: 'transparent',
            borderRadius: [50, 50] 
        }]
    },
    options: {
        cutout: '50%', // size of the hole in the center


        plugins: {
            legend: {
                position: 'left',
                labels: {
                    font: {
                        size: 14 // controls legend text size
                    },
                    boxWidth: 20,     // Width of the legend box
                    boxHeight: 20,    // Height of the legend box (effective in recent versions)
                    pointStyle: 'circle', // You can also try 'rectRounded', 'triangle', etc.
                    usePointStyle: true
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
            backgroundColor: ['#0D4AAC', '#EC1824'],
            borderWidth: 0,
            borderRadius: [50, 50] 
        }]
    },
    options: {
        cutout: '20%',
        borderRadius: '100%',
        plugins: {
            legend: {
                position: 'left',
                labels: {
                    font: {
                        size: 14 // controls legend text size
                    },
                    boxWidth: 20,     // Width of the legend box
                    boxHeight: 20,    // Height of the legend box (effective in recent versions)
                    pointStyle: 'circle', // You can also try 'rectRounded', 'triangle', etc.
                    usePointStyle: true
                }
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
        pieChart.data.datasets = [{
            label: 'Income Breakdown',
            data: incomeCategoryTotals,
            backgroundColor: ['#0D4AAC', '#EC1824', '#FEBD01',],
            borderColor: 'transparent',
        }];
        title.textContent = 'Income Breakdown by Category';
    } else {
        pieChart.data.labels = categoryNames;
        pieChart.data.datasets = [{
            label: 'Expense Breakdown',
            data: categoryTotals,
            backgroundColor: [ '#FF5448', '#005EF6', '#FFD14D'],
            borderColor: 'transparent',
        }];
        title.textContent = 'Expense Breakdown by Category';
    }

    pieChart.update();
}



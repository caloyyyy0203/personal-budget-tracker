// Pie Chart for Expense Breakdown by Category
var categoryNames = JSON.parse(document.getElementById('category_names').textContent);
var categoryTotals = JSON.parse(document.getElementById('category_totals').textContent);

var ctxPie = document.getElementById('pieChart').getContext('2d');
var pieChart = new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: categoryNames,
        datasets: [{
            label: 'Expense Breakdown',
            data: categoryTotals,
            backgroundColor: ['#FF6347', '#FF9F40', '#FFCD47', '#FF6A6A', '#FFC0CB'],
            borderColor: '#fff',
            borderWidth: 1
        }]
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
            borderWidth: 1
        }]
    }
});

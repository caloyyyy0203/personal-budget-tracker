from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from .models import Entry, Category
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
import csv
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def add_entry(request):
    # Get month and year from the GET parameters (if any)
    month = request.GET.get('month')
    year = request.GET.get('year')

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        # If month and year are provided, set initial date
        initial_data = {}
        if month and year:
            initial_data['date'] = datetime(int(year), int(month), 1)  # First day of that month
        form = EntryForm(initial=initial_data)

    return render(request, 'tracker/add_entry.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = EntryForm(instance=entry)

    return render(request, 'tracker/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def dashboard(request):
    today = timezone.now()

    # Get selected month/year from GET parameters
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    if selected_month and selected_year:
        month = int(selected_month)
        year = int(selected_year)
    else:
        month = today.month
        year = today.year

    # Filter entries based on selected month and year
    entries = Entry.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total_income = entries.filter(entry_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = entries.filter(entry_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # Summarize expenses by category
    expense_categories = entries.filter(entry_type='Expense')
    expense_by_category = expense_categories.values('category__name').annotate(total_amount=Sum('amount'))

    category_names = [entry['category__name'] for entry in expense_by_category]
    category_totals = [entry['total_amount'] for entry in expense_by_category]

    # Prepare months manually
    months = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ]
    current_year = today.year
    start_year = 2020  # Adjust based on your needs
    categories = Category.objects.all() 

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'entries': entries,
        'today': today,
        'month': month,
        'year': year,
        'months': months,  # Pass months list
        'year_range': range(start_year, current_year + 1),  # Pass year range
        'category_names': category_names,
        'category_totals': category_totals,
        'income': total_income,
        'expense': total_expense,
        'categories': categories,
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def export_csv(request):
    entries = Entry.objects.filter(user=request.user)

    # Create the HttpResponse with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Type', 'Category', 'Amount'])

    for entry in entries:
        # Check if category exists and set it to 'Unknown' if None
        category_name = entry.category.name if entry.category else 'Unknown'
        writer.writerow([entry.date, entry.title, entry.entry_type, category_name, entry.amount])

    return response

def landing_page(request):
    return render(request, 'tracker/landing_page.html')

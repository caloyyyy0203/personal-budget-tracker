from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from .models import Entry, Category, Budget
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
import csv
import calendar
from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse


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
        initial_data = {}
        if month and year:
            initial_data['date'] = datetime(int(year), int(month), 1)
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
def delete_entry(request, id):
    entry = get_object_or_404(Entry, id=id)
    
    if request.method == "POST":
        entry.delete()
        return redirect('dashboard')  
    
    return redirect('dashboard')

@login_required
def set_budget(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('budget')

        try:
            amount = Decimal(amount)
        except (ValueError, TypeError):
            return render(request, 'tracker/modals/set_budget.html', {'error': 'Invalid amount', 'categories': Category.objects.all()})

        category = Category.objects.get(id=category_id)

        current_budget = Budget.objects.filter(user=request.user, category=category).first()

        if current_budget:
            current_budget.amount = amount
            current_budget.save()
        else:
            Budget.objects.create(
                user=request.user,
                category=category,
                month=timezone.now().month,
                year=timezone.now().year,
                amount=amount
            )

        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'tracker/modals/set_budget_modal.html', {'categories': categories})

@login_required
def get_budget_for_category(request, category_id):
    current_budget = Budget.objects.filter(user=request.user, category_id=category_id).first()
    
    if current_budget:
        return JsonResponse({'amount': str(current_budget.amount)})
    else:
        return JsonResponse({'amount': 0})

@login_required
def dashboard(request):
    today = timezone.now()
    now = datetime.now()

    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    if selected_month and selected_year:
        month = int(selected_month)
        year = int(selected_year)
    else:
        month = today.month
        year = today.year

    month_name = calendar.month_name[month]

    entries = Entry.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total_income = entries.filter(entry_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = entries.filter(entry_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    expense_categories = entries.filter(entry_type='Expense')
    expense_by_category = expense_categories.values('category__name').annotate(total_amount=Sum('amount'))

    income_categories = entries.filter(entry_type='Income')
    income_by_category = income_categories.values('category__name').annotate(total_amount=Sum('amount'))

    income_category_names = [entry['category__name'] for entry in income_by_category]
    income_category_totals = [entry['total_amount'] for entry in income_by_category]

    exceeded_categories = []
    for category in expense_by_category:
        category_name = category['category__name']
        total_expense_in_category = category['total_amount']
        
        budget = Budget.objects.filter(user=request.user, category__name=category_name, month=month, year=year).first()
        
        if budget and total_expense_in_category > budget.amount:
            exceeded_categories.append({
                'category_name': category_name,
                'budget': budget.amount,
                'total_expense': total_expense_in_category
            })

    category_names = [entry['category__name'] for entry in expense_by_category]
    category_totals = [entry['total_amount'] for entry in expense_by_category]

    months = [
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]
    current_year = today.year
    start_year = 2020
    categories = Category.objects.all() 
    current_budget = Budget.objects.filter(user=request.user, month=month, year=year).first()

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'entries': entries,
        'today': today,
        'month': month,
        'year': year,
        'month_name': month_name,
        'months': months,
        'year_range': range(start_year, current_year + 1),
        'category_names': category_names,
        'category_totals': category_totals,
        'income': total_income,
        'expense': total_expense,
        'income_category_names': income_category_names, 
        'income_category_totals': income_category_totals,  
        'categories': categories,
        'now': now,
        'current_budget': current_budget,
        'exceeded_categories': exceeded_categories,
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def export_csv(request):
    entries = Entry.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Type', 'Category', 'Amount'])

    for entry in entries:
        category_name = entry.category.name if entry.category else 'Unknown'
        writer.writerow([entry.date, entry.title, entry.entry_type, category_name, entry.amount])

    return response

def landing_page(request):
    return render(request, 'tracker/landing_page.html')

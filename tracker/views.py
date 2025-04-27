from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from .models import Entry
from django.db.models import Sum
from django.utils import timezone


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
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')  # We'll build dashboard later
    else:
        form = EntryForm()
    return render(request, 'tracker/add_entry.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    # Get the entry object for the logged-in user
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_list')  # Redirect to a list or a detail view
    else:
        form = EntryForm(instance=entry)

    return render(request, 'tracker/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def dashboard(request):
    today = timezone.now()

    # Filter only the current logged-in user's entries for the current month
    current_month_entries = Entry.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year
    )

    total_income = current_month_entries.filter(entry_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = current_month_entries.filter(entry_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'entries': current_month_entries,
        'today': today,  # so we can display month/year
    }

    return render(request, 'tracker/dashboard.html', context)

def landing_page(request):
    return render(request, 'tracker/landing_page.html')
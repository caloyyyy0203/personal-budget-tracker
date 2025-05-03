from django.test import TestCase
from django.contrib.auth.models import User
from .models import Budget, Category, Entry
from django.utils import timezone
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
# from tracker.models import Entry, Category, Budget
# from django.utils import timezone
from decimal import Decimal
class TrackerViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.client.login(username='tester', password='pass123')

        self.category = Category.objects.create(name='Food', type='Expense', user=self.user)
        self.entry = Entry.objects.create(
            user=self.user,
            title='Groceries',
            entry_type='Expense',
            amount=50.00,
            date=timezone.now(),
            category=self.category
        )

    def test_register_get(self):
        self.client.logout()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_add_entry_get(self):
        response = self.client.get(reverse('add_entry'))
        # print(response.content) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/add_entry.html')

    def test_add_entry_post(self):
    # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Post data to create a new entry
        response = self.client.post(reverse('add_entry'), {
            'title': 'Freelance Work',
            'entry_type': 'Income',
            'amount': 1200,
            'date': timezone.now().date(),
            'category': ''  # Leave blank for income (category is disabled)
        })

        # Should redirect after successful save
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(title='Freelance Work', user=self.user).exists())

    def test_edit_entry_get(self):  
        response = self.client.get(reverse('edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/edit_entry.html')

    def test_edit_entry_post(self):
        # self.client.login(username='testuser', password='testpassword')  # Log in the test user

        # Create an entry to edit
        entry = Entry.objects.create(
            title='Old Title',
            entry_type='Expense',
            amount=50,
            date=timezone.now(),
            category=self.category,
            user=self.user
        )

        # POST updated data
        response = self.client.post(reverse('edit_entry', args=[entry.id]), {
            'title': 'Updated Title',
            'entry_type': 'Expense',
            'amount': 75,
            'date': timezone.now(),
            'category': self.category.id
        })

        # Reload entry from DB
        entry.refresh_from_db()

        # Assertions
        self.assertEqual(response.status_code, 302)
        self.assertEqual(entry.title, 'Updated Title')
        self.assertEqual(entry.amount, 75)


    def test_delete_entry(self):
        response = self.client.post(reverse('delete_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/dashboard.html')
        self.assertContains(response, 'Groceries')

    def test_set_budget_post(self):
        response = self.client.post(reverse('set_budget'), {
            'category': self.category.id,
            'budget': '150.00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Budget.objects.filter(category=self.category).exists())

    def test_get_budget_for_category(self):
        Budget.objects.create(user=self.user, category=self.category, month=timezone.now().month, year=timezone.now().year, amount=Decimal('100.00'))
        response = self.client.get(reverse('get_budget_for_category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'amount': '100.00'})

    def test_export_csv(self):
        response = self.client.get(reverse('export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Groceries', response.content.decode())

    def test_category_list(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Food')

    def test_category_create_post(self):
        response = self.client.post(reverse('category_create'), {
            'name': 'Work',
            'type': 'Income'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Work').exists())

    def test_category_update_post(self):
        response = self.client.post(reverse('category_update', args=[self.category.id]), {
            'name': 'Food Updated',
            'type': 'Expense'
        })
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Food Updated')

    def test_category_delete(self):
        response = self.client.post(reverse('delete_entry', args=[self.entry.id]))  # delete entry so category can be deleted
        response = self.client.get(reverse('category_delete', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_get_categories_income(self):
        Category.objects.create(name='Salary', type='Income', user=self.user)
        response = self.client.get(reverse('get_categories') + '?entry_type=Income')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Salary', response.content.decode())

    def test_get_categories_expense(self):
        response = self.client.get(reverse('get_categories') + '?entry_type=Expense')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Food', response.content.decode())
        
class BudgetAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.income_category = Category.objects.create(
            user=self.user,
            name='Salary',
            type=Category.INCOME,
            is_default=True
        )
        self.expense_category = Category.objects.create(
            user=self.user,
            name='Groceries',
            type=Category.EXPENSE
        )

    def test_create_budget(self):
        budget = Budget.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=1000.00
        )
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        self.assertEqual(budget.month, current_month)
        self.assertEqual(budget.year, current_year)
        self.assertEqual(str(budget), f"{self.user.username} - {self.expense_category.name} - {current_month}/{current_year} - $1000.00")

    def test_create_category_defaults(self):
        category = Category.objects.create(
            name="Unassigned",
            type=Category.EXPENSE,
            is_default=True
        )
        self.assertIsNone(category.user)
        self.assertEqual(str(category), "Unassigned (Expense)")

    def test_create_entry_with_defaults(self):
        entry = Entry.objects.create(
            user=self.user,
            title="Paycheck",
            amount=2000.00,
            entry_type='Income',
            category=self.income_category
        )
        self.assertEqual(entry.title, "Paycheck")
        self.assertEqual(entry.amount, 2000.00)
        self.assertEqual(entry.entry_type, 'Income')
        self.assertEqual(entry.category.name, 'Salary')
        self.assertEqual(str(entry), "Paycheck - 2000.00 (Income)")
        self.assertEqual(entry.date.date(), timezone.now().date())  # test default date
        # print("entry.date:", entry.date, type(entry.date))
        # print("timezone.now().date():", timezone.now().date(), type(timezone.now().date()))

    def test_entry_with_notes(self):
        entry = Entry.objects.create(
            user=self.user,
            title="Dinner",
            amount=50.00,
            entry_type='Expense',
            category=self.expense_category,
            notes="Dinner with friends"
        )
        self.assertEqual(entry.notes, "Dinner with friends")

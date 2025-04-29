from django import forms
from .models import Entry, Category

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'amount', 'date', 'entry_type', 'category', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'entry_type': forms.Select(attrs={'placeholder': 'Select type'}),
            'category': forms.Select(attrs={'placeholder': 'Select category'}),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Optional notes...',
                'rows': 3
            }),
        }

    # 1️⃣ Field validation: Amount must be positive
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        return amount

    # 2️⃣ Field validation: Title must not be empty
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError('Title cannot be empty.')
        return title

    # 3️⃣ Form-wide validation: Category required if entry is an Expense
    def clean(self):
        cleaned_data = super().clean()
        entry_type = cleaned_data.get('entry_type')
        category = cleaned_data.get('category')

        if entry_type == 'Expense' and category is None:
            raise forms.ValidationError('Category is required for expenses.')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
            'type': forms.Select(attrs={'placeholder': 'Select type'}),
        }

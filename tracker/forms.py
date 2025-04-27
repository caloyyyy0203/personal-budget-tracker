from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'amount', 'date', 'entry_type', 'category', 'notes']

    # 1️⃣ Field validation: Amount must be positive
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        return amount

    # 2️⃣ Field validation: Title must not be empty (extra safe)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError('Title cannot be empty.')
        return title

    # 3️⃣ Form-wide validation: If entry is an Expense,category is required
    def clean(self):
        cleaned_data = super().clean()
        entry_type = cleaned_data.get('entry_type')
        category = cleaned_data.get('category')

        if entry_type == 'Expense' and category is None:
            raise forms.ValidationError('Category is required for expenses.')


from django import forms
from .models import *

class add_port(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = 'name',


class add_comp(forms.ModelForm):
    class Meta:
        model = Composed_of
        fields = ['portfolio_id','ticker','num_shares']

    def clean_num_shares(self):
        num_shares = self.cleaned_data.get('num_shares')
        if num_shares < 1:
            raise forms.ValidationError("Number of shares must be 1 or greater.")
        return num_shares

    def save(self, commit=True):
        instance = super().save(commit=False)
        ticker = instance.ticker
        num_shares = instance.num_shares
        existing_entry = Composed_of.objects.filter(ticker=ticker).first()

        if existing_entry:
            existing_entry.num_shares += num_shares
            if commit:
                existing_entry.save()
            return existing_entry
        else:
            if commit:
                instance.save()
            return instance
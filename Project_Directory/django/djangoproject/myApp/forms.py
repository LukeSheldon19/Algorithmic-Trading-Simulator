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
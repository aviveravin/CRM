from django.forms import ModelForm
from app.models import CRM

class CRMForm(ModelForm):
    class Meta:
        model = CRM
        fields = ['role' , 'description' , 'place' , 'phone']
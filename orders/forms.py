from django import forms

class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
              ("0", 'False'),
              ("1", 'True'),
          ])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
          choices=[
              ("0", 'False'),
              ("1", 'True'),
          ])
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(
            attrs={'class': 'form-control',
                  'type': 'date'
                  }))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(
            attrs={'class': 'form-control',
                  'type': 'date'
                  }))
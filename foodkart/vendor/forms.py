from django import forms
from accounts.models import Account


class VendorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class': 'form-control',}))    
       
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Re-enter Password',
        'class': 'form-control',}))
    
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'enter name',
        'class': 'form-control',})) 

    
     
    class Meta:
        model = Account
        fields = ['email','vendor_name', 'first_name', 'last_name','phone_number','password']


     

    def __init__(self, *args,**kwargs):
        super(VendorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'enter e-mail' 
        self.fields['vendor_name'].widget.attrs['placeholder'] = 'enter vendor name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'enter last Name'        
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter phone number' 
 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 


    def clean(self):
        cleaned_data = super(VendorRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )


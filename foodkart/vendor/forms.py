from django import forms
from accounts.models import Account
from store.validators import validate_image
from . models import Vendor, OpeningHour


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

    # vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[validate_image])
     
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
        
        if len(password) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long.")

            
    def clean_phone_number(self):
        phone_number= self.cleaned_data.get('phone_number')
        
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be valid")
        
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contail only digits")



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name',]
        
    def __init__(self, *args,**kwargs):                    
        super(VendorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
                
                

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day','from_hour', 'to_hour', 'is_closed']
        
    # def __init__(self, *args,**kwargs):                    
    #     super(OpeningHourForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'

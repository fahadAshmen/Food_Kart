from django import forms
from . models import Account, UserProfile, VendorProfile
from store.validators import validate_image
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class': 'form-control',}))    
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Re-enter Password',
        'class': 'form-control',}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email', 'phone_number','password']

    def __init__(self, *args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name' 
        self.fields['email'].widget.attrs['placeholder'] = 'Enter E-mail' 
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone Number' 
 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
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
        
        if len(phone_number)<10:
            raise forms.ValidationError("Phone number must be valid")
        
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contail only digits")
        

            
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...', 'required': 'required'}))
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':"Image files only"}, widget=forms.FileInput, validators=[validate_image])
        
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'country', 'state', 'city', 'pin_code','latitude','longitude']
        
    def __init__(self, *args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

            

class VendorProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...', 'required': 'required'}))
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':"Image files only"}, widget=forms.FileInput, validators=[validate_image])
        
    class Meta:
        model = VendorProfile
        fields = ['profile_picture', 'address', 'country', 'state', 'city', 'pin_code']
        
    def __init__(self, *args,**kwargs):
        super(VendorProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            
class UserForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number']
    
    def __init__(self, *args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
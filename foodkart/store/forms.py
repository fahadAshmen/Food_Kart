from django import forms
from . models import Product
from store.validators import validate_image


class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[validate_image]) 
        
    class Meta:
        model = Product
        fields = ('category','food_title','description','price','image','is_veg')
        labels ={
            'category':'Category',
            'food_title':'Name of Food',
            'description':'Description',
            'price':'Price',
            'image':'Image',
            'is_veg':'is_veg',
            
        }
        
    def __str__(self):
        return self.food_title







from store.models import Category
from django import forms

class CategoryForm(forms.ModelForm):


    class Meta:
        model=Category
        fields = ("category_name","description")
        labels ={
           'category_name' : 'Category Name',
           'description' : 'Description',
        }

    def __init__(self, *args,**kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs['placeholder'] = 'enter category name' 
        self.fields['description'].widget.attrs['placeholder'] = 'enter description'
        
 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
from django import forms
from . models import User, Profile, Book

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs= {"placeholder" : "Enter Password"}))
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs= {"placeholder" : "Confirm Password"}))
    class Meta:
        model = User
        fields = ["first_name" , "last_name" ,"user_type", "email" , "password"]

    def __init__(self , *args , **kwargs):
        super(RegistrationForm, self).__init__(*args , **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name" #applying the text in the placeholder
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
    
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'  #applying the bootstrap class form-control on all the fields

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
        
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match.")
        
    #     return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])  # Hash the password
    #     if commit:
    #         user.save()
    #     return user




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'country', 'state']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "category", "image","price", "description"]

from django import forms

from .models import Book, Profile, User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "user_type", "email", "password")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs[
            "placeholder"
        ] = "Enter First Name"  # applying the text in the placeholder
        self.fields["last_name"].widget.attrs[
            "placeholder"
        ] = "Enter Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email"

        for field in self.fields:
            self.fields[field].widget.attrs[
                "class"
            ] = "form-control"  # applying the bootstrap class form-control on all the fields


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone_number", "address", "country", "state")


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "category",
            "image",
            "price",
            "description",
        )  # using tuple instead of list for memory optimization

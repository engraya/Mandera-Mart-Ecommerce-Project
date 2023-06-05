from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Product



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control unicase-form-control text-input ", "type" : "text", "id" : "exampleInputEmail2", "placeholder" : "Enter your Username",})
        self.fields["email"].widget.attrs.update({"class": "form-control unicase-form-control text-input", "type" : "email","id" : "exampleInputEmail1", "placeholder" : "Enter your Email",})
        self.fields["password1"].widget.attrs.update({"class": "form-control unicase-form-control text-input",  "type" : "password", "id" : "exampleInputEmail1", "placeholder" : "Enter your Password", })
        self.fields["password2"].widget.attrs.update({"class": "form-control unicase-form-control text-input", "type" : "password", "id" : "exampleInputEmail1", "placeholder" : "Confirm your Password",})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserLoginForm(AuthenticationForm):
       def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["username"].widget.attrs.update({"class": "form-control unicase-form-control text-input", "type" : "text", "placeholder" : "Enter your Username", "id" : "exampleInputEmail1"})
            self.fields["password"].widget.attrs.update({"class": "form-control unicase-form-control text-input", "type" : "password", "placeholder" : "Enter your Password", "id" : "exampleInputPassword1"})


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter your Product Name", })
        self.fields["category"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Choose your Product category",})
        self.fields["price"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter your Product price",})
        self.fields["digital"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter your Product Type",})
        self.fields["description"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter Product Description",})
        self.fields["image"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Choose your Product Image",})

    class Meta:
        model = Product
        fields = '__all__'





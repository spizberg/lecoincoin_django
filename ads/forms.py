from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250)


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=(forms.TextInput(attrs={"name": "username", "class": "form-control",
                                                              "placeholder": "Username", "required": ""})))

    password = forms.CharField(max_length=100,
                               widget=(forms.PasswordInput(attrs={"name": "password", "class": "form-control",
                                                                  "placeholder": "Password", "required": ""})))


class SaleAdCreationForm(forms.Form):
    title = forms.CharField(max_length=100, widget=(forms.TextInput(attrs={"name": "title", "class": "form-control",
                                                                           "placeholder": "Title", "required": ""})))

    price = forms.DecimalField(min_value=0,
                               widget=(forms.NumberInput(attrs={"name": "price", "class": "form-control",
                                                                "step": "0.01", "placeholder": "10,00", "required": ""})))

    description = forms.CharField(widget=(forms.Textarea(attrs={"name": "description", "class": "form-control",
                                                                "placeholder": "Description", "required": ""})))

    illustrations = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                           "class": "form-control form-control-sm"}))

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from punkweb_bb.models import BoardProfile, Category, Post, Shout, Subcategory, Thread
from punkweb_bb.widgets import BBCodeEditorWidget


class LoginForm(AuthenticationForm):
    """
    Override the default AuthenticationForm to add CSS classes to the
    username and password fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "pw-input fluid"}
        )
        self.fields["password"].widget.attrs.update({"class": "pw-input fluid"})


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "pw-input fluid"}
        )
        self.fields["password1"].widget.attrs.update({"class": "pw-input fluid"})
        self.fields["password2"].widget.attrs.update({"class": "pw-input fluid"})


class BoardProfileModelForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = (
            "image",
            "signature",
        )
        widgets = {
            "signature": BBCodeEditorWidget(),
        }


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",
            "order",
        )
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True, "class": "pw-input"}),
            "order": forms.TextInput(
                attrs={"class": "pw-input", "min": "0", "type": "number"}
            ),
        }


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
        labels = {
            "content": "",
        }
        widgets = {
            "content": BBCodeEditorWidget(),
        }


class ShoutModelForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ("content",)


class SubcategoryModelForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = (
            "name",
            "description",
            "order",
            "staff_post_only",
        )
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True, "class": "pw-input"}),
            "description": BBCodeEditorWidget(),
            "order": forms.TextInput(
                attrs={"class": "pw-input", "min": "0", "type": "number"}
            ),
        }


class ThreadModelForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
        )
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True, "class": "pw-input"}),
            "content": BBCodeEditorWidget(),
        }

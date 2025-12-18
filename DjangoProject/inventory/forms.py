from django import forms
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Remove available_quantity from form — it will be set automatically
        fields = [
            "title",
            "subtitle",
            "authors",
            "isbn",
            "publisher",
            "category",
            "description",
            "total_quantity",
            "price",
            "cover_image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def save(self, commit=True):
        book = super().save(commit=False)
        # Automatically set available_quantity if adding a new book
        if not book.pk:  # New book
            book.available_quantity = book.total_quantity
        if commit:
            book.save()
        return book


class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ("STAFF", "Staff"),
        ("USER", "User"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data["role"]
            Profile.objects.create(user=user, role=role)

            # Create Member for non-staff users
            # membership_id must be unique; we can derive from user id
            if role == "USER":
                # Example ID: M0001, M0002 etc.
                membership_id = f"M{user.id:04d}"
                # If you want the Member active immediately:
                Member.objects.create(
                    user=user, membership_id=membership_id, active=True
                )
        return user
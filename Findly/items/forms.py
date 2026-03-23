from django import forms

from .models import Item, ItemVerification, ClaimRequest


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ItemForm(forms.ModelForm):
    uploaded_images = forms.ImageField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        label="Item Images (Select multiple)"
    )

    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "status",
            "location",
            "city",
            "category",
            "date_happened",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date_happened": forms.DateInput(attrs={"type": "date"}),
        }


class ItemVerificationForm(forms.ModelForm):

    class Meta:
        model = ItemVerification
        fields = [
            "description",
            "receipt",
            "image1",
            "image2",
            "image3",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ClaimRequestForm(forms.ModelForm):

    class Meta:
        model = ClaimRequest
        fields = [
            "message",
            "proof_image",
            "proof_document",
        ]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe why this is your item (any details you remember)."}),
        }

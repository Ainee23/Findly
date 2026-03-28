from django import forms

from .models import Item, ItemVerification, ClaimRequest


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ItemForm(forms.ModelForm):
    uploaded_images = MultipleFileField(
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

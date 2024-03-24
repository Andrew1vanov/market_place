from django import forms
class CouponApplyForm(forms.From):
    code = forms.CharField()
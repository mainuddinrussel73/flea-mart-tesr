from django.contrib.auth.models import User
from django import forms
from User.models import SellItemInfo,Comments

class SellItemInfoForm(forms.ModelForm):
    class Meta():
        model = SellItemInfo
        fields = ('item_name','item_type','item_location','item_exprice','item_usetime','item_reason','item_pic')


class CommentsForm(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ('content','username')

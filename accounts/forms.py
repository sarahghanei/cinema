from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from accounts.models import Payment, Profile


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'transaction_code']
        # or: exclude = ['profile', 'transaction_time']

    def clean_transaction_code(self):
        code = self.cleaned_data.get('transaction_code')
        try:
            # should be in format: bank-<amount>-<TOKEN>#
            # e.g. bank-30000-UHB454GRH73BDYU#
            assert code.startswith('bank-')
            assert code.endswith('#')
            int(code.split('-')[
                    1])  # if we can't convert part 2 of receipt to int try will catch the error and pass it to the except part.
        except:
            # in the top, asserts will raise AssertionError so we got them and put them in except and raise ValidationError
            raise ValidationError('قالب رسید تراکنش معتبر نیست')
        return code

    def clean_amount(self):
        # this func will return cleaned amount or raise ValidationError
        # we access entered amount from request, they are available in payment form.
        amount = self.cleaned_data.get('amount')
        if amount % 1000 != 0:
            raise ValidationError('مبلغ پرداختی باید ضریبی از هزار تومان باشد')
        return amount

    def clean(self):
        # final clean check
        # this function overrides clean func in the super class, so we have to mention it.
        super().clean()
        code = self.cleaned_data.get('transaction_code')
        amount = self.cleaned_data.get('amount')
        if code is not None and amount is not None:
            if int(code.split('-')[1]) != amount:
                raise ValidationError('رسید و مبلغ تراکنش هم‌خوانی ندارند')
        # if there is no problem in cleaning, clean function will do nothing and just pass the code.


class MyUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'email']

    password = None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'address', 'profile_image']

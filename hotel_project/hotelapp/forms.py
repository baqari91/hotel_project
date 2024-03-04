from django.forms import ModelForm
from .models import Booking

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out", "guests"]

    def clean(self):
        super(BookingForm, self).clean()
        check_in = self.cleaned_data.get("check_in")
        check_out = self.cleaned_data.get("check_out")
        guests = self.cleaned_data.get("guests")
        if check_in and check_out and check_in > check_out:
            self._errors['check_in'] = self.error_class(['Check in date must be before check out date.'])
        if guests and guests < 1:
            self._errors['guests'] = self.error_class(['Number of guests must be 1 or more.'])
        return self.cleaned_data



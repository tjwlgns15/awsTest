from datetime import datetime, timedelta
from django import forms
from django.utils import timezone

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'placeholder': 'ex) ' + datetime.now().strftime('%Y-%m-%d')})
    )
    end_date = forms.DateField(label='End Date')

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            # 'datetime.datetime' 객체로 변환
            start_datetime = datetime.combine(start_date, datetime.min.time())

            # 데이터베이스 시간대에서 Django 시간대로 변환
            start_datetime = timezone.make_naive(timezone.make_aware(start_datetime, timezone.utc))

            # 9시간 추가
            start_datetime += timedelta(hours=9) - timedelta(days=1)

        return start_datetime

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date:
            # 'datetime.datetime' 객체로 변환
            end_datetime = datetime.combine(end_date, datetime.min.time())

            # 데이터베이스 시간대에서 Django 시간대로 변환
            end_datetime = timezone.make_naive(timezone.make_aware(end_datetime, timezone.utc))

            # 9시간 추가
            end_datetime += timedelta(hours=9) - timedelta(days=1)

        return end_datetime

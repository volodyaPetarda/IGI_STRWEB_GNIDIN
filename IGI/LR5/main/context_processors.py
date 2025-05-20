import datetime
import calendar
from django.utils import timezone
from django.conf import settings
import pytz


import datetime
import calendar
from django.utils import timezone
from django.conf import settings
import pytz

def time_info_context(request):
    user_timezone_str = request.COOKIES.get('django_timezone', 'Europe/Minsk')
    try:
        user_tz = pytz.timezone(user_timezone_str)
    except pytz.UnknownTimeZoneError:
        user_timezone_str = 'Europe/Minsk'
        try:
            user_tz = pytz.timezone(user_timezone_str)
        except pytz.UnknownTimeZoneError:
            user_timezone_str = 'UTC'
            user_tz = pytz.timezone(user_timezone_str)


    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc, user_tz)

    today_for_calendar = now_local.date()
    cal_display_year = today_for_calendar.year
    cal_display_month = today_for_calendar.month
    text_cal = calendar.TextCalendar(calendar.MONDAY)
    month_calendar_str = text_cal.formatmonth(cal_display_year, cal_display_month)
    current_calendar_month_name = datetime.date(cal_display_year, cal_display_month, 1).strftime('%B %Y')

    return {
        'current_time_utc_ctx': now_utc,
        'current_time_local_ctx': now_local,
        'user_timezone_str_ctx': user_timezone_str,
        'text_calendar_str_ctx': month_calendar_str,
        'current_calendar_month_name_ctx': current_calendar_month_name,
    }

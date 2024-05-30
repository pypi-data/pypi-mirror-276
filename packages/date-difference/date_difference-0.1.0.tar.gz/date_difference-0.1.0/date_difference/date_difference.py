# date_difference/date_difference.py
from datetime import datetime

def calculate_date_difference(date1_str, date2_str, date_format="%Y-%m-%d %H:%M:%S"):
    """
    حساب الفرق بين تاريخين معطاة كنصوص.
    
    :param date1_str: التاريخ الأول كنص
    :param date2_str: التاريخ الثاني كنص
    :param date_format: تنسيق التاريخ الافتراضي هو "%Y-%m-%d %H:%M:%S"
    :return: عدد الأيام، الساعات، الدقائق والثواني بين التاريخين
    """
    # تحويل النصوص المدخلة إلى كائنات datetime
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    
    # حساب الفرق بين التاريخين
    difference = date2 - date1
    
    # استخراج عدد الأيام، الساعات، الدقائق والثواني من الفرق
    days = difference.days
    seconds = difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    return days, hours, minutes, seconds

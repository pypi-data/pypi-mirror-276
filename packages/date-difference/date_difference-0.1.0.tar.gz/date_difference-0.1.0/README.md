# date_difference

مكتبة Python لحساب الفرق بين تاريخين.

## كيفية الاستخدام

```python
from date_difference import calculate_date_difference

# حساب الفرق بين التاريخين
days, hours, minutes, seconds = calculate_date_difference("2023-01-01 12:00:00", "2024-05-30 15:30:45")

# طباعة النتيجة
print(f"الفرق بين التاريخين هو: {days} أيام، {hours} ساعات، {minutes} دقائق، {seconds} ثوانٍ")

from datetime import timedelta

def calculate_vacations_days(start_date, end_date):
  
  if start_date and end_date:
    delta = end_date - start_date
    return delta.days + 1 if delta.days >= 0 else 0
  return 0
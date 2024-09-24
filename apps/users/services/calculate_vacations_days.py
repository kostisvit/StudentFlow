from datetime import timedelta

def calculate_vacations_days(start_date, end_date):
  
  if start_date and end_date:
    delta = end_date - start_date
    return delta.days
  return 0
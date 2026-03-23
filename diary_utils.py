from datetime import date, timedelta

def get_working_days(start_date, end_date):
    """
    Calculates a list of working days (excluding Sundays) between two dates.
    """
    if start_date > end_date:
        return []
        
    working_days = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() != 6:  # 6 corresponds to Sunday
            working_days.append(current_date)
        current_date += timedelta(days=1)
    return working_days

def count_working_days(start_date, end_date):
    """
    Counts the number of working days (excluding Sundays) between two dates.
    """
    return len(get_working_days(start_date, end_date))

def is_sunday(d):
    """
    Checks if a given date is a Sunday.
    """
    return d.weekday() == 6

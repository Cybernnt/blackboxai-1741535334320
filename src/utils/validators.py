from datetime import datetime

def validate_date(date_str):
    """Validate date string in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_positive_number(value):
    """Validate if value is a positive number"""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False

def validate_stock_quantity(quantity, available_stock):
    """Validate if quantity is less than or equal to available stock"""
    try:
        return float(quantity) <= float(available_stock)
    except (ValueError, TypeError):
        return False

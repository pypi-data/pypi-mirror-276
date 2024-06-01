

from datetime import datetime
import pytz

__version__ = '24.6.1'

def print_current_timestamp(timezone='in'):
    if timezone == 'in':
        tz = 'Asia/Kolkata'
    elif timezone == 'ng':
        tz = 'Africa/Lagos'
    elif timezone == 'eu':
        tz = 'Europe/Paris'
    elif timezone == 'us':
        tz = 'US/Eastern'
    else:
        print("Invalid timezone abbreviation. Please use 'in', 'us', 'eu', or 'sa'.")
        return
    
    now = datetime.now(pytz.timezone(tz))
    print(f"Current {tz} Timestamp:", now)
    return now;

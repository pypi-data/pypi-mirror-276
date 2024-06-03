# sigevents_us/__init__.py

import pandas as pd
from .events import get_events

def add_events(df, order_date): # we can change the column name here, For JUICER we are using order_date
    df[order_date] = pd.to_datetime(df[order_date])
    df['Event'] = df[order_date].dt.strftime('%Y-%m-%d').map(lambda date: find_event(date))
    return df

def find_event(date_str):
    year = int(date_str[:4])
    events = get_events(year)
    for event, event_date in events.items():
        if event_date == date_str:
            return event
    return None

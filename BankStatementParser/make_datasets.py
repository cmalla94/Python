import pandas as pd 
import calendar
import re

df = pd.read_csv('data.csv')

df = df.drop(['c1', 'c2'], axis=1)
df = df[df.amount > 0]
df['month'] = df.date.str.replace('[\d*]', '').str.strip()
df['day'] = df.date.str.replace('[A-Z]', '').str.strip().str.extract(r'(\d{1,2})')
df = df.drop(['date'], axis=1)

test = {v: k for k,v in enumerate(calendar.month_abbr)}
months = {}
for key in test:
    months[key.upper()] = test[key]
def append_zero(x):
    x = int(x)
    return "{:02d}".format(x)
def make_date(df):
    date = '{}-{}-{}'.format(df.year, append_zero(months[df.month]), df.day)
    return date
def clean_month(month):
    return month[:3]
def convert_dollars(x):
    return '${:,.2f}'.format(x)





df['month'] = df.month.apply(clean_month)
df['day'] = df.day.apply(append_zero)
df['date'] = df.apply(make_date, axis=1)
df['date'] = df.date.str.strip()

df.columns = ['Place', 'amount', 'Year', 'Month', 'Day', 'Date']
cols = ['Date', 'Place', 'amount', 'Month', 'Year', 'Day']

df = df[cols]


# def extract_cities(text):
#     result = re.search(r"BURN*|VAN*|COQ*|SURR*|NORTH*|")
cities = df.Place.str.extract(r"(BURN|VAN|COQ|SURR|NORTH|NEW\s?WE*|WEST|LAS|TOR|SAN|RICH)", expand=False)
df['City'] = cities.str.replace('BURN', 'BURNABY').str.replace('RICH', 'RICHMOND') \
    .str.replace(r'NEW\sWE|WEST|NEWWE', 'NEW WESTMINSTER') \
        .str.replace('VAN', 'VANCOUVER').str.replace('SURR', 'SURREY').str.replace('NORTH', 'NORTH VANCOUVER') \
            .str.replace('COQ', 'COQUITLAM').str.replace('TOR', 'TORONTO') \
                .str.replace('SAN', 'SAN FRANSCISCO').str.replace('LAS', 'LAS VEGAS').fillna(value='Unknown')

df.to_csv('data_cleaned.csv', index=False)
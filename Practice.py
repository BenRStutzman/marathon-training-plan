import Functions as f

min_date = f.d.date(1998, 10, 6)
max_date = f.d.date(2020, 5, 1)
date = f.get_date('Enter a date between your birth and graduation', min_date, max_date)
print(date)

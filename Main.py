""" This program is a marathon training plan generator. """

import Functions as f

today = f.d.date.today()
mar_date = f.get_date("When is your marathon?", today,
                      today.replace(year = today.year + 10))
start_date = f.get_start_date(today, mar_date)
time_till_race = mar_date - start_date
print("You'll be training for", time_till_race.days, "days.")

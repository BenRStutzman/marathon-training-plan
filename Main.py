""" This program is a marathon training plan generator. """

import Functions as f

try:
    today = f.d.date.today()
    race_date = f.get_race_date(today, 10)
    start_date = f.get_start_date(today, race_date)
    weekly_mileage = f.get_mileage(10)
    (days_first_week, days_last_week, num_weeks) = f.calc_weeks(start_date,
                                                                race_date)
    plan = f.build_plan(days_first_week, days_last_week, num_weeks, weekly_mileage)
    print(plan)
except f.QuitError:
    f.e.msgbox("Too bad. I'm sure you could have done it!")

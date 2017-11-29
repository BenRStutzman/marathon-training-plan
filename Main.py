""" This program is a marathon training plan generator. """

import Functions as f

while True:
    try:
        today = f.d.date.today()
        race_date = f.get_race_date(today, 10)
        start_date = f.get_start_date(today, race_date)
        (days_first_week, days_last_week, num_weeks) = f.calc_weeks(start_date,
                                                                    race_date)
        weekly_mileage = f.calc_weekly_mileage(num_weeks)
        plan = f.build_plan(days_first_week, days_last_week, num_weeks,
                            weekly_mileage)
        f.write_plan(plan, start_date)
        f.deliver_plan()
        f.ask_another()
    except f.QuitError:
        break
f.e.msgbox("Good luck training!")

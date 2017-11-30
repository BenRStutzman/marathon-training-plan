""" This program is a marathon training plan generator. """

import Functions as f

while True:
    try:
        today = f.d.date.today()
        race_date = f.get_race_date(today, 10)
        start_date = f.get_start_date(today, race_date)
        (days_first_week, days_last_week, num_weeks, num_days) = f.calc_weeks(
            start_date, race_date)
        (initial_mileage, weekly_mileage) = f.calc_weekly_mileage(num_weeks, days_first_week,
                                               days_last_week)
        plan = f.build_plan(num_weeks, weekly_mileage, days_first_week,
                            days_last_week)
        long_runs = f.calc_long_runs(num_weeks, weekly_mileage,
                                     initial_mileage, days_first_week)
        plan = f.add_taper(plan, num_days, days_last_week)
        f.write_plan(plan, start_date)
        emailed = f.deliver_plan()
        f.ask_another(emailed)
    except f.QuitError:
        break
f.e.msgbox("Good luck training!")

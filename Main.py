"""
Ben Stutzman
CS 120 Final Project
12/1/2017
This is a marathon training plan generator. It asks the user for the dates he/she
wants to train and the intensity of training (mileage), and then creates a basic
plan for the number of miles he/she should run each day to prepare for the race.
It saves this to a text file and offers to email it to the user. """

import Functions as f

# Repeats until user decides to quit, allowing the generation of multiple plans
while True:
    try:
        # Finds the current date
        today = f.d.date.today()
        # Asks for the dates of the marathon and the beginning of training
        race_date = f.get_race_date(today, 10)
        start_date = f.get_start_date(today, race_date)
        # Calculates details about dates of the training schedule
        schedule = f.calc_schedule(start_date, race_date)
        (days_first_week, days_last_week, num_weeks, num_days) = schedule
        # Creates a gradually increasing weekly mileage regimen
        mileage = f.calc_mileage(num_weeks, days_first_week, days_last_week)
        (initial_mileage, final_mileage, weekly_mileage) = mileage
        # Builds the basic plan, based on the weekly mileage
        plan = f.build_plan(num_weeks, weekly_mileage,
                            days_first_week, days_last_week)
        # Adds one designated 'long run' each week to build endurance
        plan = f.add_long_runs(plan, num_weeks, initial_mileage, final_mileage,
                               days_first_week, days_last_week)
        # Eases up the plan at the end to let the runner rest up
        plan = f.add_taper(plan, num_days, days_last_week)
        # Write the plan to a text file 
        f.write_plan(plan, start_date)
        # Email the plan to the user, if desired
        emailed = f.deliver_plan()
        # Ask if the user wants to make another plan
        f.conclude(emailed)
    except f.QuitError:
        # Quits if the user ever closes an easygui box or presses cancel
        break
f.e.msgbox("Good luck training!")

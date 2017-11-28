""" This file contains the functions for the marathon
training plan generator. """

import calendar as c
import datetime as d
import easygui as e
from random import randint

class QuitError(Exception):
    """ An error to be raised if the user selects 'cancel' in any input box. """
    pass

def get_date(prompt, min_date, max_date):
    """ Ask the user to enter a date between two specified dates using
    easygui."""
    question = 'Please select the year:'
    choices = [i for i in range(min_date.year, max_date.year + 1)]
    year = e.choicebox(question, prompt, choices)
    if year == None:
        raise QuitError
    else:
        year = int(year)
    question = 'Please select the month:'
    choices = [('0' + str(i))[-2:] for i in range(1, 13)]
    if min_date.year == max_date.year:
        choices = choices[min_date.month - 1: max_date.month]
    elif year == min_date.year:
        choices = choices[min_date.month - 1:]
    elif year == max_date.year:
        choices = choices[:max_date.month]
    month = e.choicebox(question, prompt, choices)
    if month == None:
        raise QuitError
    else:
        month = int(month)
    question = 'Please select the day:'
    month_length = c.monthrange(year, month)[1]
    choices = [('0' + str(i))[-2:] for i in range(1, month_length + 1)]
    if (min_date.year, min_date.month) == (max_date.year, max_date.month):
        choices = choices[min_date.day - 1: max_date.day]
    elif (year, month) == (min_date.year, min_date.month):
        choices = choices[min_date.day - 1:]
    elif (year, month) == (max_date.year, max_date.month):
        choices = choices[:max_date.day]
    day = e.choicebox(question, prompt, choices)
    if day == None:
        raise QuitError
    else:
        day = int(day)
    
    return d.date(year, month, day)

def get_race_date(today, time_range):
    """ Ask the user for the date of their marathon. """
    max_date = today.replace(year = today.year + time_range)
    return get_date("When is your marathon?", today, max_date)

def get_start_date(today, race_date):
    """ Ask the user for the date they started/will start training. """
    question = "When do you want to start training?"
    choices = ['I already did!', 'Today!', 'Ummm, later...']
    answer = e.choicebox(question, '', choices)
    if answer == choices[0]:
        return get_date('When did you start training?', today.replace(year =
                        today.year - 1), today)
    elif answer == choices[1]:
        return today
    elif answer == choices[2]:
        return get_date('When will you start training?', today, race_date)
    else:
        raise QuitError

def get_mileage(min_mileage):
    question = "How many miles would you like to run per week?"
    while True:
        answer = e.integerbox(question)
        if answer == None:
            raise QuitError
        elif answer >= min_mileage:
            return answer
        else:
            e.msgbox("You must run at least %d miles per week." % min_mileage)

def calc_weeks(start_date, race_date):
    race_day = race_date.weekday()
    start_day = start_date.weekday()
    days_first_week = (7 - start_day) % 7
    days_last_week = (race_day + 1) % 7
    num_days = (race_date - start_date).days + 1
    if start_date.isocalendar()[:2] == race_date.isocalendar()[:2]:
        days_first_week = num_days
        days_last_week = 0
        num_weeks = 0
    else:
        num_weeks = (num_days - days_first_week - days_last_week) // 7
    if days_first_week:
        num_weeks += 1
    if days_last_week:
        num_weeks += 1
    return (days_first_week, days_last_week, num_weeks)


def split_week(days, total_mileage):
    proportions = [randint(1,100) for i in range(days)]
    multiplier = total_mileage / sum(proportions)
    mileage = [round(i * multiplier) for i in proportions]
    diff = total_mileage - sum(mileage)
    mileage[0] += diff
    return mileage

def build_plan(days_first_week, days_last_week, num_weeks, weekly_mileage):
    plan = {}
    start = 1
    end = num_weeks
    if days_first_week:
        plan[1] = split_week(days_first_week,
                               round(weekly_mileage * (days_first_week / 7)))
        start += 1
    for week in range(start, end):
        plan[week] = split_week(7, weekly_mileage)
    if days_last_week == 0:
        plan[num_weeks] = split_week(6, weekly_mileage - 26).append(26.2)
    elif days_last_week > 1:
        plan[num_weeks] = split_week(days_last_week - 1, round((weekly_mileage
                                - 26) * ((days_last_week - 1) / 7))).append(26.2)
    else:
        plan[num_weeks] = [26.2]
    return plan

if __name__ == '__main__':
    print("This file contains the functions for "
          "the marathon training plan generator.")

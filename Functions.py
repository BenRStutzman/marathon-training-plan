""" This file contains the functions for the marathon
training plan generator. """

import calendar as c
import datetime as d
import easygui as e
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import smtplib

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

def get_mileage(prompt, min_mileage, max_mileage, qualifier = ''):
    if min_mileage == 1:
        plural1 = ''
    else:
        plural1 = 's'
    if max_mileage == 1:
        plural2 = ''
    else:
        plural2 = 's'
    while True:
        answer = e.integerbox(prompt, lowerbound = None, upperbound = None)
        if answer == None:
            raise QuitError
        elif answer < min_mileage:
            e.msgbox("You must run at least %d mile%s%s."
                     % (min_mileage, plural1, qualifier))
        elif answer > max_mileage:
            e.msgbox("You may only run up to %d mile%s%s."
                     % (max_mileage, plural2, qualifier))
        else:
            return answer
            
            
def calc_mileage(num_weeks, days_first_week, days_last_week):
    initial_mileage = get_mileage("Initial miles per week?", 1, 75,
                                  " per week to start")
    final_mileage = get_mileage("Final miles per week?", max(30, initial_mileage)
                                , 100, " per week at the end")
    weekly_mileage = []
    if num_weeks == 2:
        weekly_mileage += [round(final_mileage * 0.75 * days_first_week / 7)]
    elif num_weeks == 3:
        weekly_mileage += [round(final_mileage * (days_first_week / 7))]
        weekly_mileage += [round(final_mileage * 0.75)]
    elif num_weeks == 4:
        weekly_mileage += [round(initial_mileage * (days_first_week / 7))]
        weekly_mileage.append(final_mileage)
        weekly_mileage += [round(final_mileage * 0.75)]
    elif num_weeks > 4:
        if days_first_week < 7:
            weekly_mileage += [round(initial_mileage * (days_first_week / 7))]
            num_weeks -= 1
        weekly_mileage += [round(initial_mileage + (i/(num_weeks - 3)) *
                (final_mileage - initial_mileage)) for i in range(
                 num_weeks - 2)]
        weekly_mileage += [round(final_mileage * 0.75)]
    weekly_mileage += [round(final_mileage / 2 * ((days_last_week - 1) / 7))]
    return (initial_mileage, final_mileage, weekly_mileage)

def calc_schedule(start_date, race_date):
    race_day = race_date.weekday()
    start_day = start_date.weekday()
    num_days = (race_date - start_date).days + 1
    if start_date.isocalendar()[:2] == race_date.isocalendar()[:2]:
        days_first_week = num_days
        days_last_week = num_days
        num_weeks = 1
    else:
        days_first_week = (7 - start_day) % 7
        days_last_week = (race_day + 1) % 7
        num_weeks = (num_days - days_first_week - days_last_week) // 7
        if days_first_week:
            num_weeks += 1
        else:
            days_first_week = 7
        if days_last_week:
            num_weeks += 1
        else:
            days_last_week = 7
    return (days_first_week, days_last_week, num_weeks, num_days)


def split_week(days, total_mileage, spread):
    if days == 0:
        return []
    proportions = [randint(1,100) for i in range(days - 1)]
    for day in range(len(proportions)):
        while proportions[day] < sum(proportions) / ((days - 1) * spread):
            proportions[day] += 1
        while proportions[day] > spread * sum(proportions) / (days - 1):
            proportions[day] -= 1
    proportions.append(0)
    multiplier = total_mileage / sum(proportions)
    mileage = [round(i * multiplier) for i in proportions]
    diff = total_mileage - sum(mileage)
    if mileage[0] > - diff:
        mileage[0] += diff
    else:
        mileage[0] = 0
    return mileage

def build_plan(num_weeks, weekly_mileage, days_first_week, days_last_week):
    plan = []
    spread = 2
    if num_weeks > 1:
        plan.append(split_week(days_first_week, weekly_mileage[0], spread)) 
        for week in range(1, num_weeks - 1):
            plan.append(split_week(7, weekly_mileage[week], spread))
    plan.append(split_week(days_last_week - 1, weekly_mileage[-1], spread)
                + [26.2])
    return plan

def calc_long_runs(num_weeks, initial_mileage, days_first_week, days_last_week,
                   longest_run):
    long_runs = []
    if days_last_week >= 6:
        last_run = round(longest_run / 2)
    else:
        last_run = 0
    first_long_run = round(initial_mileage/3)
    if num_weeks == 2:
        if days_first_week <= 2:
            long_runs.append(0)
        else:
            long_runs.append(last_run)
    elif num_weeks == 3:
        if days_first_week <= 2:
            long_runs.append(0)
        else:
            long_runs.append(longest_run)
        long_runs.append(last_run)
    elif num_weeks == 4:
        if days_first_week <= 2:
            long_runs.append(0)
        else:
            long_runs.append(first_long_run)
        long_runs += [longest_run, last_run]
    elif num_weeks > 4:
        if days_first_week <= 2:
            long_runs.append(0)
            num_weeks -= 1
        long_runs += [round(first_long_run + i / (num_weeks - 3) * (longest_run
                    - first_long_run)) for i in range(num_weeks - 2)]
        long_runs.append(last_run)
    return long_runs + [0]

def insert_long_run(week, week_index, distance):
    while week[-2] < distance:
        week[-2] += 1
        second_index = week.index(max(week[:-2]))
        week[second_index] -= 1
    while week[-2] > distance:
        week[-2] -= 1
        second_index = week.index(min(week[:-2]))
        week[second_index] += 1
    return week

def add_long_runs(plan, num_weeks, initial_mileage, final_mileage,
                  days_first_week, days_last_week):
    longest_run = get_mileage("How many miles will your longest training "
                              "run be?", 10, final_mileage * 2/5,
                              " for your longest run")
    long_runs = calc_long_runs(num_weeks, initial_mileage, days_first_week,
                               days_last_week, longest_run)
    for week_index, week in enumerate(plan):
        if long_runs[week_index]:
            plan[week_index] = insert_long_run(week, week_index,
                                               long_runs[week_index])
    return plan

def add_taper(plan, num_days, days_last_week):
    taper_vals = [5,3,1]
    if num_days >= 2:
        if  days_last_week >= 2:
            plan[-1][-2] = taper_vals[-1]
        else:
            plan[-2][-1] = taper_vals[-1]
    if num_days >= 3:
        if days_last_week >= 3:
            plan[-1][-3] = taper_vals[-2]
        elif days_last_week == 2:
            plan[-2][-1] = taper_vals[-2]
        else:
            plan[-2][-2] = taper_vals[-2]
    if num_days >= 4:
        if days_last_week >= 4:
            plan[-1][-4] = taper_vals[-3]
        elif days_last_week == 3:
            plan[-2][-1] = taper_vals[-3]
        elif days_last_week == 2:
            plan[-2][-2] = taper_vals[-3]
        else:
            plan[-2][-3] = taper_vals[-3]
    return plan

def write_plan(plan, start_date):
    text = 'Marathon Training Plan'
    counter = 0
    for week_num, week in enumerate(plan):
        text += '\n\nWeek ' + str(week_num + 1) + ':'
        for day in week:
            date_str = '\n' + (start_date + d.timedelta(counter)).strftime(
                                    '%A, %B %d')

            text += date_str
            if day == 1:
                plural = ''
            else:
                plural = 's'
            text += ':' + ' '*(26-len(date_str)) + str(day) + ' mile' + plural
            counter += 1
        if sum(week) == 1:
            plural = ''
        else:
            plural = 's'
        text += '\nTotal:' + ' '*20 + str(sum(week)) + ' mile' + plural
    with open('training_plan.txt', 'w+') as f:
        f.write(text)

def email_plan():
    while True:
        address = e.enterbox("Please enter your email address: ")
        if address == None:
            return False
        my_address = 'ben.stutzman.unofficial@gmail.com'
        message = MIMEMultipart()
        message['From'] = my_address
        message['To'] = address
        message['Subject'] = 'Your Marathon Training Plan'
        body = 'Attached is your training plan.\nHappy training!'
        message.attach(MIMEText(body, 'plain'))
        
        file_name = 'Training_plan.txt'
        with open(file_name, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', "attachment; "
                                  "filename= %s" % file_name)
            message.attach(attachment)
        # Source for attaching file to email (previous 8 lines): naelshiab.com

        try:
            server = smtplib.SMTP(host = 'smtp.gmail.com', port = 587)
            server.starttls()
            server.login(my_address, 'Boa8Constrictor9')
            message = message.as_string()
            server.sendmail(my_address, address, message)
            server.quit()
            return True
        except smtplib.SMTPRecipientsRefused:
            if not e.ynbox("Sorry, that email address is invalid. "
                       "Try another address?"):
                return False

def deliver_plan():
    if e.ynbox("Your plan has been created! "
                 "Would you like the file to be emailed to you?"):
        emailed = email_plan()
    else:
        emailed = False
    return emailed

def ask_another(emailed):
    if emailed:
        addition = "Message sent! "
    else:
        addition = "Your plan is in the file 'Training_plan.txt'. "
    if not e.ynbox(addition + "Make another plan?"):
        raise QuitError

if __name__ == '__main__':
    print("This file contains the functions for "
          "the marathon training plan generator.")

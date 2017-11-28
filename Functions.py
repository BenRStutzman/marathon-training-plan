""" This file contains the functions for the main method of the marathon training
plan generator. """

import datetime as d
import calendar as c
import easygui as e

def get_date(prompt, min_date, max_date):
    
    question = 'Please select the year:'
    choices = [i for i in range(min_date.year, max_date.year + 1)]
    year = int(e.choicebox(question, prompt, choices))

    question = 'Please select the month:'
    choices = [('0' + str(i))[-2:] for i in range(1, 13)]
    if min_date.year == max_date.year:
        choices = choices[min_date.month - 1: max_date.month]
    elif year == min_date.year:
        choices = choices[min_date.month - 1:]
    elif year == max_date.year:
        choices = choices[:max_date.month]
    month = int(e.choicebox(question, prompt, choices))

    question = 'Please select the day:'
    month_length = c.monthrange(year, month)[1]
    choices = [('0' + str(i))[-2:] for i in range(1, month_length + 1)]
    if (min_date.year, min_date.month) == (max_date.year, max_date.month):
        choices = choices[min_date.day - 1: max_date.day]
    elif (year, month) == (min_date.year, min_date.month):
        choices = choices[min_date.day - 1:]
    elif (year, month) == (max_date.year, max_date.month):
        choices = choices[:max_date.day]
    day = int(e.choicebox(question, prompt, choices))
    
    return d.date(year, month, day)

def get_start_date(today, mar_date):
    question = "When do you want to start training?"
    choices = ['I already did!', 'Today!', 'Ummm, later...']
    answer = e.choicebox(question, '', choices)
    if answer == choices[0]:
        return get_date('When did you start training?', today.replace(year =
                        today.year - 1), today)
    elif answer == choices[1]:
        return today
    else:
        return get_date('When will you start training?', today, mar_date)

if __name__ == '__main__':
    print('This file contains the functions for the main method of '
          'the marathon training plan generator.''')

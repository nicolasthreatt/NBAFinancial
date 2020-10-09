'''
teamsCurrrentCapPlot.py


TODO:
    - Compare N teams vs. each other 
'''

import argparse
import financialDB
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
import pandas as pd
import pyodbc


def getTeamsSalaryCapData(season):

    sql_table_df = financialDB.readTable("Teams", "SalaryCapOverview{}".format(season))

    year1 = sql_table_df[['Team', season]]

    year1[season] = year1[season].map(lambda x: x.replace(",", "").replace("$", ""))
    year1[season] = year1[season].astype(int)

    createPlot(year1, season)


def createPlot(data, season):

    ax = data.plot(figsize=(10, 8), y=season, kind='bar')

    # Add Axis Labels
    ax.set_title("Teams Salary Salary Cap: {} Season".format(season))

    ax.set_xlabel("Teams")
    ax.set_ylabel('Salary ($)')

    ax.set_xticklabels(data['Team'])

    # Import Numbers
    yearMean    = data[season].mean()
    salayCapMin = 109140000
    luxuryTax   = 132000000
    
    # Draw lines at official NBA Salary Cap, Team Average, and Luxary Tax for 2019-20 Season
    plt.axhline(y=salayCapMin, linestyle='--', linewidth=1, color='k')
    ax.annotate('{0:,.0f}'.format(salayCapMin), xy=(26, salayCapMin + 1000000), fontsize=7)

    plt.axhline(y=yearMean, linestyle=':', linewidth=1, color='r')
    ax.annotate('${0:,.0f}'.format(int(yearMean)), xy=(26, yearMean + 1000000), fontsize=7)

    plt.axhline(y=luxuryTax, linestyle='-.', linewidth=1, color='m')
    ax.annotate('${0:,.0f}'.format(luxuryTax), xy=(26, luxuryTax + 1000000), fontsize=8)
    
    # Add Extra Ticks
    ax.set_yticks(list(ax.get_yticks()) + [salayCapMin, yearMean, luxuryTax])
    a = ax.get_yticks().tolist()
    a = ['${0:,.0f}'.format(int(val)) for val in a]

    a[len(a) - 3] = 'Cap Minimum'
    a[len(a) - 2] = 'Team Average'
    a[len(a) - 1] = 'Luxury Tax'

    ax.set_yticklabels(a)

    plt.show()

def processCmdArgs():

    parser = argparse.ArgumentParser(description='Plotting teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")
    
    parser.add_argument('--team', dest='team', type=str, metavar='', required=False,
                         help="Abbreviated Team City")

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(args.season)

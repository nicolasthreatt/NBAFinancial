'''
teamsCurrrentCapPlot.py


TODO:
    - Format plot for Compare N teams vs. each other 
    - Cleanup/Reduce Code
'''

import argparse
import financialDB
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
import pandas as pd
import pyodbc

# Add to Utils.py
def getCmdTeam(cmdTeamAbr):
    teams = [
        ("ATL", "Atlanta Hawks"),          ("BOS", "Boston Celtics"),     ("BRK", "Brooklyn Nets"), 
        ("CHO", "Charlotte Hornets"),      ("CHI", "Chicago Bulls"),      ("CLE", "Cleveland Cavaliers"), 
        ("DAL", "Dallas Mavericks"),       ("DEN", "Denver Nuggets"),     ("DET", "Detroit Pistons"), 
        ("GSW", "Golden State Warriors"),  ("HOU", "Houston Rockets"),    ("IND", "Indiana Pacers"),
        ("LAC", "Los Angeles Clippers"),   ("LAL", "Los Angeles Lakers"), ("MEM", "Memphis Grizzlies"),
        ("MIA", "Miami Heat"),             ("MIL", "Milwaukee Bucks"),    ("MIN", "Minnesota Timberwolves"),
        ("NOP", "New Orleans Pelicans"),   ("NYK", "New York Knicks"),    ("OKC", "Oklahoma City Thunder"),
        ("ORL", "Orlando Magic"),          ("PHI", "Philadelphia 76ers"), ("PHO", "Phoenix Suns"),
        ("POR", "Portland Trail Blazers"), ("SAC", "Sacramento Kings"),   ("SAS", "San Antonio Spurs"),
        ("TOR", "Toronto Raptors"),        ("UTA", "Utah Jazz"),          ("WAS", "Washington Wizards"),
    ]

    for team in teams:
        if team[0] == cmdTeamAbr:
            return team[1]

    sys.exit('Invalid Team!')


def getTeamsSalaryCapData(season, cmdTeamsAbr=None):

    sql_table_df = financialDB.readTable("Teams", "SalaryCapOverview{}".format(season))

    teams = [ getCmdTeam(cmdTeamAbr) for cmdTeamAbr in cmdTeamsAbr ]

    print(teams)
    
    year1 = pd.DataFrame()
    if teams:
        year1 = sql_table_df[['Team', season]].loc[sql_table_df['Team'].isin(teams)]
    else:
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
    salayCapMin = 109140000    # 2019-20 Season
    luxuryTax   = 132000000    # 2019-20 Season
    
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
    
    parser.add_argument('--teams', dest='teams', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Abbreviated Teams City")

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(args.season, cmdTeamsAbr=args.teams)

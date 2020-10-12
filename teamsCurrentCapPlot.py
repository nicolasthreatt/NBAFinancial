'''
File:
    - teamsCurrrentCapPlot.py

Description:
    - Graphs each team current total salary for its players

TODO:
    - Investigate how to add Team Salary $ on top of bar when comparing teams
    - Figure out better way than to hardcore values for Luxary Tax and Cap Min
'''


import argparse
import financialDB
import matplotlib.pyplot as plt
import os
import pandas as pd
import pyodbc
import sys


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

    year1 = pd.DataFrame()
    if teams:
        year1 = sql_table_df[['Team', season]].loc[sql_table_df['Team'].isin(teams)]
    else:
        year1 = sql_table_df[['Team', season]]

    year1[season] = year1[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int)

    seasonAvg = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int).mean()

    createPlot(year1, season, seasonAvg)


def createPlot(data, season, seasonAvg):

    ax = data.plot(figsize=(10, 8), y=season, kind='bar')

    # Edit Axis Labels
    ax.set_title("Teams Salary Salary Cap: {} Season".format(season))
    ax.set_xlabel("Teams")
    ax.set_ylabel("Salary")
    ax.set_xticklabels(data['Team'])
    plt.xticks(rotation=80)

    # Set Y-Axis Limits
    ax.set_ylim(ymin=100000000)
    ax.set_ylim(ymax=140000000)

    # Format Y-Axis Ticks to Display $-Currency
    ax.set_yticks(list(ax.get_yticks()))
    a = ax.get_yticks().tolist()
    a = ['${0:,.0f}'.format(int(val)) for val in a]
    ax.set_yticklabels(a)

    # Format Axis Values Sizing
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)

    # Important Numbers
    salayCapMin = 109140000    # 2019-20 Season
    luxuryTax   = 132000000    # 2019-20 Season

    textIncrement = 400000
    data_size = len(data) - 0.55

    # Draw lines and add text at NBA Salary Cap, Team Average, and Luxary Tax for 2019-20 Season
    plt.axhline(y=salayCapMin, linestyle='--', linewidth=1, color='k')
    ax.text(data_size, salayCapMin + textIncrement, 
            'Cap Minimum - ${0:,.0f}'.format(salayCapMin),
            fontsize = 7,
            horizontalalignment="right")

    plt.axhline(y=seasonAvg, linestyle=':', linewidth=1, color='r')
    ax.text(data_size, int(seasonAvg) + textIncrement, 
            'Team Average - ${0:,.0f}'.format(int(seasonAvg)),
            fontsize = 7,
            horizontalalignment="right")

    plt.axhline(y=luxuryTax, linestyle='-.', linewidth=1, color='m')
    ax.text(data_size, luxuryTax + textIncrement, 
            'Luxury Tax - ${0:,.0f}'.format(luxuryTax),
            fontsize = 7,
            horizontalalignment="right")

    # Display Plot
    ax.get_legend().remove()
    plt.show()


# Add to Utils.py
def processCmdArgs():

    parser = argparse.ArgumentParser(description='Plotting teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")

    parser.add_argument('--teams', dest='teams', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Abbreviated Teams City")

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(season=args.season, cmdTeamsAbr=args.teams)

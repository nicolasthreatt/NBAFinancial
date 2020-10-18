'''
File:
    - teamsCurrrentCapPlot.py

Description:
    - Graphs each team current total salary for its players

TODO:
    - Investigate how to add Team Salary $ on top of bar when comparing teams
    - Figure out better way than to hardcode values for Luxary Tax and Cap Min
'''


import financialDB
import matplotlib.pyplot as plt
import pandas as pd
import utils


def getTeamsSalaryCapData(season, teamsAbr=None):

    sql_table_df = financialDB.readTable("Teams", "SalaryCapOverview{}".format(season))

    teams = [ utils.getCmdTeam(teamAbr) for teamAbr in teamsAbr ]

    year1 = pd.DataFrame()
    if teams:
        year1 = sql_table_df[['Team', season]].loc[sql_table_df['Team'].isin(teams)]
    else:
        year1 = sql_table_df[['Team', season]]

    year1[season] = year1[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int)

    league_avg = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int).mean()

    createPlot(year1, season, league_avg)


def createPlot(data, season, league_avg):

    ax = data.plot(figsize=(10, 8), y=season, kind='bar', legend=None)

    ax.set_title("Teams Salary Cap: {} Season".format(season))
    ax.set_xlabel("Teams")
    ax.set_ylabel("Salary")
    ax.set_xticklabels(data['Team'])
    plt.xticks(rotation=80)

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

    plt.axhline(y=league_avg, linestyle=':', linewidth=1, color='r')
    ax.text(data_size, int(league_avg) + textIncrement, 
            'League Average - ${0:,.0f}'.format(int(league_avg)),
            fontsize = 7,
            horizontalalignment="right")

    plt.axhline(y=luxuryTax, linestyle='-.', linewidth=1, color='m')
    ax.text(data_size, luxuryTax + textIncrement, 
            'Luxury Tax - ${0:,.0f}'.format(luxuryTax),
            fontsize = 7,
            horizontalalignment="right")

    plt.show()


if __name__ == "__main__":
    args = utils.processCmdArgs()

    getTeamsSalaryCapData(season=args.season, teamsAbr=args.teams)

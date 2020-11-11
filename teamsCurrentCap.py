'''
File:
    - teamsCurrrentCapPlot.py

Description:
    - Graphs each team current total salary for its players

TODO:
    - Investigate how to add Team Salary $ on top of bar when comparing teams
    - Figure out better way than to hardcode values for Luxary Tax and Cap Min
    - Cleanup
'''


import financialDB
import matplotlib.pyplot as plt
import pandas as pd
import utils
import sys

sys.path.insert(1, '../NBAPlots')
import plottingFinancial


def getTeamsSalaryCapData(season, teamsAbr=None, plot=None):

    sql_table_df = financialDB.readTable("Teams", "SalaryCapOverview{}".format(season))

    teams = [ utils.getCmdTeam(teamAbr) for teamAbr in teamsAbr ]

    teamsCurrentSalaryData = pd.DataFrame()
    if teams:
        teamsCurrentSalaryData = sql_table_df[['Team', season]].loc[sql_table_df['Team'].isin(teams)]
    else:
        teamsCurrentSalaryData = sql_table_df[['Team', season]]

    teamsCurrentSalaryData[season] = teamsCurrentSalaryData[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int)

    if plot == 'bar': 
        # Important Numbers (Need to move)
        salayCapMin = 109140000    # 2019-20 Season
        luxuryTax   = 132000000    # 2019-20 Season

        sql_table_df[season] = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", "")).astype(int)
        league_avg  = sql_table_df[season].mean() #TODO: GET MEAN FOR ALL TEAMS IN DB. MAYBE MAKE INTO FUNCTION
        plottingFinancial.createTeamsCurrentCapPlot(season, teamsCurrentSalaryData, salayCapMin, luxuryTax, league_avg)

    return teamsCurrentSalaryData


if __name__ == "__main__":
    args = utils.processCmdArgs()

    getTeamsSalaryCapData(season=args.season, teamsAbr=args.teams, plot=args.plot)

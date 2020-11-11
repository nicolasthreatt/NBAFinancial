'''
File:
    - salaryCapPlot.py

Description:
    - Get teams salary cap data from Database 
    - Plot if needed

TODO:
    - Add individual player(s) option to line graph
    - Better naming for varaibles and functions
'''


import financialDB
import numpy as np
import pandas as pd
import sys
import utils

sys.path.insert(1, '../NBAPlots')
import plottingFinancial as pltFinancial


class Team(dict):
    def __init__(self):
        self.seasons = dict()


class ContractInfo:
    def __init__(self, players, contracts):
        self.players    = players
        self.contracts  = contracts


def getTeamsSalaryCapData(season, teamsAbr=None, cmdYears=None, plot=None):

    sql_table_df  = financialDB.readTable("Players", "Payroll{}".format(season))

    contractYears = cmdYears if cmdYears else utils.getFutureSeasons(currentSeason=int(season[:4]), futureSeason=int(season[-2:]))

    # Format Data
    for year in contractYears:
        sql_table_df[year] = sql_table_df[year].map(lambda x: x.replace(",", "").replace("$", ""))
        sql_table_df[year] = [0 if contract == '' else contract for contract in sql_table_df[year]]
        sql_table_df[year] = sql_table_df[year].astype(int)

    teams = [ utils.getCmdTeam(teamAbr) for teamAbr in teamsAbr ] if teamsAbr else sql_table_df['Team'].unique()

    # Get Contract Data
    teams_to_contracts = dict()
    for team in teams:
        teams_to_contracts[team] = Team()
        for year in contractYears:

            year_sorted = sql_table_df[['Player', year]].sort_values(by=[year])
            year_sorted = year_sorted[year_sorted[year] > 0]
            teams_to_contracts[team].seasons[year] = ContractInfo(players=year_sorted["Player"].loc[sql_table_df.Team == team], 
                                                                  contracts=year_sorted[year].loc[sql_table_df.Team == team])

    if plot: determinePlot(teams_to_contracts, teams, contractYears, plot)

    return teams_to_contracts


def determinePlot(teams_to_contracts, teams, contractYears, plot):

    if plot == 'compare':
        pltFinancial.createCompareSubplots(teams_to_contracts, contractYears, teams)
    elif plot == 'line':
        pltFinancial.createLinePlot(teams_to_contracts, teams)
    elif plot == None:
        if (len(contractYears) == 1):
            pltFinancial.createIndividualYearPlot(teams_to_contracts, contractYears, teams)
        else:
            pltFinancial.createMultiYearSubplots(teams_to_contracts, contractYears, teams)


if __name__ == "__main__":
    args = utils.processCmdArgs()

    getTeamsSalaryCapData(args.season, teamsAbr=args.teams, cmdYears=args.years, plot=args.plot)

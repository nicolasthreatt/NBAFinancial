'''
teamContracts.py

TODO:
    - Finish Command line arguments for year and team
    - Cleanp
'''

import argparse
import financialDB
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
import numpy as np
import os
import pandas as pd
import pyodbc


class Team(dict):
    def __init__(self):
        self.seasons = dict()


class ContractInfo:
    def __init__(self, players, contracts):
        self.players    = players
        self.contracts  = contracts


def getFutureSeason(currentSeason, futureSeason):
    return (str(currentSeason)   + '-' + str(futureSeason),
            str(currentSeason+1) + '-' + str(futureSeason+1),
            str(currentSeason+2) + '-' + str(futureSeason+2),
            str(currentSeason+3) + '-' + str(futureSeason+3),
            str(currentSeason+4) + '-' + str(futureSeason+4),
            str(currentSeason+5) + '-' + str(futureSeason+5),
            "Guaranteed")


def getTeamsSalaryCapData(season):

    sql_table_df = financialDB.readTable("Players", "Payroll{}".format(season))

    currentSeason = int(season[:4])
    futureSeason  = int(season[-2:])
    contractYears = (year1, year2, year3, year4, year5, year6, guaranteed) = getFutureSeason(currentSeason, futureSeason)

    for season in contractYears:

        # Format Data
        sql_table_df[season] = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", ""))
        sql_table_df[season] = [0 if contract == '' else contract for contract in sql_table_df[season]]
        sql_table_df[season] = sql_table_df[season].astype(int)

    teamsPlayersContracts = dict()
    for team in sql_table_df['Team'].unique():

        teamsPlayersContracts[team] = Team()
        for year in contractYears:

            year_sorted = sql_table_df[['Player', year]].sort_values(by=[year])
            year_sorted = year_sorted[year_sorted[year] > 0]
            teamsPlayersContracts[team].seasons[year] = ContractInfo( players=year_sorted["Player"].loc[sql_table_df.Team == team], 
                                                                      contracts=year_sorted[year].loc[sql_table_df.Team == team] )

    createPlots(teamsPlayersContracts)


def createPlots(df_dict, season="2019-20"):

    (currentSeason, futureSeason) = ( int(season[:4]), int(season[-2:]) )
    contractYears = (year1, year2, year3, year4, year5, year6, guaranteed) = getFutureSeason(currentSeason, futureSeason)

    nrow, ncol = 3, 3
    for team in df_dict.keys():

        fig, ax = plt.subplots(nrow, ncol, constrained_layout=True)
        fig.suptitle('Salary Cap Player Breakdown - {}'.format(team), fontsize=12)
    
        seasons = list(contractYears)

        for row in range(0, 3):
            for col in range(0, 3):

                if (row != 2):
                    salay_year = seasons.pop(0)
                    ax[row, col].pie(x=df_dict[team].seasons[salay_year].contracts, 
                                        startangle=200,
                                        labels=df_dict[team].seasons[salay_year].players,
                                        rotatelabels = 25,
                                        labeldistance=1.0,
                                        textprops={'fontsize': 5},
                                        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                        shadow=False)[0]
                    ax[row, col].set_title(salay_year)

                elif (row == 2) and (col == 1):
                    salay_year = seasons.pop(0)
                    ax[row, col].pie(x=df_dict[team].seasons[salay_year].contracts, 
                                        startangle=200,
                                        labels=df_dict[team].seasons[salay_year].players,
                                        rotatelabels = 25,
                                        labeldistance=1.0,
                                        textprops={'fontsize': 5},
                                        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                        shadow=False)[0]
                    ax[row, col].set_title(salay_year)
                    
                else:
                    ax[row, col].axis('off')

        plt.show()


def processCmdArgs():

    parser = argparse.ArgumentParser(description='Plotting teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")
    
    parser.add_argument('--team', dest='team', type=str, metavar='', required=False,
                         help="Individal Team Season Salary Cap Infomation")
    

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(args.season)

    
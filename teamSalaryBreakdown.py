'''
teamContracts.py

TODO:
    - Explore more formating options
'''

import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
import pandas as pd
import pyodbc


class Season(dict):
    def __init__(self):
        self.seasons = dict()


class ContractInfo:
    def __init__(self, players, contracts):
        self.players   = players
        self.contracts = contracts


def connectDB():

    # Database Credentials
    server   = os.getenv('azureServer')
    database = os.getenv('azureDBFinancial')
    username = os.getenv('azureDBUsername')
    password = os.getenv('azureDBPswd')
    driver   = '{ODBC Driver 17 for SQL Server}'

    # Connect to Database
    cnxn = pyodbc.connect('DRIVER='+driver+';      \
                           SERVER='+server+';      \
                           PORT=1433;              \
                           DATABASE='+database+';  \
                           UID='+username+';       \
                           PWD='+ password)
    return cnxn


def getFutureSeason(currentSeason, futureSeason):
    return (str(currentSeason)   + '-' + str(futureSeason),
            str(currentSeason+1) + '-' + str(futureSeason+1),
            str(currentSeason+2) + '-' + str(futureSeason+2),
            str(currentSeason+3) + '-' + str(futureSeason+3),
            str(currentSeason+4) + '-' + str(futureSeason+4),
            str(currentSeason+5) + '-' + str(futureSeason+5))


def getTeamsSalaryCapData(season):

    '''
    TODO: Move lines 36-43 into a seperate file where every other file can access, something such as
    def importTable(sqlTable):
    '''
    # Connect to Database
    cnxn = connectDB()

    # Get Stats from Database
    sqlDB = pd.read_sql_query(
        '''SELECT *
            FROM [Players].[Payroll{}]'''.format(season), cnxn)

    currentSeason = int(season[:4])
    futureSeason  = int(season[-2:])
    (year1, year2, year3, year4, year5, year6) = getFutureSeason(currentSeason, futureSeason)

    for current, future in zip( range(currentSeason, currentSeason+6), range(futureSeason, futureSeason+6) ):

        # Format Data
        season = str(current) + '-' + str(future)
        sqlDB[season] = sqlDB[season].map(lambda x: x.replace(",", "").replace("$", ""))
        sqlDB[season] = [0 if contract == '' else contract for contract in sqlDB[season]]
        sqlDB[season] = sqlDB[season].astype(int)

    teamsPlayersContracts = dict()
    for team in sqlDB['Team'].unique():

        teamsPlayersContracts[team] = Season()
        for year in (year1, year2, year3, year4, year5, year6):

            year_sorted = sqlDB[['Player', year]].sort_values(by=[year])
            year_sorted = year_sorted[year_sorted[year] > 0]
            teamsPlayersContracts[team].seasons[year] = ContractInfo( year_sorted['Player'].loc[sqlDB.Team == team], year_sorted[year].loc[sqlDB.Team == team] )

        # TODO: Add Guarentee Pie Subplot

    createPlots(teamsPlayersContracts)


def createPlots(df_dict, season="2019-20"):
    # TODO: Create 6 subplots from class Season(dict)

    (currentSeason, futureSeason) = ( int(season[:4]), int(season[-2:]) )
    (year1, year2, year3, year4, year5, year6) = getFutureSeason(currentSeason, futureSeason)

    nrow, ncol = 2, 3
    for team in df_dict.keys():

        fig, ax = plt.subplots(nrow, ncol)
        fig.suptitle('Salary Cap Player Breakdown - {}'.format(team), fontsize=15)
        for a, (season, contractInfo) in zip(ax.flatten(), df_dict[team].seasons.items()):

            a.pie(x=contractInfo.contracts, 
                  startangle=200,
                  labels=contractInfo.players,
                  rotatelabels = 25,
                  labeldistance=1.0,
                  textprops={'fontsize': 5},
                  autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                  shadow=False)[0]
            a.set_title(season)

        plt.show()


def processCmdArgs():

    parser = argparse.ArgumentParser(description='Plotting teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")                 
    

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(args.season)

    
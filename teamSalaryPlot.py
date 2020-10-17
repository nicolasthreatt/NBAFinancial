'''
File:
    - teamSalaryPlot.py

Description:
    - Graphs a breakdown of team(s) contracts for its players

TODO:
    - Discover more options formatting plots
'''


import argparse
import financialDB
import itertools
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


class Team(dict):
    def __init__(self):
        self.seasons = dict()


class ContractInfo:
    def __init__(self, players, contracts):
        self.players    = players
        self.contracts  = contracts


# Add to Utils.py
def getFutureSeasons(currentSeason, futureSeason):
    return [ "Guaranteed",
             str(currentSeason)   + '-' + str(futureSeason),
             str(currentSeason+1) + '-' + str(futureSeason+1),
             str(currentSeason+2) + '-' + str(futureSeason+2),
             str(currentSeason+3) + '-' + str(futureSeason+3),
             str(currentSeason+4) + '-' + str(futureSeason+4),
             str(currentSeason+5) + '-' + str(futureSeason+5) ]


# Add to Utils.py
def getCmdTeam(teamAbr):
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
        if teamAbr == team[0]:
            return team[1]

    sys.exit('Invalid Team!')


def getTeamsSalaryCapData(season, teamsAbr=None, cmdYears=None, compare=False, line=False):

    sql_table_df  = financialDB.readTable("Players", "Payroll{}".format(season))

    contractYears = cmdYears if cmdYears else getFutureSeasons(currentSeason=int(season[:4]), futureSeason=int(season[-2:]))

    # Format Data
    for year in contractYears:
        sql_table_df[year] = sql_table_df[year].map(lambda x: x.replace(",", "").replace("$", ""))
        sql_table_df[year] = [0 if contract == '' else contract for contract in sql_table_df[year]]
        sql_table_df[year] = sql_table_df[year].astype(int)

    teams = [ getCmdTeam(teamAbr) for teamAbr in teamsAbr ] if teamsAbr else sql_table_df['Team'].unique()
    teams_to_contracts = dict()

    # Get Contract Data
    for team in teams:

        teams_to_contracts[team] = Team()
        for year in contractYears:

            year_sorted = sql_table_df[['Player', year]].sort_values(by=[year])
            year_sorted = year_sorted[year_sorted[year] > 0]
            teams_to_contracts[team].seasons[year] = ContractInfo(players=year_sorted["Player"].loc[sql_table_df.Team == team], 
                                                                  contracts=year_sorted[year].loc[sql_table_df.Team == team])

    determinePlot(teams_to_contracts, teams, contractYears,
                  compare=compare, line=line)


def determinePlot(teams_to_contracts, teams, contractYears, compare=False, line=False):

    if compare:
        createCompareSubplots(teams_to_contracts, contractYears, teams)
    elif line:
        createLinePlot(teams_to_contracts, teams)
    else:
        if (len(contractYears) == 1):
            createIndividualYearPlot(teams_to_contracts, contractYears, teams)
        else:
            createMultiYearSubplots(teams_to_contracts, contractYears, teams)


def convertContracts(players_to_contracts, teams_to_contracts, team):

    players_to_contracts.clear()
    teams_to_contracts[team].seasons.pop("Guaranteed")

    for season in teams_to_contracts[team].seasons.values():

        if not any([season.contracts.empty, season.players.empty]):
            contracts, players = zip(*sorted(zip(season.contracts, season.players), reverse=True))

        for player, contract in zip(np.array(players), np.array(contracts)): 

            if player not in players_to_contracts.keys():
                players_to_contracts[player] = list()
            players_to_contracts[player].append(contract)


def createCompareSubplots(teams_to_contracts, seasons, teams):

    season_itr = itertools.cycle(seasons)
    team_itr   = itertools.cycle(teams)

    fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
    fig.suptitle('Salary Cap Comparison', fontsize=12)

    for row in range(0, 1):
        for col in range(0, 2):
            salay_year = next(season_itr)
            team       = next(team_itr)

            contracts, players = zip(*sorted(zip(teams_to_contracts[team].seasons[salay_year].contracts, teams_to_contracts[team].seasons[salay_year].players), reverse=True))

            ax[col].pie(x=contracts, 
                        startangle=75,
                        labels=players,
                        rotatelabels = 25,
                        labeldistance=1.0,
                        textprops={'fontsize': 6},
                        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                        shadow=False)[0]

            ax[col].legend(loc = 'best', 
                           prop={'size': 6},
                           bbox_to_anchor=(1.05, 1),
                           borderaxespad=0,
                           labels=['%s - ${0:,.0f}'.format(s) % (l) for l, s in zip(players, contracts)])

            ax[col].set_title(team + ': ' + salay_year)

    plt.show()


#TODO: Add individual player(s) option
def createLinePlot(teams_to_contracts, teams):

    players_to_contracts = dict()
    for team in teams:

        convertContracts(players_to_contracts, teams_to_contracts, team)

        fig, ax = plt.subplots()
        for player, contracts in players_to_contracts.items():
            plt.plot(getFutureSeasons(2019, 20)[1:len(contracts)+1], contracts, marker='', linewidth=2, alpha=0.9, label=player)

        ax.set_ylim(ymin=0)
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, step=1000000))

        # Format Y-Axis Ticks to Display Currency ($)
        ax.set_yticks(list(ax.get_yticks()))
        a = ax.get_yticks().tolist()
        a = ['${0:,.0f}'.format(int(val)) for val in a]
        ax.set_yticklabels(a)

        plt.title("{}".format(team), fontsize=14)
        plt.xlabel("Season")
        plt.ylabel("Salary")

        plt.legend(loc='best')
        plt.grid(True)
        plt.show()


def createIndividualYearPlot(teams_to_contracts, seasons, teams):

    salay_year = seasons.pop(0)

    for team in teams:
        contracts, players = zip(*sorted(zip(teams_to_contracts[team].seasons[salay_year].contracts, teams_to_contracts[team].seasons[salay_year].players),
                                 reverse=True))

        fig, ax, junk = plt.pie(x=contracts,
                                startangle=75,
                                labels=players,
                                rotatelabels = 25,
                                labeldistance=1.0,
                                textprops={'fontsize': 7},
                                autopct='%1.1f%%',
                                shadow=False)

        plt.suptitle('Salary Cap Player Breakdown: {}'.format(team))
        plt.title('{}'.format(salay_year), fontsize=12)

        plt.legend(loc = 'best', 
                   prop={'size': 8},
                   bbox_to_anchor=(1.05, 1),
                   borderaxespad=0,
                   labels=['%s - ${0:,.0f}'.format(s) % (l) for l, s in zip(players, contracts)])

        plt.show()


def createMultiYearSubplots(teams_to_contracts, seasons, teams):

    season_itr = itertools.cycle(seasons)

    for team in teams:
        fig, ax = plt.subplots(nrows=3, ncols=3, constrained_layout=True)
        fig.suptitle('Salary Cap Player Breakdown - {}'.format(team), fontsize=12)

        for row in range(0, 3):
            for col in range(0, 3):

                if (row == 0) and (col == 1):
                    salay_year = next(season_itr)
                    ax[row, col].pie(x=teams_to_contracts[team].seasons[salay_year].contracts, 
                                     startangle=200,
                                     labels=teams_to_contracts[team].seasons[salay_year].players,
                                     rotatelabels = 25,
                                     labeldistance=1.0,
                                     textprops={'fontsize': 5},
                                     autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                     shadow=False)[0]
                    ax[row, col].set_title(salay_year)
                elif (row != 0):
                    salay_year = next(season_itr)
                    ax[row, col].pie(x=teams_to_contracts[team].seasons[salay_year].contracts, 
                                     startangle=200,
                                     labels=teams_to_contracts[team].seasons[salay_year].players,
                                     rotatelabels = 25,
                                     labeldistance=1.0,
                                     textprops={'fontsize': 5},
                                     autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                                     shadow=False)[0]
                    ax[row, col].set_title(salay_year)
                else:
                    ax[row, col].axis('off')

        plt.show()


# Add to Utils.py
def processCmdArgs():

    parser = argparse.ArgumentParser(description='Plotting teams salary cap infomation from https://www.basketball-reference.com/contracts/')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                         help="Teams' Season for Salary Cap Infomation")

    parser.add_argument('--teams', dest='teams', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Abbreviated Teams City")

    parser.add_argument('--years', dest='years', nargs='+', type=str, metavar='', required=False, default=list(),
                         help="Selected Year(s)")

    # TeamA YearA TeamB YearB
    parser.add_argument('--compare', dest='compare', action='store_true', required=False,
                         help='Compare Teams Seasons')

    parser.add_argument('--line', dest='line', action='store_true', required=False,
                         help='Line Graph Plot')

    return parser.parse_args()


if __name__ == "__main__":
    args = processCmdArgs()

    getTeamsSalaryCapData(args.season, teamsAbr=args.teams, cmdYears=args.years, compare=args.compare, line=args.line)

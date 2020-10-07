'''
teamSalary.py

'''

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
import pandas as pd
import pyodbc

import financialDB


def getTeamsSalaryCapData(season):

    sql_table_df = financialDB.readTable("Teams", "SalaryCapOverview2019-20")

    year1 = sql_table_df[['Team', '2019-20']]

    year1[season] = year1[season].map(lambda x: x.replace(",", "").replace("$", ""))
    year1[season] = year1[season].astype(int)

    createPlot(year1, "2019-20")


def createPlot(data, season):

    ax = data.plot(figsize=(10, 8), y=season, kind='bar')

    # Add Axis Labels
    ax.set_title("Teams Salary Salary Cap: {} Season".format(season))

    ax.set_xlabel("Teams")
    ax.set_ylabel('Salary ($)')

    ax.set_xticklabels(data['Team'])

    # Calculcate Avg Salary Cap
    yearMean = data[season].mean()
    salayCapMin = 109140000
    
    # Draw line at official NBA Salary Cap for 2019-20 Season
    plt.axhline(y=salayCapMin, linestyle='--', linewidth=1, color='k')
    ax.annotate('$109,140,000', xy=(26, salayCapMin + 1000000), fontsize=8)

    plt.axhline(y=yearMean, linestyle=':', linewidth=1, color='r')
    ax.annotate('${0:,.0f}'.format(int(yearMean)), xy=(26, yearMean + 1000000), fontsize=8)
    
    # Add Extra Ticks
    ax.set_yticks(list(ax.get_yticks()) + [salayCapMin, yearMean])
    a = ax.get_yticks().tolist()
    a = ['${0:,.0f}'.format(int(val)) for val in a]

    a[len(a) - 2] = 'Cap Minimum'
    a[len(a) - 1] = 'Team Average'

    ax.set_yticklabels(a)

    # rects = ax.patches

    # Make some labels.
    # labels = ["label%d" % i for i in xrange(len(rects))]

    # for rect, label in zip(rects, labels):
    #     height = rect.get_height()
    #     ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
    #             ha='center', va='bottom')

    plt.show()


if __name__ == "__main__":
    season = "2019-20" # TODO: Make cmd line arguement
    getTeamsSalaryCapData(season)

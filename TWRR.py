from utility import *
import pandas as pd
import sys

class Performance(object):

    @staticmethod
    def _dietzPeriodPostion(floatStartPosition, floatEndPosition, dfCF = None, convention = 0):
        """
        :param dfCF: must have 2 columns [Value, CFDirection(1:inCF, -1:outCF, rest direction will be ignored)]
        :param convention: 0:inCF is BOD and outCF is EOD, 1:BeginOfDay, 2:EndOfDay
        """
        totalInCF = dfCF.loc[dfCF['Direction'] == 1, 'Value'].sum()
        totalOutCF = dfCF.loc[dfCF['Direction'] == -1, 'Value'].sum()
        start = 0
        end = 0

        if dfCF is None:
            return floatStartPosition, floatEndPosition

        if convention == 0: #inCF is BOD and outCF is EOD
            start = floatStartPosition + totalInCF
            end = floatEndPosition + totalOutCF
        elif convention == 1: #BOD
            start = floatStartPosition + totalInCF - totalOutCF
            end = floatEndPosition
        elif convention == 2: #EOD
            start = floatStartPosition
            end = floatEndPosition - totalInCF + totalOutCF

        return start,end

    @classmethod
    def calcPeriodReturn(cls, floatStartPosition, floatEndPosition, dfCF = None, convention = 0):
        """
        :param floatStartPosition: start position
        :param floatEndPosition: end position
        :param dfCF: must have 2 columns [Value, CFDirection(1:inCF, -1:outCF, rest direction will be ignored)]
        :param convention: 0:inCF is BOD and outCF is EOD, 1:BeginOfDay, 2:EndOfDay
        :return: return value
        """
        try:
            startPos, endPos = cls._dietzPeriodPostion(floatStartPosition, floatEndPosition, dfCF, convention)
            if startPos == 0:
                raise Exception("Begin position should not be 0 when calculate return.")
            ret =  endPos/startPos - 1
            return ret
        except Exception as e:
            #todo: should be logged
            print("Unexpected error:", e.args)
            return None

    @staticmethod
    def chainLinkReturn(dfPeriodReturns):
        """
        :param dfPeriodReturns: a series of returns
        """
        seriesReturn = dfPeriodReturns['Return'] + 1
        re = seriesReturn.product() - 1
        return re

    @classmethod
    def consolidatedReturn(cls, dfComponentReturn):
        """

        :param dfComponentReturn: must have columns Weight and Return
        :return:
        """
        ret = dfComponentReturn.apply(lambda row: row['Weight'] * row['Return'], axis=1).sum()
        return ret

if __name__ == "__main__":
    dfCF = FileLoader.csvLoader(r'\test\dfCF.csv')
    print(Performance.calcPeriodReturn(500,100,dfCF))
    print(Performance.calcPeriodReturn(500, 100, dfCF, 1))
    print(Performance.calcPeriodReturn(500, 100, dfCF, 2))

    print(Performance.calcPeriodReturn(0, 0, dfCF))
    print(Performance.calcPeriodReturn(0, 0, dfCF, 1))
    print(Performance.calcPeriodReturn(0, 0, dfCF, 2))

    consolidatedReturn = FileLoader.csvLoader(r'\test\consolidatedReturn.csv')
    print(Performance.consolidatedReturn(consolidatedReturn))



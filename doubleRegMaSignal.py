import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class maSignal():

    def __init__(self):
        self.author = 'ChannelCMT'

    def maEnvironment(self, am, paraDict):
        envPeriod = paraDict["envPeriod"]

        envMa = ta.MA(am.close, envPeriod)
        envDirection = 1 if am.close[-1]>envMa[-1] else -1
        return envDirection, envMa

    def maCross(self,am,paraDict):

        regPeriod =  paraDict["regPeriod"]
        fastPeriod = paraDict["fastPeriod"]
        slowPeriod = paraDict["slowPeriod"]

        prediction = ta.LINEARREG(am.close, regPeriod)
        residual = (am.close - prediction) / am.close
        resSma = ta.MA(residual, fastPeriod)
        resLma = ta.MA(residual, slowPeriod)

        residualUp = resSma[-1] > resLma[-1] and resSma[-2]<= resLma[-2]
        residualDn = resSma[-1] < resLma[-1] and resSma[-2]>= resLma[-2]

        maCrossSignal = 0
        if residualUp:
            maCrossSignal = 1
        elif residualDn:
            maCrossSignal = -1
        else:
            resSignal = 0
        return maCrossSignal, resSma, resLma
    
    def filterLowAtr(self, am, paraDict):
        atrPeriod = paraDict["atrPeriod"]
        lowVolThreshold = paraDict["lowVolThreshold"]

        # 过滤超小波动率
        atr = ta.ATR(am.high, am.low, am.close, atrPeriod)
        filterCanTrade = 1 if atr[-1]>am.close[-1]*lowVolThreshold else 0
        return filterCanTrade
        
# Matplotlib model classes

import numpy as np

class Market():
    """total available market and service available segment"""

    def __init__(self, salespm, market_price, saspc, market_growth):
        """initialize market attributes"""
        self.salespm = salespm
        self.market_price = market_price
        self.saspc = saspc
        self.market_growth = market_growth

    def tam(self):
        self.market = round(float(self.salespm) * float(self.market_price) * (1+(float(self.market_growth)/100)) * 12, 2)
        return self.market

    def sas(self):
        self.seg = round(float(self.market) * (float(self.saspc)/100), 2)
        return self.seg

class Forecastpl():
    
    def __init__(self, unitsm1, pricem1, sgmom, cmgrowth, pindex, cogs, opex, fixed):
        """initialize fp&l attributes"""
        self.unitsm1 = unitsm1
        self.pricem1 = pricem1
        self.sgmom = sgmom
        self.cmgrowth = cmgrowth
        self.pindex = pindex
        self.cogs = cogs
        self.opex = opex
        self.fixed = fixed

    #growth percentages
    def sales_growth(self):
        self.sales_growth_mom = (float(self.sgmom) / 100) + 1
        return self.sales_growth_mom

    def cm_growth(self):
        self.cm_growth_mom = float(self.cmgrowth) / 100
        return self.cm_growth_mom

    def price_growth(self):
        self.price_growth_mom = (float(self.pindex) / 100) + 1
        return self.price_growth_mom

    def cogs_pc(self):
        self.cogs_initial = float(self.cogs) / 100
        return self.cogs_initial

    def opex_pc(self):
        self.opex_initial = float(self.opex) / 100
        return self.opex_initial

    def fixed_pc(self):
        self.fixed_cost = float(self.fixed) / 100  
        return self.fixed_cost    

    #unit sales growth mom cumulative
    def units_mom(self):
        unitlist = []
        for grmom in range(12):
            unitlist.append(self.unitsm1)
            self.unitsm1 = float(self.unitsm1) * self.sales_growth_mom
        self.units_array = np.asarray(unitlist, dtype=np.float64)
        return self.units_array    

    #unit price growth mom cumlative
    def price_mom(self):
        pricelist = []
        for grmom in range(12):
            pricelist.append(float(self.pricem1))
            self.pricem1 = float(self.pricem1) * self.price_growth_mom
        self.price_array = np.asarray(pricelist, dtype=np.float64)
        return self.price_array

    #revenue
    def revenue_profile(self):
        self.revenue = self.units_array * self.price_array
        return self.revenue

    #cm initial calculation
    def cm_calc_initial(self):
        self.cogs_m1 = self.revenue[0] * self.cogs_initial
        self.opex_m1 = self.revenue[0] * self.opex_initial
        self.cm_m1 = self.revenue[0] - (self.cogs_m1 + self.opex_m1)
        self.cm_pc_m1 = self.cm_m1 / self.revenue[0]
        return self.cm_pc_m1

    #cm adjusted
    def cm_adjusted(self):
        cmlist = []
        for grmom in range(12):
            cmlist.append(self.cm_pc_m1)
            self.cm_pc_m1 = self.cm_pc_m1 + self.cm_growth_mom
        self.cm_array = np.asarray(cmlist, dtype=np.float64)
        return self.cm_array

    #cm calculation
    def cm_calc(self):
        self.cm_calc_fpl = self.revenue * self.cm_array
        return self.cm_calc_fpl

    #fixed costs
    def fixed_calc(self):
        self.fplfixed = self.revenue[0] * self.fixed_cost
        self.fixed_array = np.full((12), self.fplfixed)
        return self.fixed_array

    #operating profit
    def fpl_op_profit(self):
        self.op_profit = self.cm_calc_fpl - self.fixed_array
        return self.op_profit

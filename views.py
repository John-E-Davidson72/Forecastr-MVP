# views.py

#imports
from flask import Flask, render_template, request, redirect, url_for

import numpy as np

import matplotlib.pyplot as plt

from models import Market, Forecastpl

import os, datetime

from nocache import nocache

# app config
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "null" 
app.config['SECRET_KEY'] = '\\\x01\x81\x12\xc5\xa6\xa4Q\x90\x1ct\x89E\x1dzr8~P\xdb\x0f\xfbq\xed'
app.config["DEBUG"] = False

# get script folder, set path and incremental file names
base_dir = os.path.abspath(__file__)
temp_dir = os.path.split(base_dir)
path_dir = temp_dir[0]
#set the chart path
chart_path = '\\static\\img\\'
# set incremental file names
fileDate = datetime.datetime.now()
fileExt = fileDate.strftime("%Y%m%d%H%M%S")
fileName = 'plot-' + fileExt + '.png'
# define the full path for the chart
img_path = path_dir + chart_path + fileName

#routes
@app.route('/', methods=['GET', 'POST'])
@nocache
def market():
    if request.method == 'POST':
        return redirect(url_for('forecast'))
    else:
        return render_template('market.html')

@app.route('/forecast/<urldate>', methods=['POST'])
@nocache
def forecast(urldate):
    #tam & sas
    sales = request.form['sales']
    price = request.form['price']
    sas = request.form['sas']
    growth = request.form['growth']
    total = Market(sales, price, sas, growth)
    calc_tam = total.tam()
    calc_sas = total.sas()
    #forecast P&L inputs
    salesm1 = request.form['salesm1']
    pricem1 = request.form['pricem1']
    sgmom = request.form['sgmom']
    cmgrowth = request.form['cmgrowth']
    pindex = request.form['pindex']
    cogs = request.form['cogs']
    opex = request.form['opex']
    fixed = request.form['fixed']
    #forecast P&L class constructor
    fpl = Forecastpl(salesm1, pricem1, sgmom, cmgrowth, pindex, cogs, opex, fixed)
    #x chart axis
    x = np.arange(1, 13)
    #forecast P&L growth and percentages
    fpl.sales_growth()
    fpl.cm_growth()
    fpl.price_growth()
    fpl.cogs_pc()
    fpl.opex_pc()
    fpl.fixed_pc()
    #forecast P&L pre-plot calculations
    fpl.units_mom()
    fpl.price_mom()
    fpl_rev = fpl.revenue_profile()
    fpl.cm_calc_initial()
    fpl.cm_adjusted()
    fpl_cmadj = fpl.cm_calc()
    fpl.fixed_calc()
    fpl_op = fpl.fpl_op_profit()
    #forecast P&L cumulative
    fpl_rev_cum = np.cumsum(fpl_rev)
    fpl_cmadj_cum = np.cumsum(fpl_cmadj)
    fpl_op_cum = np.cumsum(fpl_op)
    #sas and fp&l comparison
    fpl_sas = round(np.sum(fpl_rev, dtype=np.float64), 2)
    fpl_sas_delta = round(float(fpl_sas - calc_sas), 2)
    fpl_sas_delta_pc = round(float((fpl_sas / calc_tam) * 100), 2)    
    #plot parameters
    plt.plot(x, fpl_rev_cum, label='revenue')
    plt.plot(x, fpl_cmadj_cum, label='cm')
    plt.plot(x, fpl_op_cum, label='op profit')
    plt.xlabel('month')
    plt.ylabel('£')
    plt.title('Forecast P&L cumulative ')
    plt.legend()
    plt.xticks(x)
    plt.savefig(img_path)
    return render_template(
        'forecast.html', 
        sales=sales,
        price=price,
        sas=sas,
        growth=growth,
        calc_tam=calc_tam, 
        calc_sas=calc_sas,
        name = 'Forecast P&L cumulative', 
        fpl_sas = fpl_sas,
        fpl_sas_delta = fpl_sas_delta,
        fpl_sas_delta_pc = fpl_sas_delta_pc,
        urldate = urldate,
        fileName = fileName,
        fileExt = fileExt
    )

@app.context_processor
def inject_timestamp():
    return {'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S")}

#if __name__ == "__main__":
    #app.run()

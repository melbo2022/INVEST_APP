from flask import Flask, render_template, request, jsonify
import numpy as np
import numpy_financial as npf
import pandas as pd
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64

#-期間計算（NPER)---------------------------------------------------------------------
def calculate_nper(rate, pmt, pv, fv, when):
    nper = npf.nper(rate / 12, pmt, pv, fv, when)
    nper = int(nper)
    nper_year = nper / 12
    nper_year_round = math.ceil(nper_year * 10) / 10

    return nper, nper_year_round

#-現在価値計算（PV)---------------------------------------------------------------------
def calculate_pv(rate,nper,pmt,fv,when):
    pv=npf.pv(rate/12,nper*12,-pmt,fv,when)
    pv = int(pv)
    return pv

#-将来価値計算（fV)---------------------------------------------------------------------
def calculate_fv(rate,nper,pmt,pv,when):
    fv=npf.fv(rate/12,nper*12,-pmt,-pv,when)
    fv = int(fv)
    return fv
#-積立（支払）額計算(pmt)----------------------------------------------------------------
def calculate_pmt(rate,nper,pv,fv,when):
    pmt=npf.pmt(rate/12,nper*12,pv,fv,when)
    pmt=int(pmt)
    return pmt

#-利率計算(rate)----------------------------------------------------------------
def calculate_rate(nper,pmt,pv,fv,when):    
    rate=npf.rate(nper*12,pmt,pv,fv,when)
    rate=rate*12
    return rate

#-指定回元金支払計算(ppmt)----------------------------------------------------------------
def calculate_ppmt(rate,per,nper,pv,fv,when):   
    ppmt=npf.ppmt(rate/12,per,nper*12,pv,fv,when)  
    return ppmt

#-指定回利息支払計算(ipmt)----------------------------------------------------------------
def calculate_ipmt(rate,per,nper,pv,fv,when):   
    ipmt=npf.ipmt(rate/12,per,nper*12,pv,fv,when)  
    return ipmt


# if __name__ == "__main__":
#     calculate_nper(rate, pmt, pv, fv, when)
   


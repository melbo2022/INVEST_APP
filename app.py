'''place holder
depo
利率0.02
積立額50,000円
現在貯蓄額1,000,000円
期間33年
目標　30,000,000円

Loan
利率　0.02
返済額200,000円
借入額　30,000,000円
期間14.4年

Pen
利率　0.02
取崩額　200,000円
年金原資額20,000,000円
期間9.1年
'''


from flask import Flask, render_template, request,session
from flask_session import Session
import numpy_financial as npf
import matplotlib.pyplot as plt
# フォントの設定を変更して日本語をサポート
plt.rcParams["font.family"] = "IPAGothic"
#--------------------------------------------------------------------------------------
from calculate import calculate_nper,calculate_pv,calculate_fv,calculate_pmt,calculate_rate,calculate_ppmt,calculate_ipmt
from generate_plot import generate_plot
#--------------------------------------------------------------------------------------

app = Flask(__name__)

# Flask-Sessionの設定
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# 'static' フォルダを静的ファイルとして提供
app.config['UPLOAD_FOLDER'] = 'static'

#--ここから------------------------------------------------------------------
@app.route('/')
def index():
    
    return render_template('index.html')

@app.errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

#---------------------------------------------------------------------------------
@app.route('/Savings', methods=['GET', 'POST'])
def Savings():
    inv_name = "積立運用計算"
    return render_template('deposit.html', inv_name=inv_name)

@app.route('/Loan', methods=['GET', 'POST'])
def Loan():
    inv_name = "借入金計算"
    return render_template('loan.html', inv_name=inv_name)

@app.route('/Pen', methods=['GET', 'POST'])
def Pen():
    inv_name = "年金計算"
    return render_template('pen.html', inv_name=inv_name)


#-NPER-----------------------------------------------------------------------------
@app.route('/NPER_depo', methods=['GET', 'POST'])
@app.route('/NPER_loan', methods=['GET', 'POST'])
@app.route('/NPER_pen', methods=['GET', 'POST'])

def NPER_all():
    if request.path == '/NPER_depo':
        url_name = "depo"
        template = "output_nper_depo.html"
        x_label = '経過年数'
        y_label = '積立貯蓄金残高'
        title = '積立貯蓄額累積グラフ'


    elif request.path == '/NPER_loan':
        url_name = "loan"
        template = "output_nper_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'


    elif request.path == '/NPER_pen':
        url_name = "pen"
        template = "output_nper_pen.html"
        x_label = '経過年数'
        y_label = '年金原資残高'
        title = '年金原資残高グラフ'

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass
    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        pmt = float(request.form.get('input2'))
        pv = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        when = int(request.form.get('input5'))

      

        nper, nper_year_round = calculate_nper(rate, pmt, pv, fv, when)

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

       
        return render_template(template, nper=nper, nper_year=nper_year_round, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)

#-PV-----------------------------------------------------------------------------
@app.route('/PV_loan', methods=['GET', 'POST'])
@app.route('/PV_pen', methods=['GET', 'POST'])

def PV_all(): 


    if request.path == '/PV_loan':
        url_name = "loan"
        template = "output_PV_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'


    elif request.path == '/PV_pen':
        url_name = "pen"
        template = "output_PV_pen.html"
        x_label = '経過年数'
        y_label = '年金原資残高'
        title = '年金原資残高グラフ'

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass
    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        nper = float(request.form.get('input2'))
        pmt = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        when = int(request.form.get('input5'))   

        pv = calculate_pv(rate, nper, pmt, fv, when)
        nper=int(nper)*12

        x_list = list(range(1, nper + 1))

        if request.path == '/PV_pen':               
            y_list = [-(npf.fv(rate / 12, k, -pmt, pv, when)) for k in x_list]

        elif request.path == '/PV_loan': 
            y_list = [npf.fv(rate / 12, k, -pmt, pv, when) for k in x_list]
        

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()
        
        # if request.path == '/PV_pen':
        #     pv=pv*-1

        # pvを3桁区切りにフォーマット
        formatted_pv = '{:,.0f}'.format(pv)

       
        return render_template(template, pv=formatted_pv, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)

#-FV-----------------------------------------------------------------------------
@app.route('/FV_depo', methods=['GET', 'POST'])

def FV_all(): 


    if request.path == '/FV_depo':
        url_name = "depo"
        template = "output_fv_depo.html"
        x_label = '経過年数'
        y_label = '積立貯蓄金残高'
        title = '積立貯蓄額累積グラフ'
   

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        print("該当なし")

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        nper = float(request.form.get('input2'))
        pmt = float(request.form.get('input3'))
        pv = float(request.form.get('input4'))
        when = int(request.form.get('input5'))          

        fv = calculate_fv(rate, nper, pmt, pv, when)
        nper=int(nper)*12
   

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, -pmt, -pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # fvを3桁区切りにフォーマット
        formatted_fv = '{:,.0f}'.format(fv)
       
        return render_template(template, fv=formatted_fv, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)

#-PMT-----------------------------------------------------------------------------
@app.route('/PMT_depo', methods=['GET', 'POST'])
@app.route('/PMT_loan', methods=['GET', 'POST'])
@app.route('/PMT_pen', methods=['GET', 'POST'])

def PMT_all(): 

    if request.path == '/PMT_depo':
        url_name = "depo"
        template = "output_pmt_depo.html"
        x_label = '経過年数'
        y_label = '積立貯蓄金残高'
        title = '積立貯蓄額累積グラフ'



    elif request.path == '/PMT_loan':
        url_name = "loan"
        template = "output_pmt_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'


    elif request.path == '/PMT_pen':
        url_name = "pen"
        template = "output_pmt_pen.html"
        x_label = '経過年数'
        y_label = '年金原資残高'
        title = '年金原資残高グラフ'

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        nper = float(request.form.get('input2'))
        pv = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        when = int(request.form.get('input5'))   

        pmt = calculate_pmt( rate,nper,pv,fv,when)
        nper=int(nper)*12

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # pmtを3桁区切りにフォーマット
        formatted_pmt = '{:,.0f}'.format(pmt)

       
        return render_template(template, pmt=formatted_pmt, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)

    
#-PMT-----------------------------------------------------------------------------
@app.route('/RATE_depo', methods=['GET', 'POST'])
@app.route('/RATE_loan', methods=['GET', 'POST'])
@app.route('/RATE_pen', methods=['GET', 'POST'])

def RATE_all(): 

    if request.path == '/RATE_depo':
        url_name = "depo"
        template = "output_rate_depo.html"
        x_label = '経過年数'
        y_label = '積立貯蓄金残高'
        title = '積立貯蓄額累積グラフ'



    elif request.path == '/RATE_loan':
        url_name = "loan"
        template = "output_rate_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'


    elif request.path == '/RATE_pen':
        url_name = "pen"
        template = "output_rate_pen.html"
        x_label = '経過年数'
        y_label = '年金原資残高'
        title = '年金原資残高グラフ'

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        nper = float(request.form.get('input1'))
        pmt = float(request.form.get('input2'))
        pv = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        when = int(request.form.get('input5'))   

        rate = calculate_rate(nper,pmt,pv,fv,when)
        nper=int(nper)*12
        

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # rateを%でフォーマット
        formatted_rate = "{:.1%}".format(rate)

       
        return render_template(template, rate=formatted_rate, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)

#PPMT---------------------------------------------------------------------------------
@app.route('/PPMT_loan', methods=['GET', 'POST'])

def PPMT_loan(): 

    if request.path == '/PPMT_loan':
        url_name = "loan"
        template = "output_ppmt_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'    

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        per = float(request.form.get('input2'))
        nper = float(request.form.get('input3'))
        pv = float(request.form.get('input4'))
        fv = float(request.form.get('input5'))
        when = int(request.form.get('input6'))   

        ppmt= calculate_ppmt(rate,per,nper,pv,fv,when)
        ppmt=int(ppmt)

        pmt=npf.pmt(rate/12,nper*12,pv,fv,when)
        pmt=int(pmt)       

        nper=int(nper)*12
        

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # pmtを3桁区切りにフォーマット
        formatted_ppmt = '{:,.0f}'.format(ppmt)

       
        return render_template(template, ppmt=formatted_ppmt, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)
    
#IPMT---------------------------------------------------------------------------------
@app.route('/IPMT_loan', methods=['GET', 'POST'])

def IPMT_loan(): 

    if request.path == '/IPMT_loan':
        url_name = "loan"
        template = "output_Ipmt_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'    

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        per = float(request.form.get('input2'))
        nper = float(request.form.get('input3'))
        pv = float(request.form.get('input4'))
        fv = float(request.form.get('input5'))
        when = int(request.form.get('input6'))   

        ipmt= calculate_ipmt(rate,per,nper,pv,fv,when)
        ipmt=int(ipmt)

        pmt=npf.pmt(rate/12,nper*12,pv,fv,when)
        pmt=int(pmt)       

        nper=int(nper)*12
        

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # pmtを3桁区切りにフォーマット
        formatted_ipmt = '{:,.0f}'.format(ipmt)

       
        return render_template(template, ipmt=formatted_ipmt, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)
    
#CUMIPMT---------------------------------------------------------------------------------
@app.route('/CUMIPMT_loan', methods=['GET', 'POST'])

def CUMIPMT_loan(): 

    if request.path == '/CUMIPMT_loan':
        url_name = "loan"
        template = "output_cumIpmt_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'    

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        nper = float(request.form.get('input2'))
        pv = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        speriod = int(request.form.get('input5'))
        eperiod = int(request.form.get('input6'))
        when = int(request.form.get('input7'))   

       
       # cumipmtがnumpyで使用できないためipmtより計算する-------------------------------
        cumipmt = 0
        for r in range(speriod, eperiod + 1):
            ipmt = npf.ipmt(rate / 12, r, nper * 12, pv, fv, when)
            cumipmt = cumipmt + int(ipmt)

    #グラフ用に算出----------------------------------------------------------------------
        pmt=npf.pmt(rate/12,nper*12,pv,fv,when)
        pmt=int(pmt)   
        nper=int(nper)*12
    #------------------------------------------------------------------------------------

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # pmtを3桁区切りにフォーマット
        formatted_cumipmt = '{:,.0f}'.format(cumipmt)

       
        return render_template(template, cumipmt=formatted_cumipmt, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)
    
    

    
#CUMPRINC---------------------------------------------------------------------------------
@app.route('/CUMPRINC_loan', methods=['GET', 'POST'])

def CUMPRINC_loan(): 

    if request.path == '/CUMPRINC_loan':
        url_name = "loan"
        template = "output_cumprinc_loan.html"
        x_label = '経過年数'
        y_label = '借入金残高'
        title = '借入金残高グラフ'    

    else:
        # どのURLにもマッチしない場合の処理
        # 例えば、エラーを返すなどの適切な処理を記述する
        pass

    if request.method == 'POST':
        rate = float(request.form.get('input1'))
        nper = float(request.form.get('input2'))
        pv = float(request.form.get('input3'))
        fv = float(request.form.get('input4'))
        speriod = int(request.form.get('input5'))
        eperiod = int(request.form.get('input6'))
        when = int(request.form.get('input7'))   

       
       # cumprincがnumpyで使用できないためppmtより計算する
        cumprinc = 0
        for r in range(speriod, eperiod + 1):
            ppmt = npf.ppmt(rate / 12, r, nper * 12, pv, fv, when)
            cumprinc = cumprinc + int(ppmt)

    #グラフ用に算出----------------------------------------------------------------------
        pmt=npf.pmt(rate/12,nper*12,pv,fv,when)
        pmt=int(pmt)   
        nper=int(nper)*12
    #------------------------------------------------------------------------------------

        x_list = list(range(1, nper + 1))
        y_list = [npf.fv(rate / 12, k, pmt, pv, when) for k in x_list]

        x_year_list = []
        for i in x_list:
            val = i % 12
            if val == 0:
                n = i // 12
                x_year_list.append(n)
            else:
                continue

        last_year = len(x_year_list) + 1
        x_year_list.append(last_year)

        y_year_list = y_list[11::12]
        y_year_list.append(fv)

       
        graph_html = generate_plot(x_year_list, y_year_list, x_label, y_label, title)


        # セッションデータをクリア
        session.clear()

        # pmtを3桁区切りにフォーマット
        formatted_cumprinc = '{:,.0f}'.format(cumprinc)

       
        return render_template(template, cumprinc=formatted_cumprinc, graph_html=graph_html, title=title, url_name=url_name)

    else:
        return render_template(template)
    



#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)









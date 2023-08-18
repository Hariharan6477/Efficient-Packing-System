from flask import Flask, render_template,request,session
from knapsack_01 import knapsack_dynamic_programming
from knapsack_frac import knapsack_frac
from adt import item
import sqlite3
from plot_gen import graph
from plot_gen1 import graph1
from SendMail import Send_Mail

app = Flask(__name__)

app.secret_key='abc@123'

@app.route('/')
def home():
    try:
        if session['loggedin']==True:
            return render_template('logout.html')
        else:
            return render_template('index.html')
    except:
        return render_template('index.html') 

@app.route('/login', methods=['GET','POST'])
def loginchk():
    msg=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        mail=str(request.form['email'])
        pasw=str(request.form['password'])
        connection=sqlite3.connect('Customer.db')
        cursor=connection.cursor()
        cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ? and PASSWORD = ?;",(mail,pasw))
        row=cursor.fetchall()
        if len(row)==1:
            session['loggedin'] = True
            session['name']=row[0][0]
            session['mail']=row[0][1]
            return render_template('logout.html')
        else:
            msg='incorrect login credentials! please recheck'
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        name=str(request.form['name'])
        mail=str(request.form['email'])
        ph=int(request.form['phone'])
        pasw=str(request.form['password'])
        if len(name)<15:
            if len(mail)<25:
                if '@gmail.com'in mail:
                    if len(str(ph))==10:
                        if len(pasw)<8:
                            connection=sqlite3.connect('Customer.db')
                            cursor=connection.cursor()
                            cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ?;",(mail,))
                            row=cursor.fetchall()
                            connection.commit()
                            if len(row)==0:
                                cursor.execute('''INSERT INTO CUSTOMER VALUES(?,?,?,?);''',(name,mail,ph,pasw))
                                connection.commit()
                                msg='registered successfully!'
                                session['loggedin'] = True
                                session['name']=name
                                session['mail']=mail
                                return render_template('logout.html')
                            else:
                                msg='          user already found,please sign in!'
                        else:
                            msg='         password length should be within 8 characters!'
                    else:
                        msg='          enter a valid phone number!'
                else:
                    msg='         email id should contain @gmail.com!'
            else:
                msg='          email-id too long!'
        else:
            msg='         name is more than the limit of 14 letters!'
    return render_template('register.html',msg=msg)

@app.route('/logout', methods=['GET','POST'])
def logout():
    session['loggedin']=False
    return render_template('index.html')

@app.route('/knapsack')
def knapsack():
    try:
        if session['loggedin']==True:
            return render_template('knapsack.html')
        else:
            return render_template('login.html')
    except:
        return render_template('login.html')    

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/weights-and-values', methods=['POST'])
def weights_and_values():
    num_products = int(request.form['num-products'])
    capacity = int(request.form['capacity'])
    return render_template('weights_and_values.html', num_products=num_products,capacity=capacity)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

def calculate_price(packed_weight,address):
    total_cost = packed_weight*7
    labour_charge=250
    shipment_cost_within_city=50
    shipment_cost_outside_city=250
    total_cost+=labour_charge
    if ('chennai' in address.lower()):
        total_cost+=shipment_cost_within_city
    else:
        total_cost+=shipment_cost_outside_city
    return total_cost

@app.route('/pricelogin')
def pricelogin():
    try:
        if session['loggedin']==True:
            return render_template('knapsack.html')
        else:
            return render_template('login.html')
    except:
        return render_template('login.html')

@app.route('/result', methods=['POST'])
def result():
    num_products = int(request.form['num-products'])
    capacity = int(request.form['capacity'])
    weights = []
    values = []
    names=[]
    types=[]
    items=[]
    for i in range(num_products):
        name = str(request.form[f'name{i}'])
        weight = int(request.form[f'weight{i}'])
        value = int(request.form[f'value{i}'])
        category=int(request.form[f'divisible{i}'])
        names.append(name)
        weights.append(weight)
        values.append(value)
        types.append(category)
        items.append(item(name,weight,value,category))

    # if all products are indivisible it will choose 0/1 knapsack method
    global notincluded
    if 1 not in types:
        result,graph_data,notincluded=knapsack_dynamic_programming(items, capacity)
    else:
        objs=[]
        for i in range(len(weights)):
            if types[i]==1:
                item_type='Divisible'
            else:
                item_type='InDivisible'
            obj=item(names[i],weights[i],values[i],item_type)
            objs+=[obj]
        
        
        result,graph_data,notincluded=knapsack_frac(objs,capacity)

    optimal_solution = result[0]
    selected_products = result[1]
    global total_weight
    global rem_weight
    total_weight=result[2]
    rem_weight=result[3]
    global selp
    global noti
    global wt
    selp=""
    noti=""
    for i in selected_products:
        selp+=i.name+","
    for i in notincluded:
        noti+=i.name+","
    
    if rem_weight<=10:
        wt=10
    elif rem_weight>10 and rem_weight<=20:
        wt=20
    else:
        wt=0
    if 1 not in types:
        graph1(graph_data)
    else:
        graph(graph_data)
    if notincluded==[] or rem_weight>20:
        return render_template('result1.html', optimal_solution=optimal_solution, selected_products=selp[:-1])
    else:
        return render_template('result2.html', optimal_solution=optimal_solution, selected_products=selp,not_included=noti[:-1])

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/final1')
def final1():
    return render_template('summary_yes.html', selected_products=selp[:-1],
                           not_included=noti[:-1],total_weight=total_weight,
                           rem_weight=rem_weight,wt=wt)

@app.route('/final2')
def final2():
    return render_template('summary_no.html', selected_products=selp[:-1],
                           not_included=noti[:-1],total_weight=total_weight,
                           rem_weight=rem_weight,wt=wt)

@app.route('/deliverydetails',methods=['GET','POST'])
def details():
    global uf_name
    global ul_name
    global u_mail
    global u_address
    global u_phone
    if request.method=='POST':
        uf_name=request.form['fname']
        ul_name=request.form['lname']
        # u_mail=request.form['em']
        u_address=request.form['add']
        u_phone=request.form['num']
        return render_template('loading.html')
    return render_template('delivery_details.html')

@app.route('/finalpage')
def finalpage():
    return render_template('loading.html')

@app.route('/finalpage1')
def finalpage1():
    cost=calculate_price(total_weight+wt,u_address)
    mail_msg=f'Thanks for choosing our service!\nYour order has been confirmed\n\nShipment Details:\n{uf_name} {ul_name}\n{u_address}\n{u_phone}\n\nTotal cost:{cost}'
    Send_Mail(session['mail'],mail_msg)
    session['cost']=cost
    return render_template('finalpage.html',cost=cost)

if __name__ == '__main__':
    app.run(debug=True)
import matplotlib.pyplot as plt
import pandas as pd
from adt import item
import numpy as np

def knapsack_frac(items, capacity):

    #intializing value/weight table of all items
    vw_table=[]     
    v_table=[]
    capacity2=capacity
    
    graph_weight=[]  
    graph_name=[]
    graph_value=[]
    graph_vw=[]

    for i in range(len(items)):
        #adding each item along with its value by weight ratio
        vw_table+=[(items[i],items[i].value/items[i].weight)]
        v_table+=[(items[i],items[i].value)]
        graph_name+=[items[i].name]
        graph_value+=[items[i].value]
        graph_weight+=[items[i].weight]
        graph_vw+=[items[i].value/items[i].weight]

    graph_table=[graph_name,graph_value,graph_weight,graph_vw]

    #sorting based on the value by weight ratio
    vw_table=sorted(vw_table,key=lambda x:x[1],reverse=True)
    v_table=sorted(v_table,key=lambda x:x[1],reverse=True)

    included_items_vw=[]
    tot_val_vw=0
    tot_weight_vw=0
    rem_weight_vw=0

    #checking whether the item is divisible or can be packed inside the box
    for i in vw_table:
        item_weight=i[0].weight
        if item_weight<=capacity:
            capacity-=item_weight
            tot_weight_vw+=item_weight
            included_items_vw+=[i[0]]
            tot_val_vw+=i[0].value
        else: 
            if i[0].type=='Divisible':
                tot_weight_vw+=capacity
                rem_weight_vw+=item_weight-capacity
                tot_val_vw+=(i[1]*capacity)
                break
            rem_weight_vw+=item_weight
        
    vw_output=(tot_val_vw,included_items_vw,tot_weight_vw,rem_weight_vw)

    included_items_v=[]
    tot_val_v=0
    tot_weight_v=0
    rem_weight_v=0

    for i in v_table:
        item_weight=i[0].weight
        if item_weight<=capacity2:
            capacity2-=item_weight
            tot_weight_v+=item_weight
            included_items_v+=[i[0]]
            tot_val_v+=i[0].value
        else: 
            if i[0].type=='Divisible':
                tot_weight_v+=capacity2
                rem_weight_v+=item_weight-capacity2
                tot_val_v+=((i[1]/i[0].weight)*capacity2)
                break
            rem_weight_v+=item_weight
    
    #returning result
    v_output=(tot_val_v,included_items_v,tot_weight_v,rem_weight_v)

    result=max(v_output,vw_output)

    notincluded=[]
    for i in items:
        if i not in result[1]:
            notincluded.append(i)
    
    graph_table+=[[tot_val_v,tot_weight_v,rem_weight_v],[tot_val_vw,tot_weight_vw,rem_weight_vw]]
    return (graph_table)

i1=item('fan',10,60,'Divisible')
i2=item('car',20,100,'Divisible')
i3=item('bike',30,120,'InDivisible')
l=[i1,i2,i3]
result=knapsack_frac(l,50)
print(result)

def graph(result):
    label=result[0]
    values=result[1]
    weights=result[2]
    vw=result[3]
    max_val=max(values)
    max_wei=max(weights)
    max_vw=max(vw)
    exp_val=[0.1 if x==max_val else 0 for x in values]
    exp_vw=[0.1 if x==max_vw else 0 for x in vw]
    
    #plot the pie chart
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(6,5))
    ax1.pie(values, labels=label, autopct='%0.1f%%',explode=exp_val)
    ax1.set_title('value factor')
    ax2.pie(vw, labels=label, autopct='%1.1f%%',explode=exp_vw)
    plt.subplots_adjust(wspace=0.4)
    ax2.set_title('value/weight factor')
    plt.savefig('static/graph1.png')
    plt.close()
    
    # Plot the line chart
    plt.plot(label,weights,'o-')
    plt.plot(label,values,'o-')
    plt.plot(label,vw,'o-')
    plt.legend(['weights','values','v/w ratio'])
    plt.savefig('static/graph2.png')
    plt.close()

    # plot the bar chart
    y=result[4]
    z=result[5]
    x_label=['total profit','total weight packed','remainin weight']
    X_axis = np.arange(len(x_label))
    plt.bar(X_axis - 0.2, y, 0.4, label = 'priority-values')
    plt.bar(X_axis + 0.2, z, 0.4, label = 'priority-value/weight')
    plt.xticks(X_axis, x_label)
    plt.legend()
    plt.savefig('static/graph3.png')
    plt.close()
try:   
    graph(result)
except:
    pass
import matplotlib.pyplot as plt
import pandas as pd
from adt import item

def knapsack_frac(items, capacity):

    #intializing value/weight table of all items
    vw_table=[]
    graph_table=[]     

    for i in range(len(items)):
        #adding each item along with its value by weight ratio
        vw_table+=[(items[i],items[i].value/items[i].weight)]
        graph_table+=[(items[i].name,items[i].value,items[i].weight,items[i].value/items[i].weight)]
    
    #sorting based on the value by weight ratio
    vw_table=sorted(vw_table,key=lambda x:x[1],reverse=True)

    included_items=[]
    tot_val=0
    tot_weight=0

    #checking whether the item is divisible or can be packed inside the box
    for i in vw_table:
        item_weight=i[0].weight
        if item_weight<=capacity:
            capacity-=item_weight
            tot_weight+=item_weight
            included_items+=[i[0].name]
            tot_val+=i[0].value
        else: 
            if i[0].type=='Divisible':
                tot_weight+=capacity
                included_items+=[i[0].name]
                tot_val+=(i[1]*capacity)
                break
    
    #returning result
    return (tot_val,included_items,tot_weight,graph_table)

i1=item('fan',60,120,'Divisible')
i2=item('car',30,180,'Divisible')
i3=item('bike',40,120,'InDivisible')
l=[i1,i2,i3]
result=knapsack_frac(l,50)
print(result[0],result[1])
df=pd.DataFrame(result[3],columns=['name','value','weight','vw_ratio'])

ax = plt.gca()
 
# line plot for math marks
df.plot(kind='line',
        x='name',
        y='weight',
        color='green', ax=ax)
 
# line plot for physics marks
df.plot(kind='line', x='name',
        y='value',
        color='blue', ax=ax)
 
# line plot for chemistry marks
df.plot(kind='line', x='name',
        y='vw_ratio',
        color='black', ax=ax)
 
# set the title
plt.title('LinePlots')
 
# show the plot
plt.savefig('static/graph2.png')
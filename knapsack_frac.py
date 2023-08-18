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
            if i[0].type=='Divisible' and item_weight<=capacity:
                tot_weight_vw+=capacity
                rem_weight_vw+=item_weight-capacity
                tot_val_vw+=(i[1]*capacity)
                included_items_vw+=[i[0]]
                break
            rem_weight_vw+=item_weight
        
    vw_output=(tot_val_vw,included_items_vw,tot_weight_vw,rem_weight_vw)
    print(vw_output)

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
            if i[0].type=='Divisible'and item_weight<=capacity2:
                tot_weight_v+=capacity2
                rem_weight_v+=item_weight-capacity2
                tot_val_v+=((i[1]/i[0].weight)*capacity2)
                included_items_v+=[i[0]]
                break
            rem_weight_v+=item_weight
    
    #returning result
    v_output=(tot_val_v,included_items_v,tot_weight_v,rem_weight_v)
    print(v_output[0])

    result=max(v_output,vw_output,key=lambda x:x[0])

    notincluded=[]
    for i in items:
        if i not in result[1]:
            notincluded.append(i)
    # if result[1][-1].type=="Divisible":
    #     notincluded.append(result[1][-1])
    
    graph_table+=[[tot_val_v,tot_weight_v,rem_weight_v],[tot_val_vw,tot_weight_vw,rem_weight_vw]]

    print(result)
    return result,graph_table,notincluded

if __name__=='__main___':
    from adt import item
    i1=item('fan',10,60,'InDivisible')
    i2=item('car',20,100,'Divisible')
    i3=item('bike',30,120,'InDivisible')
    l=[i1,i2,i3]
    result=knapsack_frac(l,50)
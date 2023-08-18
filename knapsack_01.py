
from adt import item
def knapsack_dynamic_programming(items, capacity):
    n = len(items)
    names=[]
    weights=[]
    values=[]
    
    for itm in items:
        names.append(itm.name)
        weights.append(itm.weight)
        values.append(itm.value)
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
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    included = []
    tot_weight=0
    combinations=[]
    comb_vals=[]
    i, w = n, capacity
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            included.append(i - 1)
            comb_vals.append(dp[i][w])
            combinations.append(",".join([items[x].name for x in included]))
            tot_weight+=weights[i-1]
            w -= weights[i - 1]
        i -= 1

    included.reverse()
    included_itemlist=[items[i] for i in included]
    rem_weight=0
    for i in range(len(weights)):
        if i not in included:
            rem_weight+=weights[i]
    notincluded=[]
    for i in items:
        if i not in included_itemlist:
            notincluded.append(i)
    graph_table+=[combinations]
    graph_table+=[comb_vals]
    return (dp[n][capacity],included_itemlist,tot_weight,rem_weight),graph_table,notincluded



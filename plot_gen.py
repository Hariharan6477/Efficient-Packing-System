import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def graph(result):
    matplotlib.use('agg')
    try:
        label=result[0]
        values=result[1]
        weights=result[2]
        vw=result[3]
        max_val=max(values)
        max_wei=max(weights)
        max_vw=max(vw)
        exp_val=[0.1 if x==max_val else 0 for x in values]
        exp_vw=[0.1 if x==max_vw else 0 for x in vw]
        
        #plot the pie
        fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.pie(values, labels=label, autopct='%1.1f%%',explode=exp_val)
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
        plt.xlabel("Products")
        plt.ylabel("Values (Rs) and Weights (kg)")
        plt.legend(['weights','values','v/w ratio'])
        plt.savefig('static/graph2.png')
        plt.close()

        # plot the bar chart
        y=result[4]
        z=result[5]
        x_label=['total profit','total weight packed','remaining weight']
        X_axis = np.arange(len(x_label))
        plt.bar(X_axis - 0.2, y, 0.4, label = 'priority-values')
        plt.bar(X_axis + 0.2, z, 0.4, label = 'priority-value/weight')
        plt.xticks(X_axis, x_label)
        plt.xlabel("Category-wise Statistics")
        plt.ylabel("Values (Rs.) and Weights (kg)")
        plt.legend()
        plt.savefig('static/graph3.png')
        plt.close()
    except:
        pass
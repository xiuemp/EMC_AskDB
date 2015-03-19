import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def pie(heads, pie_dict, output_path="./"):
    """ 
    Make a pie chart by input lists
    """
    colors  = ["pink","lightskyblue","yellow","yellowgreen","coral","orange","lightcoral","gold"]

    title = heads[0]
    total_count = heads[-1]
    labels = pie_dict.keys()
    labels.sort()
    quants = []
    for key in labels:
        quants.append(pie_dict[key])

    fig = plt.figure(1, figsize=(6,6))
    plt.pie(quants, explode=None, colors=colors, labels=labels, \
        autopct='%1.1f%%',pctdistance=0.8)

    plt.title(title, fontsize = 20)
    plt.text(1, 1, "total: "+str(total_count))

    #plt.show()
    fig.savefig(output_path+title.replace(" ","_")+".png")
    #clear the cavas or it will overlap 
    plt.clf()

    return title.replace(" ","_")+".png"

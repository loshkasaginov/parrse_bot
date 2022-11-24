import matplotlib.pyplot as plt
import numpy as np


def create_graph(avg, vacancy):
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    ax.bar(['москва', 'санкт-питербург', 'Екатеринбург', 'Новосибирск', 'украина'],
           [avg[0][0], avg[1][0], avg[2][0], avg[3][0], avg[4][0]], color='red', label="avg salary", alpha=0.8)
    ax.legend(f'avg {vacancy} salary')
    plt.savefig(f'images/{vacancy}.png', transparent=True)
    #plt.show()

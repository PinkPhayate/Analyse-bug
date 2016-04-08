import pandas as pd
import matplotlib.pyplot as plt
def draw_grph(num,exNum,mdl_typ1,exNum2,mdl_typ2):

    THRESHOLD = 0.5
    filename = './../result/ex'+str(exNum)+'/record_ex'+str(exNum)+'_'+mdl_typ1+'_'+str(THRESHOLD)+'.csv'
    df = pd.read_csv(filename, header=0)
    vers = df.index
    value = df['f_value']
    plt.plot(vers, value, label=str(exNum)+'_'+mdl_typ1, color = 'blue')

    filename = './../result/ex'+str(exNum2)+'/record_ex'+str(exNum2)+'_'+mdl_typ2+'_'+str(THRESHOLD)+'.csv'
    df = pd.read_csv(filename, header=0)
    vers = df.index
    value = df['f_value']
    plt.plot(vers, value, label=str(exNum2)+'_'+mdl_typ2, color = 'red')

    # plt.xticks( df['version'], df.index ) # location, labels
    plt.xticks([0,1,2,3], ['4.1.0','4.2.0','4.3.0','4.4.0'])

    # figure environment
    plt.legend(loc='upper left')
    plt.xlabel('version')
    plt.ylabel('F-value')

    # save figure
    filename = './../result/figure/ex'+str(num)+'.png'
    plt.savefig(filename)
    plt.clf

def draw_graph(exNum):
    draw_grph(exNum,exNum,'nml',exNum,'rfn')


if __name__ == '__main__':
    # draw_grph('1','1','nml','1','rfn')
    # draw_grph('2','2','nml','2','rfn')
    draw_grph(3,1,'rfn',2,'rfn')

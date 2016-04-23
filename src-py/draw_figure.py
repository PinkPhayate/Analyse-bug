import pandas as pd
import matplotlib.pyplot as plt
import version
def draw_grph(num,exNum,mdl_typ1,exNum2,mdl_typ2):

    THRESHOLD = 0.5
    filename = './../result/ex'+str(exNum)+'/record_ex'+str(exNum)+'_'+mdl_typ1+'_'+str(THRESHOLD)+'.csv'
    print filename
    df = pd.read_csv(filename, header=0)
    df = df.sort_index(ascending=False)
    vers = df.index
    value = df['f_value']
    print value
    plt.plot(vers, value, label=str(exNum)+'_'+mdl_typ1, color = 'blue')

    filename = './../result/ex'+str(exNum2)+'/record_ex'+str(exNum2)+'_'+mdl_typ2+'_'+str(THRESHOLD)+'.csv'
    print filename
    df = pd.read_csv(filename, header=0)
    df = df.sort_index(ascending=False)
    vers = df.index
    value = df['f_value']
    print value
    plt.plot(vers, value, label=str(exNum2)+'_'+mdl_typ2, color = 'red')

    # plt.xticks( df['version'], df.index ) # location, labels
    plt.xticks([0,1,2,3], ['4.1.0','4.2.0','4.3.0','4.4.0'])

    # figure environment
    plt.legend(loc='upper left')
    plt.xlabel('version')
    plt.ylabel('F-value')

    # save figure
    filename = './../result/figure/ex'+str(num)+'_'+mdl_typ1+'_'+mdl_typ2 + str(THRESHOLD) +'.png'
    plt.savefig(filename)
    plt.clf

def draw_grph3(num,exNum,mdl_typ1,exNum2,mdl_typ2,exNum3,mdl_typ3):

    THRESHOLD = 0.5

    filename = './../result/ex'+str(exNum)+'/record_ex'+str(exNum)+'_'+mdl_typ1+'_'+str(THRESHOLD)+'.csv'
    print filename
    df = pd.read_csv(filename, header=0)
    df = df.sort_index(ascending=False)
    vers = df.index
    value = df['f_value']
    print value
    plt.plot(vers, value, label=str(exNum)+'_'+mdl_typ1, color = 'blue')

    filename = './../result/ex'+str(exNum2)+'/record_ex'+str(exNum2)+'_'+mdl_typ2+'_'+str(THRESHOLD)+'.csv'
    print filename
    df = pd.read_csv(filename, header=0)
    df = df.sort_index(ascending=False)
    vers = df.index
    value = df['f_value']
    print value
    plt.plot(vers, value, label=str(exNum2)+'_'+mdl_typ2, color = 'red')

    filename = './../result/ex'+str(exNum3)+'/record_ex'+str(exNum3)+'_'+mdl_typ3+'_'+str(THRESHOLD)+'.csv'
    print filename
    df = pd.read_csv(filename, header=0)
    df = df.sort_index(ascending=False)
    vers = df.index
    value = df['f_value']
    print value
    plt.plot(vers, value, label=str(exNum3)+'_'+mdl_typ3, color = 'green')

    # plt.xticks( df['version'], df.index ) # location, labels
    plt.xticks([0,1,2,3], ['4.1.0','4.2.0','4.3.0','4.4.0'])

    # figure environment
    plt.legend(loc='upper left')
    plt.xlabel('version')
    plt.ylabel('F-value')

    # save figure
    filename = './../result/figure/ex' + str(num) + '_' + mdl_typ1 + '_' + mdl_typ2 + '_' + mdl_typ3 + str(THRESHOLD) + '.png'
    plt.savefig(filename)
    plt.clf


def draw_graph(exNum):
    draw_grph3(exNum,exNum,'nml',exNum,'rfn',exNum,'chrn')



if __name__ == '__main__':
    # draw_graph(1)
    # draw_graph(2)
    # draw_graph(11)
    # draw_graph(12)

#  compare single and mult
    # draw_grph('3','1','nml','2','nml')
    # draw_grph('3','1','rfn','2','rfn')
    # draw_grph('3','1','chrn','2','chrn')

#  compare choised single and choised mult
    # draw_grph('1112','11','nml','12','nml')
    # draw_grph('1112','11','rfn','12','rfn')
    # draw_grph('1112','11','chrn','12','chrn')

#  compare single and choised single
    # draw_grph('1-11','1','nml','11','nml')
    # draw_grph('1-11','1','rfn','11','rfn')
    # draw_grph('1-11','1','chrn','11','chrn')

#  compare mult and choised mult
    # draw_grph('1-12','2','nml','12','nml')
    # draw_grph('1-12','2','rfn','12','rfn')
    draw_grph('1-12','2','chrn','12','chrn')

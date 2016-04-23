import pandas as pd
import version
# version : fileNo : bugNo

fileNums = []
vers = version.get_version_short_list()
for ver in vers:
    fileNum = []
    fileNum.append(ver)

    # get the number of module
    df = pd.read_csv('./../org/solr-' + ver + '/containment.txt', header=None)
    num = df.size
    fileNum.append(num)

    # get the number of bug module
    df = pd.read_csv('./../metrics/numBug/slr_' + ver + '_bgmd.csv', header=None)
    num = df.size
    fileNum.append(num)
    fileNums.append(fileNum)
records = pd.DataFrame(fileNums)
records.columns = ['version', 'moduls', 'bugs']
pd.DataFrame(records).to_csv( './../SOLR-INFORMATION.csv', index=False, cols=None )

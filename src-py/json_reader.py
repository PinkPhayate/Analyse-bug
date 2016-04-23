import json
import version
import pandas as pd

f = open('slr_bug_list.json', 'r')
jsonData = json.load(f)
f.close()

vers = version.get_version_list()
solr_df = []
for ver in vers:
    list = []
    list.append(ver)

    bugs = jsonData.get(ver).get('bug_fix')
    numBug  = len(bugs)
    list.append(numBug)

    df = pd.read_csv('slr_' + ver + '_bgmd.csv', header=0)
    numMod = len(df)
    list.append(numMod)

    print list
    solr_df.appendz(lista)

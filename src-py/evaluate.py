import pandas as pd
import version



def evaluate_ex_report(df,evals,mdl_typ):
    THRESHOLD = 0.5

    evals_df = pd.DataFrame(evals)
    df = pd.concat([df,evals_df] ,axis=1)
    df = df.rename(columns={0:'evaluation'})
    df.to_csv( './../result/ex2/df_ex1_' + mdl_typ + '_' + str(THRESHOLD) + '.csv', index=False, cols=0)

    nm = len(df)
    np = 0.0
    nf = 0.0
    nc = 0.0
    # df = pd.DataFrame(df)
    for row in df.iterrows():
        s = row[-1]
        value = s['evaluation']
        actual = s['fault']
        # print (value,actual)

        if value > THRESHOLD:
            np += 1
        if actual != 0:
            nf += 1
        if value > THRESHOLD and actual != 0:
            nc += 1
    f_value = 2*nc / ( nf + np )

    record = []
    record.append(int(nm))
    record.append(int(np))
    record.append(int(nf))
    record.append(int(nc))
    record.append(f_value)

    return record





def evaluate_ex_merge(exNum,curr_ver):
    THRESHOLD = 0.5

    nml_df = pd.read_csv( './../result/ex'+str(exNum)+'/df_ex'+str(exNum)+'_nml_' + str(THRESHOLD) +'_' + curr_ver + '.csv',  header=0 )
    chrn_df = pd.read_csv( './../result/ex'+str(exNum)+'/df_ex'+str(exNum)+'_chrn_' + str(THRESHOLD) +'_' + curr_ver + '.csv', header=0 )
    chrn_df = chrn_df[['filename','evaluation']]
    chen_df = chrn_df.rename(columns={'evaluation':'chrn_evaluation'})

    df = pd.merge(nml_df, chrn_df, on='filename')

    nm = len(df)
    np = 0.0
    nf = 0.0
    nc = 0.0
    # df = pd.DataFrame(df)
    for row in df.iterrows():
        s = row[-1]
        value = s['evaluation_x']
        chrn_value = s['evaluation_y']
        actual = s['fault']
        # print (value,actual)

        flag = False
        if value > THRESHOLD:
            np += 1
            flag = True
        elif chrn_value > THRESHOLD:
            np += 1
            flag = True
        if actual != 0:
            nf += 1
        if flag and actual != 0:
            nc += 1
    f_value = 2*nc / ( nf + np )

    record = []
    record.append(int(nm))
    record.append(int(np))
    record.append(int(nf))
    record.append(int(nc))
    record.append(f_value)

    return record



def evaluate_merged(exNum):
    THRESHOLD = 0.5
    vers = version.get_version_short_list()
    ev_values = []
    print 'operation starts'
    for curr_ver in vers :
        next_ver = version.get_next_version(curr_ver)
        print curr_ver
        print next_ver
        if curr_ver != '4.5.0':

            ev_value = [curr_ver,]
            ev_value.extend( evaluate_ex_merge(exNum,curr_ver) )
            ev_values.append(ev_value)


    df = pd.DataFrame(ev_values)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df = df.sort_index(ascending=False)
    df.to_csv( './../result/ex'+str(exNum)+'/Mrecord_ex'+str(exNum)+'_' + str(THRESHOLD) + '.csv', index=False, cols=None)


evaluate_merged(1)
evaluate_merged(2)

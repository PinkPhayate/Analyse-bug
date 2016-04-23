import pandas as pd
import statsmodels.api as sm
import version
import numpy as np
import types
record = []
THRESHOLD = 0.5


def create_df_ref (filename) :
    try:
        df = pd.read_csv(filename, header=None)
    except:
        return 'NULL'
    df.columns = ['fileName', 'TCchar', 'LOC','N1','N2','eta1','eta2','N','NN','NF','fault','fileName2','NumOfBug','loc','chum','relatedChum','delectChum','ncdChum','isNewModule']
    # add constant
    df['intercept'] = 1.0
    rfn_df = df[['fileName', 'TCchar', 'LOC', 'N', 'NN', 'NF', 'fault','chum','relatedChum','delectChum','ncdChum', 'intercept']]
    return rfn_df

def nrmlize(df) :
    ndf = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum']]
    ndf = ndf.div(ndf.sum(1),axis=0)
    df =  df[[ 'fault', 'intercept']]
    df = pd.concat([df,ndf] ,axis=1)
    return df

def evaluate_ex(df,evals):
    global THRESHOLD
    global record

    evals_df = pd.DataFrame(evals)
    df = pd.concat([df,evals_df] ,axis=1)
    # df.rename(columns={0:'fault'})

    nm = len(df)
    np = 0.0
    nf = 0.0
    nc = 0.0
    # df = pd.DataFrame(df)
    for row in df.iterrows():
        s = row[-1]
        value = s[-1]
        actual = s['fault']
        # print (value, actual)

        if value > THRESHOLD:
            np += 1
        if actual != 0:
            nf += 1
        if value > THRESHOLD and actual != 0:
            nc += 1
    f_value = 2*nc / ( nf + np )

    record.append(int(nm))
    record.append(int(np))
    record.append(int(nf))
    record.append(int(nc))
    record.append(f_value)

    return df


if __name__ == '__main__':
    ex4()

def ex4():

    global record
    global THRESHOLD
    list = version.get_version_list()
    records = []
    for curr_ver in list :
        if curr_ver != '10.10.2.0':
            next_version = version.get_next_version(curr_ver)
            print curr_ver
            # print next_version

            record = []
            record.append(curr_ver)
            df = create_df_ref('./../data/metrics/METRICS_V' + curr_ver + '.csv')
            # normalize
            df = nrmlize(df)

            # dependent value
            dv_data = df['fault']
            # explanatory value
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            try:
                result = logit.fit()
            except:
                print curr_ver + 'is singular.'
                # result = logit.fit(method='bfgs')
            # print result.summary()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept'])

            # create model used evaluatopn_ex
            df = create_df_ref('./../data/metrics/METRICS_V' + next_version + '.csv')
            # normalize
            df = nrmlize(df)
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            print '---logit_odds---'
            print logit_odds
            evals = logit.cdf(logit_odds)
            print '---evals---'
            print evals

            # operate evaluation_ex
            df = evaluate_ex(df,evals)
            pd.DataFrame(df).to_csv( './../data/result/ex4_ref/result_' + curr_ver + 'ex4_ref.csv', index=False )
            records.append(record)

    pd.DataFrame(records).to_csv( './../data/result/record_ex4_ref_' + str(THRESHOLD) +'.csv', index=False, cols=None )

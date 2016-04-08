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


def evaluate_ex(df,evals):
    global THRESHOLD
    global record

    evals_df = pd.DataFrame(evals)
    df = pd.concat([df,evals_df] ,axis=1)
    df = df.rename(columns={0:'evaluation'})

    nm = len(df)
    np = 0.0
    nf = 0.0
    nc = 0.0
    # df = pd.DataFrame(df)
    for row in df.iterrows():
        s = row[-1]
        value = s['evaluation']
        actual = s['fault']

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
    ex1()

def ex1():
    global record
    global THRESHOLD
    list = version.get_version_list()
    records = []
    for curr_ver in list :
        if curr_ver != '10.10.2.0':
            next_version = version.get_next_version(curr_ver)
            print curr_ver
            print next_version

            record = []
            record.append(curr_ver)
            filename = './../data/metrics/METRICS_V' + curr_ver + '.csv'
            df = create_df_ref(filename)


            # dependent value
            dv_data = df['fault']
            # explanatory value
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()
            # print result.summary()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept'])

            # create model used evaluatopn_ex
            df = create_df_ref('./../data/metrics/METRICS_V' + next_version + '.csv')
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)
            df = evaluate_ex(df,evals)

            # operate evaluation_ex
            pd.DataFrame(df).to_csv( './../data/result/ex1_ref/result_' + curr_ver + 'ex1_ref.csv', index=False, cols=None )
            records.append(record)

    pd.DataFrame(records).to_csv( './../data/result/record_ex1_ref_' + str(THRESHOLD) +'.csv', index=False, cols=None )
def ex1(threshold):
    global record
    global THRESHOLD
    THRESHOLD = threshold
    list = version.get_version_list()
    records = []
    for curr_ver in list :
        if curr_ver != '10.10.2.0':
            next_version = version.get_next_version(curr_ver)
            print curr_ver
            print next_version

            record = []
            record.append(curr_ver)
            filename = './../data/metrics/METRICS_V' + curr_ver + '.csv'
            df = create_df_ref(filename)


            # dependent value
            dv_data = df['fault']
            # explanatory value
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()
            # print result.summary()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept'])

            # create model used evaluatopn_ex
            df = create_df_ref('./../data/metrics/METRICS_V' + next_version + '.csv')
            ev_data = df[['TCchar', 'LOC', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum','intercept']]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)
            df = evaluate_ex(df,evals)

            # operate evaluation_ex
            pd.DataFrame(df).to_csv( './../data/result/ex1_ref/result_' + curr_ver + 'ex1_ref.csv', index=False, cols=None )
            records.append(record)

    pd.DataFrame(records).to_csv( './../data/result/record_ex1_ref_' + str(THRESHOLD) +'.csv', index=False, cols=None )

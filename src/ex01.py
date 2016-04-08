import pandas as pd
import statsmodels.api as sm
import merge_metrics as mm
import version
import draw_figure as fig

# record = []
THRESHOLD = 0.5
nrm_prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF']
ref_prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF','chum','relatedChum','delectChum','ncdChum']


def evaluate_ex(df,evals):
    global THRESHOLD
    # global record

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


def ex1(threshold):
    # global record
    global THRESHOLD
    global nrm_prms
    global ref_prms

    THRESHOLD = threshold
    vers = version.get_version_short_list()
    ev_values_nml = []
    ev_values_ref = []
    print 'operation starts'
    for curr_ver in vers :
        next_ver = version.get_next_version(curr_ver)
        print curr_ver
        print next_ver
        if curr_ver != '4.5.0':
            curr_df = mm.create_df(curr_ver)

            # dependent value
            dv_data = curr_df['fault']
            # explanatory value
            ev_data = curr_df[nrm_prms]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=nrm_prms)
            print coef

            # create model used evaluatopn_ex
            next_df = mm.create_df(next_ver)
            ev_data = next_df[nrm_prms]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( evaluate_ex(next_df, evals) )
            ev_values_nml.append(ev_value)


            # explanatory value
            ev_data = curr_df[ref_prms]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=ref_prms)

            # create model used evaluatopn_ex
            ev_data = next_df[ref_prms]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( evaluate_ex(next_df, evals) )
            ev_values_ref.append(ev_value)



    df = pd.DataFrame(ev_values_nml)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df.to_csv( './../result/ex1/record_ex1_nml_' + str(THRESHOLD) +'.csv', index=False, cols=None)
    df = pd.DataFrame(ev_values_ref)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df.to_csv( './../result/ex1/record_ex1_rfn_' + str(THRESHOLD) +'.csv', index=False, cols=None)





if __name__ == '__main__':
    ex1(0.5)
    fig.draw_graph(1)

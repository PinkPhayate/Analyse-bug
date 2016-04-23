import pandas as pd
import statsmodels.api as sm
import merge_metrics as mm
import merge_metrics_more as mmm
import version
import draw_figure as fig
import ex01

def create_df_used_all_predate_nml (curr_ver) :
    vers = version.get_all_previous_version_list(curr_ver)
    marged_df = pd.DataFrame([])
    print vers
    for ver in vers :
        df = mmm.create_df(ver)
        # print df
        marged_df = pd.concat([marged_df, df])
    return marged_df

def evaluate_ex_report(df,evals,mdl_typ,curr_ver):
    THRESHOLD = 0.5

    evals_df = pd.DataFrame(evals)
    df = pd.concat([df,evals_df] ,axis=1)
    df = df.rename(columns={0:'evaluation'})
    df.to_csv( './../result/ex2/df_ex2_' + mdl_typ + '_' + str(THRESHOLD) +'_' + curr_ver + '.csv', index=False, cols=0)

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


def ex2_short(mdl_typ, threshold):
    if mdl_typ == 'nml':
        prms = ['TCchar', 'CountLineCode', 'CountLineComment', 'N', 'NN', 'NF','SumCyclomatic']
    elif mdl_typ == 'rfn':
        prms = ['TCchar', 'CountLineCode', 'CountLineComment', 'N', 'NN', 'NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum']
    elif mdl_typ == 'chrn':
        prms = ['chum','relatedChum','delectChum','ncdChum']

    THRESHOLD = threshold
    vers = version.get_version_short_list()
    ev_values = []
    print 'operation starts'
    for curr_ver in vers :
        next_ver = version.get_next_version(curr_ver)
        print curr_ver
        print next_ver
        if curr_ver != '4.5.0':
            curr_df = create_df_used_all_predate_nml(curr_ver)

            # dependent value
            dv_data = curr_df['fault']
            # explanatory value
            ev_data = curr_df[prms]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=prms)
            # print coef

            # create model used evaluatopn_ex
            next_df = mmm.create_df(next_ver)
            ev_data = next_df[prms]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            # print logit_odds
            evals = logit.cdf(logit_odds)
            # print evals

            ev_value = [curr_ver,]
            # ev_value.extend( ex01.evaluate_ex(next_df, evals, mdl_typ,curr_ver) )
            ev_value.extend( ex01.evaluate_ex(next_df, evals) )

            ev_values.append(ev_value)


    df = pd.DataFrame(ev_values)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df = df.sort_index(ascending=False)
    df.to_csv( './../result/ex2/record_ex2_' + mdl_typ + '_' + str(THRESHOLD) + '.csv', index=False, cols=None)




if __name__ == '__main__':
    # ex2_short('nml', 0.3)
    # ex2_short('rfn', 0.3)
    ex2_short('nml', 0.5)
    ex2_short('rfn', 0.5)
    ex2_short('chrn', 0.5)

    fig.draw_graph(2)

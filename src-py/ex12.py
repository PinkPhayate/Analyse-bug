import pandas as pd
import statsmodels.api as sm

import merge_metrics_more as mmm
import version
import draw_figure as fig
import ex01
import ex02
import ex11

def ex12_short(mdl_typ):
    if mdl_typ == 'nml':
        prms = ['TCchar', 'CountLineCode', 'CountLineComment' , 'N', 'NN', 'NF','SumCyclomatic']
    elif mdl_typ == 'rfn':
        prms = ['TCchar', 'CountLineCode', 'CountLineComment', 'N', 'NN', 'NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum']
    elif mdl_typ == 'chrn':
        prms = ['chum','relatedChum','delectChum','ncdChum']

    THRESHOLD = 0.5
    vers = version.get_version_short_list()
    ev_values = []
    prm_note = []

    for curr_ver in vers :
        next_ver = version.get_next_version(curr_ver)
        print curr_ver
        print next_ver
        if curr_ver != '4.5.0':
            curr_df = ex02.create_df_used_all_predate_nml(curr_ver)

            # get paramaters that has lowest aic value
            best_prms = ex11.get_best_paramaters(prms, curr_df, curr_ver, mdl_typ)
            # dependent value
            dv_data = curr_df['fault']
            # explanatory value
            ev_data = curr_df[list(best_prms)]

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=best_prms)

            # create model used evaluatopn_ex
            next_df = mmm.create_df(next_ver)
            # explanatory value
            ev_data = next_df[list(best_prms)]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( ex01.evaluate_ex(next_df, evals) )
            ev_values.append(ev_value)

            prm_note.append(curr_ver)
            prm_note.append(best_prms)

    df = pd.DataFrame(ev_values)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df = df.sort_index(ascending=False)
    df.to_csv( './../result/ex12/record_ex12_' + mdl_typ + '_' + str(THRESHOLD) + '.csv', index=False, cols=None)
    df = pd.DataFrame(prm_note)
    df.to_csv( './../result/ex12/prm_note_'+mdl_typ+'.csv', index=False, cols=None)

if __name__ == '__main__':
    # ex1(0.5)
    ex12_short('nml')
    ex12_short('rfn')
    ex12_short('chrn')
    fig.draw_graph(12)

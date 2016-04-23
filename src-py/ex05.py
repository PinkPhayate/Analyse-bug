import pandas as pd
import itertools
import statsmodels.api as sm
import merge_metrics as mm
import version
import draw_figure as fig
import ex01

def get_aic(dv_data,ev_data):
    logit = sm.Logit(dv_data, ev_data)
    result = logit.fit()
    aic = result.aic
    return aic

def ex4_short(mdl_typ):
    if mdl_typ == 'nml':
        prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF','SumCyclomatic']
    elif mdl_typ == 'rfn':
        prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum']
    elif mdl_typ == 'chrn':
        prms = ['chum','relatedChum','delectChum','ncdChum']

    THRESHOLD = 0.5
    vers = version.get_version_short_list()
    ev_values = []
    print 'operation starts'
    for curr_ver in vers :
        next_ver = version.get_next_version(curr_ver)
        print curr_ver
        print next_ver
        if curr_ver != '4.5.0':
            curr_df = mm.create_df(curr_ver)

            prm_dit = {}
            hash_dict = {}
            key = 0
            # dependent value
            dv_data = curr_df['fault']
            # explanatory value
            ev_data = curr_df[prms]
            # get aic
            aic = get_aic(dv_data, ev_data)
            # prm_dit.update(nrm_prms:aic)
            prm_dit[key]=aic
            hash_dict[key]=prms
            key += 1

            length = len(prms)
            for variables in itertools.combinations(prms, length-1):
                # dependent value
                dv_data = curr_df['fault']
                # explanatory value
                ev_data = curr_df[list(variables)]
                # get aic
                aic = get_aic(dv_data, ev_data)
                # prm_dit.update(variables:aic)
                prm_dit[key]=aic
                hash_dict[key]=variables
                key += 1

            print prm_dit
            best_hash = max((v,k) for (k,v) in prm_dit.items())[1]
            best_prms = hash_dict[best_hash]
            # print best_prms

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
            # print coef

            # create model used evaluatopn_ex
            next_df = mm.create_df(next_ver)
            # explanatory value
            ev_data = next_df[list(best_prms)]

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( ex01.evaluate_ex(next_df, evals) )
            ev_values.append(ev_value)


    df = pd.DataFrame(ev_values)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df = df.sort_index(ascending=False)
    df.to_csv( './../result/ex4/record_ex4_' + mdl_typ + '_' + str(THRESHOLD) + '.csv', index=False, cols=None)

if __name__ == '__main__':
    # ex1(0.5)
    ex4_short('nml')
    ex4_short('rfn')
    ex4_short('chrn')
    fig.draw_graph(4)

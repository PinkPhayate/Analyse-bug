import pandas as pd
import statsmodels.api as sm
import merge_metrics as mm
import version
import draw_figure as fig
import ex01

# record = []
THRESHOLD = 0.5
nrm_prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF','SumCyclomatic']
ref_prms = ['TCchar', 'CountLineCode', 'N', 'NN', 'NF','SumCyclomatic','chum','relatedChum','delectChum','ncdChum']

def ex3(threshold):
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
            # normalize
            ev_data = ev_data.div(ev_data.sum(1),axis=0)

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            result = logit.fit()

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=nrm_prms)
            print coef

            # create model used evaluatopn_ex
            next_df = mm.create_df(next_ver)
            # explanatory value
            ev_data = next_df[nrm_prms]
            # normalize
            ev_data = ev_data.div(ev_data.sum(1),axis=0)

            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( ex01.evaluate_ex(next_df, evals) )
            ev_values_nml.append(ev_value)


            # explanatory value
            ev_data = curr_df[ref_prms]
            # normalize
            ev_data = ev_data.div(ev_data.sum(1),axis=0)

            # create mdl
            logit = sm.Logit(dv_data, ev_data)
            try :
                result = logit.fit()
            except:
                print 'Singular matrix occured'

            # get coefficients
            params = result.params.values
            coef = pd.Series(params, index=ref_prms)

            # create model used evaluatopn_ex
            ev_data = next_df[ref_prms]
            # normalize
            ev_data = ev_data.div(ev_data.sum(1),axis=0)


            # operate evaluation_ex
            logit_odds = ev_data.dot(coef)
            evals = logit.cdf(logit_odds)

            ev_value = [curr_ver,]
            ev_value.extend( ex01.evaluate_ex(next_df, evals) )
            ev_values_ref.append(ev_value)



    df = pd.DataFrame(ev_values_nml)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df.to_csv( './../result/ex3/record_ex3_nml_' + str(THRESHOLD) +'.csv', index=False, cols=None)
    df = pd.DataFrame(ev_values_ref)
    df.columns = ['version','nm','np','nf','nc','f_value']
    df.to_csv( './../result/ex3/record_ex3_rfn_' + str(THRESHOLD) +'.csv', index=False, cols=None)

if __name__ == '__main__':
    ex3(0.5)
    fig.draw_graph(3)

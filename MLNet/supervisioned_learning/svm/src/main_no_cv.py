#!/usr/bin/python
# marina von steinkirch @2014
# steinkirch at gmail

''' This program shows the application svm for entire sets '''

import random
import sklearn.svm  as sklsvm
from sklearn import preprocessing
import numpy as np



INPUT_FILE = ['all_neat_n500', 'all_neat_n1000', 'all_neat_n1500', 'all_neat_n2000', 'all_neat_n5000', 'all_neat']



def save_result_final(net_type, output_file, aver_error, aver_error_SVC, aver_error_no, aver_error_SVC_no, aver_error_no1, aver_error_SVC_no1, aver_error_no2, aver_error_SVC_no2):
    ''' Save in a file the final result '''

    with open(output_file, "a") as f:
        f.write(net_type +',' + str(aver_error) + ","  + str(aver_error_SVC) + ',' + str(aver_error_no) + ',' + str(aver_error_SVC_no) + ',' + str(aver_error_no1) + ',' + str(aver_error_SVC_no1) + ',' + str(aver_error_no2) + ',' + str(aver_error_SVC_no2) + "\n")


def fit_model(data, truth, Chere=1.0):
    # Dual select the algorithm to either solve the dual or primal optimization problem. Prefer dual=False when n_samples > n_features.
    model = sklsvm.LinearSVC(dual=False, C=Chere) 
    model = model.fit(data, truth) 
    return model


def fit_model_SVC(data, truth):
    model = sklsvm.SVC() 
    model = model.fit(data, truth) 
    return model   


def classify_data(model, data, truth):
    guesses = model.predict(data)
    right = np.sum(guesses == truth)
    return float(right) / truth.shape[0]
    

def load_data(datafile_name):
     ''' Load the data and separate it by feature
         and labels '''
     data = np.loadtxt(datafile_name, delimiter = ',')

     # features
     X = data[:,:-1] 

     # label
     Y = data[:,-1]
     return X, Y




def main():


    OUTPUT_FILE_TRAIN = '../output/ALL_NO_CV_train.data'
    with open(OUTPUT_FILE_TRAIN , "w") as f:
        f.write('# net name, net number, dataset, accur LinearSVC, accur SVC(rgb), accur LinearSVC_no, accur SVC(rgb)_no, accur LinearSVC_no1, accur SVC(rgb)_no1 , accur LinearSVC_no2, accur SVC(rgb)_no2 \n')

    OUTPUT_FILE_TEST = '../output/ALL_NO_CV_test.data'
    with open(OUTPUT_FILE_TEST , "w") as f:
        f.write('# net name, net number, dataset, accur LinearSVC, accur SVC(rgb), accur LinearSVC_no, accur SVC(rgb)_no, accur LinearSVC_no1, accur SVC(rgb)_no1 , accur LinearSVC_no2, accur SVC(rgb)_no2\n')
        
   
    for net_type in INPUT_FILE:
        print net_type
        DATA_TRAIN = '../data/no_cv/' + net_type + '_train.data' 
        DATA_TEST = '../data/no_cv/' + net_type + '_test.data' 

        # load sets
        learn_data_X, learn_data_Y = load_data(DATA_TRAIN)
        predict_data_X, predict_data_Y = load_data(DATA_TEST)

        '''
            We do unscalled first...
        '''

        # classifier linear
        model = fit_model(learn_data_X, learn_data_Y)
        aver_error_train = classify_data(model, learn_data_X, learn_data_Y) 
        aver_error_test = classify_data(model, predict_data_X, predict_data_Y)

        # classifier SVC
        model_SVC = fit_model_SVC(learn_data_X, learn_data_Y)
        aver_error_train_SVC = classify_data(model_SVC, learn_data_X, learn_data_Y) 
        aver_error_test_SVC = classify_data(model_SVC, predict_data_X, predict_data_Y)


        '''
            ... And then scalled by mean/variance by method 1
        '''

        learn_data_X_no = preprocessing.scale(learn_data_X)
        predict_data_X_no = preprocessing.scale(predict_data_X)

        #print learn_data_X_no.mean(axis=0)
        #print learn_data_X_no.std(axis=0)
         
        # classifier linear 
        model = fit_model(learn_data_X_no, learn_data_Y)
        aver_error_train_no = classify_data(model, learn_data_X_no, learn_data_Y) 
        aver_error_test_no = classify_data(model, predict_data_X_no, predict_data_Y)

        # classifier SVC
        model_SVC = fit_model_SVC(learn_data_X_no, learn_data_Y)
        aver_error_train_SVC_no = classify_data(model_SVC, learn_data_X_no, learn_data_Y) 
        aver_error_test_SVC_no = classify_data(model_SVC, predict_data_X_no, predict_data_Y)


        '''
            ... And then scalled by mean/variance by method 2
        '''

        scaler = preprocessing.StandardScaler().fit(learn_data_X)
        learn_data_X_no1 = scaler.transform(learn_data_X)
        predict_data_X_no1 = scaler.transform(predict_data_X)

        # classifier linear 
        model = fit_model(learn_data_X_no1, learn_data_Y)
        aver_error_train_no1 = classify_data(model, learn_data_X_no1, learn_data_Y) 
        aver_error_test_no1 = classify_data(model, predict_data_X_no1, predict_data_Y)

        # classifier SVC
        model_SVC = fit_model_SVC(learn_data_X_no1, learn_data_Y)
        aver_error_train_SVC_no1 = classify_data(model_SVC, learn_data_X_no1, learn_data_Y) 
        aver_error_test_SVC_no1 = classify_data(model_SVC, predict_data_X_no1, predict_data_Y)


        '''
            ... And then scalled by xmin, xmax
        '''

        min_max_scaler = preprocessing.MinMaxScaler()
        learn_data_X_no2 = min_max_scaler.fit_transform(learn_data_X)
        predict_data_X_no2 = min_max_scaler.transform(predict_data_X)

                
        # classifier linear 
        model = fit_model(learn_data_X_no2, learn_data_Y)
        aver_error_train_no2 = classify_data(model, learn_data_X_no2, learn_data_Y) 
        aver_error_test_no2 = classify_data(model, predict_data_X_no2, predict_data_Y)

        # classifier SVC
        model_SVC = fit_model_SVC(learn_data_X_no2, learn_data_Y)
        aver_error_train_SVC_no2 = classify_data(model_SVC, learn_data_X_no2, learn_data_Y) 
        aver_error_test_SVC_no2 = classify_data(model_SVC, predict_data_X_no2, predict_data_Y)



        '''
            Saving everything
        '''
        save_result_final(net_type, OUTPUT_FILE_TRAIN, aver_error_train, aver_error_train_SVC, aver_error_train_no, aver_error_train_SVC_no,  aver_error_train_no1,  aver_error_train_SVC_no1, aver_error_train_no2,  aver_error_train_SVC_no2)
        save_result_final(net_type, OUTPUT_FILE_TEST,  aver_error_test,  aver_error_test_SVC,  aver_error_test_no,  aver_error_test_SVC_no,  aver_error_test_no1,   aver_error_test_SVC_no1, aver_error_test_no2,   aver_error_test_SVC_no2)



    print 'Done!!!'




if __name__ == '__main__':
    main()


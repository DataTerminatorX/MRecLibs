# About

This project aims at implementing different models for recommender system, regardless of running speed and performance. Still under construction.


# Usage

See examples in `test_reclib.py`

# Models

> Tips: 

> 1. Memory based models and matrix factorization models evaluate results on trainY while classification models evaluate on testY. Because the latter contain information of trainY when do modeling, the former don't.

> 2. Usually, sequence models split dataset into train/test/predict by samples while others by time.

* [x] Memory based Models 
    * [ ] User/Item CF models (with different similarity mearsurements)
    * [ ] Content based models
* [ ] Matrix Factorization models
    * [ ] Vanilla SVD
    * [ ] SVD++
* [ ] Classfication Models
    * [ ] Naive Bayes
    * [ ] 
* [ ] Sequence Models
    * [ ] N-gram
    * [ ] LSTM
    * [ ] Time-aware LSTM


## Memory based Models 
Split dataset by time. Have `train` and `predict` mode.

\--------data set--------

|\-- trainX \--|\-- trainY \--|

　　　|\--- predictX \----|

* CF (Collaborative Filtering)
    1. Train: Caculate similarities on **trainX**, tune parameter K (K is number of neighbours), do recommendation, evaluate on **trainY**, find best K
    2. Predict: Re-caculate similarities on **predictX**, fix best K, do recommendation

* CB (Content Based)
    1. Train: Tune parameter D (D is dimension of features), extract features for users and items from **trainX**, calculate similarities, do recommendation, evaluate on **trainY**
    2. Predict: Re-extract features for users and items from **predictX**, calculate similarities, do recommendation

## Matrix Factorization Models
Split dataset by time. Have `train` and `predict` mode

\--------data set--------

|\-- trainX \--|\-- trainY \--|

　　　|\--- predictX \----|

* Vanilla SVD

* SVD++
    1. Train: Tune parameter D (D is dimension of latent features), learn latent features for users and items on **trainX**, evaluate on **trainY**, find best D
    2. Predict: Fix best D, learn latent features for users and items on **predictX**, do recommendation

## Classfication Models
Split dataset by time. Have `train`, `test` and `predict` mode.

\--------data set----------------

|\-- trainX \--|\-- trainY \--|

　　　　|\-- testX \--|\-- testY \--|

　　　　　　　　|\-- predictX\-|

* NB (Naive Bayes)
    1. Train: Extract features from **trainX**, caculate possibilities p(y|x) on **trainX** and **trainY**
    2. Test: Do classification and evaluate on **testX** and **testY** 
    3. Predict: Re-caculate possibilities on **predictX**, do classification

* LR (Logistic Regression)
    1. Train: Extract features from **trainX**, tune parameters e (e is parameter of Sigmoid function) and C (C is coefficient of regularization term), learn model weights on **trainY**
    2. Test: Do classification and evaluate on **testX** and **testY** 
    3. Predict: Re-extract features on **predictX**, fix best e and C, do classification

* XgBoost

## Sequence Models
Split dataset by samples. Have `train`, `test` and `predict` mode.

\--------data set----------------

|\-- train(seqX,seqY) \--|

|\-- test(seqX,seqY) \--|

|\-- predict(seqX)\-|

* N-gram

* LSTM

* Time-aware LSTM


 
# ABOUT

# INSTALL

# USAGE

# MISC
## Pipeline of Different Models
> Tips: Memory based models and matrix factorization models evaluate results on trainY while classification models evaluate on testY. Because the latter contain information of trainY when do modeling, the former don't.

### Memory based models 
Only have train and predict mode.
\--------data set--------
|\-- trainX \--|\-- trainY \--|
　　　|\--- predictX \----|

* CF (Collaborative Filtering)
    1. Train: Caculate similarities on **trainX**, tune parameter K (K is number of neighbours), do recommendation, evaluate on **trainY**, find best K
    2. Predict: Re-caculate similarities on **predictX**, fix best K, do recommendation

* CB (Content Based)
    1. Train: Tune parameter D (D is dimension of features), extract features for users and items from **trainX**, calculate similarities, do recommendation, evaluate on **trainY**
    2. Predict: Re-extract features for users and items from **predictX**, calculate similarities, do recommendation

* SL (Sequence Learning)

### Matrix factorization models
Only have train and predict mode
\--------data set--------
|\-- trainX \--|\-- trainY \--|
　　　|\--- predictX \----|

* SVD++
    1. Train: Tune parameter D (D is dimension of latent features), learn latent features for users and items on **trainX**, evaluate on **trainY**, find best D
    2. Predict: Fix best D, learn latent features for users and items on **predictX**, do recommendation

### Classfication models
Have train, test and predict mode.
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

 
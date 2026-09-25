# Modeling lab notes

Converted from `lab_notes.ipynb`. The text below is unchanged. Notebooks that
have since moved to `archive/model/` are listed in the table below.

| Notebook | Location |
|---|---|
| model_05_ridge_initial, model_05a_ridge_14/15/16, mod_med_02_ridge | `archive/model/` |
| everything else mentioned below | `model/` |

The `mod_med_3f_*` notebooks are the ones the notes call `model_median_03f_*`.

Recovered in 2026 from the original working folder (not in the notes below):
`model_02_raw` (builds `ModelAll.csv` from `ModelData.csv`),
`make_prediction_dates` and `make_prediction_data` (build the prediction grid),
`report_support` and `report_text` (figures and text for the final report).
`modl_med_02-ridge`, `p2` and `itch` are in `archive/model/`.

---

* make\_modeling_data: build some preprocessing into the dataset



* model\_01: explore a number of modeling options (statsmodels, sklearn, seaborn) with feature subsets

* model\_02: find best OLS (polynomial) model for one feature, *time*.  Check for overfitting.  Best poly degree: 18, $R^2$: 0.455

* model\_03: find best OLS (polynomial) model for two features, *time*, *size\_kw*.  Check for overfitting.  Best poly degree: 14, $R^2$: 0.517

* __model\_04: find best OLS (polynomial) model for three features, *time*, *size\_kw*, *state*.  Requires excluding one-hot encoded *state* from polynomial expansion.  Best poly degree: 14, $R^2$: 0.534.__

* model_05_ridge_initial: initial experiments with ridge regressor.  some potentially useful code dealing with coeffients and alpha selection.  no useful modeling results.

* model_05_ridge_14: at polynomial 14, adding L2 regularization doesn't add any significant increase in  $R^2$ . The best Ridge alpha was 0.8 with $R^2$  of 0.534, the same as OLS.  Try more flexible model with regularization.

* model_05_ridge_15: same results best Ridge alpha was 0.8 with $R^2$  of 0.534 

* model_05_ridge_16: very small increase in $R^2$. The best Ridge alpha was 0.05 with $R^2$ of 0.5344, still essentially the same as OLS. This is more change than we've seen at deg 14 and 15. Also alpha is moving significantly compared to earlier models. It seems worthwhile to go to degree 17 and see if that trend continues.

* model_05_ridge_17: best Ridge alpha: 1.0, Best R squared: 0.535.  Apparently, ridge isn't going to help here.  Conclusion: model is not overfit.  Weak $R^2$ is result of noise in the data.

* model_06_lasso_b: for completeness try lasso. Best Lasso alpha: 0.0001, poly degree: 17; Best test R squared: 0.526.  Same conclusion as ridge.

* __model_08_random_forest__: Best parameters: {'RFR__max_depth': 15, 'RFR__n_estimators': 20} Best R squared: 0.596.  The Random Forest Regressor on the raw dataset provides an interesting contrast to linear regression with polynomial features. The test  $R^2$  is a very respectable 0.596. This is a better score than OLS with best polynomial features. 

    The best parameters were found using cross-validation with both models to find the overfitting boundary and then the best model was run against the test set to assess generalization capability.  Unfortunately, it would seem that RFR gets its relatively strong $R^2$ by capturing some of the noise.  It is not penalized because both the training and test sets are both noisy, each having been selected from the same (noisy) data set.  For this reason, I find the predictions unsuitable for client recommendations.

* __model_median_01_linear__: Quick rework to get numbers for poly 1 (linear).

    Median by weeks gets $R^2$ of 0.715

* __model_median_01__: A different approach - model the median cost_per_watt.  This has the advantage of strong noise rejection.  The median doesn't care how much higher a value is than the mean. Median finds the 50 percentile price within a group whether the group variance is high or low.

    Here we use OLS to model median cost as (polynomial) function of one variable, time.  Both the weekly and daily median provide strong polynomial models with __reasonable extrapolation__ for 6-8 quarters.    __Weekly median best poly degree is 8 with $R^2$: 0.849__.  Daily median best poly degree is 8, with $R^2$: 0.753.  Monthly best $R^2$: 0.747 at poly degree 13; predictions very unstable.

* __model_median_02__: OLS model median of cost as (polynomial) function of two variables, time and size.  Size is grouped into 2.5kw wide bins. 

    __Monthly median model__ has the following characteristics:
    RMSE (test): __0.689__; Best poly_degree: 8; test R squared: __0.863__.  Makes __stable__ predictions.  Reducing the poly degree produces even more stable predictions at relatively small cost in $R^2$.  Weekly median is slightly weaker ($R^2$: 0.83, poly degree 9).  Also provides stable predictions.  Daily median is  weaker yet ($R^2$: 0.74, poly degree 10).  Provides stable predictions.

* model_median_03f_month, model_median_03f_week, model_median_03f_day: OLS model median of cost as (polynomial) function of 3 variables, time, size and state (one-hot encoded, 18 columns).   Again, we exclude the state columns from polynomial expansion.  As before, size is grouped into 2.5kw wide bins.  Including the state information doesn't help accuracy or prediction.

    Days: Best parameters: {'features__num_vars__poly__degree': 8} test R squared: 0.681; unstable predictions; reduce to 6th degree for better shape.

    Weeks: Best parameters: {'features__num_vars__poly__degree': 8}; test R squared: 0.721; unstable predictions; reduce to 7th or 6th degree for better shape.

    Months: Best parameters: {'features__num_vars__poly__degree': 6}; test R squared: 0.7453698270008948; 7th looks more reasonable, 3rd also.



---

---

### Other thoughts

#### Perhaps we should be using only the biggest groups for prediction because they have best noise characteristic.  In fact, size groups 1, 2 and 3 are by far the largest groups.  

    If we use size groups 1, 2 and 3, predictions stabilize.

#### Some of the predictions have okay shape but are too radical; would regularization calm them down?

    Regularization helps a little but not enough to find optimal setting (it would be near 1.0).

#### Should try RFR on median to compare with OLS poly.

    Also, do a prediction for the raw day RFR model.



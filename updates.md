### 08/06
- Recursive 30-day forecast
    - Starting analysis
    - Adding pseudocode

### 08/07
- Database
    - Writing scripts to update database tables with new data

### 08/08
- Database
    - Consolidating database scripts into classes for more flexibility

### 08/09
- Databse
    - Cleaning up the database scripts and the ETL process

### 08/10
- Recursive 30-day forecast
    - Fitting training data for multi-forecast recursive analysis

### 08/11
- Database
    - added query_to_df method to Database class
- Recursive 30-day forecast
    - Discovered problems with scaling process that is causing model to predict the same values
    - Learned not to use scaler.inverse_transform() as it only inverse scales the prediction values back to the training value ranges. Will have to manually inverse scale predictions with mean/standard deviations from now on.
    - Need to figure out how to fit data recursively

### 08/13
- Recursive 30-day forecast
    - Duplicated predictions still exists despite new scaling method. Found the reason for this is from the tuned parameters from the XGBoost analysis. Will have to figure out what to do in the future to solve that. Will stick with new scaling process for now.
    - Implement recursive model next time

### 08/14
- Recursive 30-day forecast
    - Ran model on train and valid sets
    - Pipeline seems to be working but resutls show later predictions have less errors than earlier predictions which is odd. Will have to research if this is normal
    - Next time compare results of original scaling method to new method

### 08/15
- Recursive 30-day forecast
    - Finished running model on test set
    - Swapped back old scaling method. The new scaling method must be limiting the scaling range to the older data (newer data are higher in value since asset prices tend to appreciate)

### 08/17
- Recursive 30-day forecast
    - Experimenting with the top 4 best performing models from the direct multi-day forecast analysis
    - Running GridSearchCV for parameter tuning for each of the 4 algorithms

### 08/18
- Recursive 30-day forecast
    - Finished GridSearchCV parameter tuning
    - Rmse increased with the optimal parameters
    - Reverting back to default parameters for each model
    - Finished analysis conclusion

### 08/20
- Uploaded updates.md

### 8/23
- Database
    - Added following tables
    - equities - VVIX (volatility of VIX)
    - equities - VXN (volatility of Nasdaq 100) tickers
    - economics - DTWEXBGS (Traded weighted US dollar index)
    - economics - GOLDAMGBD228NLBM (Gold fixing price)
    - updated data

### 8/24
- 30-day forecast with equities indicator
    - preparing data
    - adding individual S&P-500 tickers
- Database
    - added TIP etf

### 8/25
- 30-day forecast with equities indicator
    - setting up ETFs, VIX, DIX data

### 8/27
- 30-day forecast with equities indicator
    - more setting up and cleaning

### 8/29
- 30-day forecast with equities indicator
    - cleaning scaling process

### 9/3
- 30-day forecast with equities indicator
    - setting up model and plotting functions

### 12/24
- updates to accessing server credentials
- fixed depreciated method in Fred
- switch to ssh auth

### 02/07/2021
- test
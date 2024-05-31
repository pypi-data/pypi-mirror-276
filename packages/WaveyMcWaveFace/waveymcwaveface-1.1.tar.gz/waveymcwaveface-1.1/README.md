# wavey
Wavey is a simple implementation of the Google TiDE model in the pytorch framework.  TiDE takes in both categorical
and continuous variables as well as a weight factor to help with time series models that depend on some weight for 
their ultimate scoring outcome.  

## InPuts
data: a pandas dataframe
embedding_dims: the size/dimensions of the embedding layer (usually the square root of the number of unique values
target_size: # of months to forecast out
test_size: % of data to test model on
random_state: integer for reproducibility 



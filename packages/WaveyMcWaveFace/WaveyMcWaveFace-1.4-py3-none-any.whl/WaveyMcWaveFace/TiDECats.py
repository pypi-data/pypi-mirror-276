import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
import numpy as np
from .utils.tide import TiDE


def run_the_model(df, snapshot, target, weights, categorical_variables, embedded_column_number,
                  target_size, model_name, location=None):
    """
    :param df: pandas dataframe of data.  If location==None, index should be date, item, snapshot
    :param snapshot: str forecast snapshot date format = "%Y-%m-%d"
    :param location: None unless forecasting below market then str value
    :param target: list of target columns (multiple columns for mulitple outouts i.e. more than 1 month of forecast)
    :param weights: list of columns to be used as weights (i.e. revenue for sales forecast)
    :param categorical_variables: list of columns that are categorical
    :param embedded_column_number: list of columns that are numerical
    :param target_size: integer of number of forecasted values in the future (i.e. 12 for 12 month forecast)
    :param model_name: str for the name of the model
    :return: dataframe of forecasts
    """

    df_ = df
    # iso_hub_market_ = iso_hub_market
    snapshot_ = snapshot
    target_ = target
    weights_ = weights
    categorical_variables_ = categorical_variables
    embedded_column_number_ = embedded_column_number
    target_size_ = target_size
    model_name_ = model_name
    location_ = location

    df_['month'] = df_.index.get_level_values(0).month

    if location is not None:
        if df_.index.get_level_values(3).nunique() > 1:
            raise Exception(f"df_full has {df_.index.get_level_values(3).nunique()} snapshots in the dataset")
    else:
        if df_.index.get_level_values(2).nunique() > 1:
            raise Exception(f"df_full has {df_.index.get_level_values(3).nunique()} snapshots in the dataset")
        idx = df_.groupby(['fcast_item', 'snapshot']).apply(
            lambda x: x.index.get_level_values('dmand_yr_mo').max())

        # # Creating a DataFrame from idx to reset its index and correct column names
        idx_df = idx.reset_index()
        idx_df.columns = ['fcast_item', 'snapshot', 'dmand_yr_mo', ]
        idx_df = idx_df[['dmand_yr_mo', 'fcast_item', 'snapshot']]
        # # Creating a proper MultiIndex to use for selection
        multi_idx = pd.MultiIndex.from_frame(idx_df)
        # # Use the properly aligned multi-index to extract the corresponding latest entries to run through the
        # trained model
        forecast_data = df_.loc[multi_idx]

        df_full = df_.loc[~df_.index.isin(forecast_data.index)]
        columns = df_full[categorical_variables].columns
        embedding_dims = []
        for i in categorical_variables[:embedded_column_number_]:
            print(i)
            embedding_dims.append(np.round(np.sqrt(df_full[i].nunique() + 1)).astype('int'))
        print(f"Embedding Dims: {embedding_dims}")

        embedding_variables = categorical_variables_ + target_ + weights_
        data = df_full[embedding_variables]
        print(data[categorical_variables].isna().sum())
        print(f"Running Model")
        # Initialize WaveyMcWaveFace instance
        tide_model = TiDE(data, embedding_dims=embedding_dims, target_size=target_size_)
        # Train the model
        tide_model.train_model(num_epochs=2000, lr=0.001, batch_size=200, patience=25)

        preds = tide_model.predict(new_data=forecast_data[categorical_variables])
        column_names = list(preds.columns)

        forecast_names = ['dmand_yr_mo', 'fcast_item', 'snapshot']
        all_names = forecast_names + column_names
        forecast = pd.concat([forecast_data.reset_index(), preds], axis=1)
        forecast = forecast[all_names]

        forecast.set_index(['dmand_yr_mo', 'fcast_item', 'snapshot'], inplace=True)
        new_var_names = {}
        for col in forecast.columns:
            if col.startswith("Prediction_"):
                # Extract the integer from the column name
                offset = int(col.split("_")[1]) + 1

                # Calculate new dates by adding the offset to the 'snapshot' dates
                new_dates = forecast.index.get_level_values('snapshot') + pd.DateOffset(months=offset)

                # Store the new dates in a dictionary with the original column name as the key
                new_var_names[col] = new_dates

                # Step 3: Melt each Prediction column individually and concatenate
                tidy_frames = []
                for c, new_dates in new_var_names.items():
                    # Temporarily set the new dates as a column for melting
                    forecast['temp_new_date'] = new_dates

                    # Melt this specific column, using the new dates as 'var_name'
                    melted = pd.melt(forecast.reset_index(),
                                     id_vars=["dmand_yr_mo", "fcast_item", "snapshot", 'temp_new_date'],
                                     value_vars=[c], value_name="preds")

                    # Rename 'temp_new_date' to something meaningful and drop unnecessary columns
                    melted.rename(columns={'temp_new_date': 'prediction_date'}, inplace=True)
                    melted.drop(columns=['variable'], inplace=True)

                    # Append to the list of tidy DataFrames
                    tidy_frames.append(melted)

                # Concatenate all the tidy frames together
                df_tidy = pd.concat(tidy_frames)
                df_tidy.drop('dmand_yr_mo', axis=1, inplace=True)
                df_tidy.rename(columns={'prediction_date': 'dmand_yr_mo'}, inplace=True)
                # Optionally, set the desired multi-index again
                df_tidy.set_index(["dmand_yr_mo", "fcast_item", "snapshot"], inplace=True)

                df_tidy['model_name'] = model_name_

                return df_tidy

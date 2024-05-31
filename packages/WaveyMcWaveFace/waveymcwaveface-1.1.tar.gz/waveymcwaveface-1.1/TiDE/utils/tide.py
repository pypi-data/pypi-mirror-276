import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


# Custom Dataset class for handling data and targets
class CustomDataset(Dataset):
    def __init__(self, categorical_data, continuous_data, targets, prices):
        self.categorical_data = categorical_data  # Store the categorical input data array
        self.continuous_data = continuous_data  # Store the continuous input data array
        self.targets = np.log(targets + 1)  # Apply log transformation to targets; +1 to avoid log(0)
        self.prices = np.log(prices + 1)

    def __len__(self):
        return len(self.targets)  # Return the number of samples in the dataset

    def __getitem__(self, idx):
        cat_x = self.categorical_data[idx]  # Get the categorical input data for the specified index
        cont_x = self.continuous_data[idx]  # Get the continuous input data for the specified index
        y = self.targets[idx]  # Get the target value for the specified index
        prices = self.prices[idx]
        # cat_x = torch.tensor(self.categorical_data[idx], dtype=torch.long)
        # cont_x = torch.tensor(self.continuous_data[idx], dtype=torch.float)
        # y = torch.tensor(self.targets[idx], dtype=torch.float)
        # prices = torch.tensor(self.prices[idx], dtype=torch.float)
        return cat_x, cont_x, y, prices  # Return tuples of categorical input, continuous input, and target value


# TiDEModel class defining the neural network architecture
class TiDEModel(nn.Module):
    def __init__(self, input_dims, embedding_dims, num_continuous, output_dim):
        super(TiDEModel, self).__init__()
        # Initialize embedding layers for each categorical feature
        self.embeddings = nn.ModuleList([
            nn.Embedding(num_embeddings, embedding_size) for num_embeddings, embedding_size in
            zip(input_dims, embedding_dims)
        ])
        # Calculate the total size of all embeddings concatenated together
        total_embedding_size = sum(embedding_dims)
        # Define the first fully connected layer, adjusting its input size to include continuous variables
        self.fc1 = nn.Linear(total_embedding_size + num_continuous, 128)
        # Define the output layer
        self.fc2 = nn.Linear(128, output_dim)

    def forward(self, x_cat, x_cont, prices=None):
        # Process each categorical feature through its embedding layer and store the result
        x_embed = [emb(x_cat[:, i]) for i, emb in enumerate(self.embeddings)]
        # Concatenate all the embeddings into a single tensor
        x_embed = torch.cat(x_embed, dim=1)
        # Ensure the continuous data is of the same data type as the embeddings
        # This converts continuous data to float if it isn't already
        x_cont = x_cont.float()
        # Concatenate the embeddings with the continuous variables
        x = torch.cat([x_embed, x_cont], dim=1)
        # Pass the concatenated embeddings and continuous variables through the first fully connected layer
        x = F.relu(self.fc1(x))
        # Pass the result through the output layer
        x = self.fc2(x)
        return x

    def get_embeddings(self, x):
        embeddings = []
        for i, emb in enumerate(self.embeddings):
            indices = x[:, i].long()
            embeddings.append(emb(indices))
        return embeddings


# TiDE class for preprocessing data and training the model
class TiDE:
    def __init__(self, data, embedding_dims, target_size, test_size=0.2, random_state=42):
        self.label_encoders = {}
        self.target_size = target_size  # Add this line to save target_size as an attribute
        self.embedding_dims = embedding_dims
        self.train_prices = None  # Initialize train_prices
        self.val_prices = None  # Initialize val_prices
        # Preprocess the data and get categorical, continuous data, and targets
        cat_data, cont_data, targets, prices = self.preprocess_data(data, target_size)

        # Split data into training and validation sets
        # Note: This assumes cat_data and cont_data are numpy arrays. Adjust as needed for other data types.
        cat_train, cat_val, cont_train, cont_val, self.train_targets, self.val_targets, train_prices, val_prices = train_test_split(
            cat_data, cont_data, targets, prices, test_size=test_size, random_state=random_state)

        # Store training and validation data in dictionaries for easier access
        self.train_data = {'cat': cat_train, 'cont': cont_train}
        self.val_data = {'cat': cat_val, 'cont': cont_val}
        self.train_prices = train_prices
        self.val_prices = val_prices

        # Calculate input dimensions for embedding layers based on categorical data
        input_dims = [len(np.unique(cat_data[:, i])) for i in range(cat_data.shape[1])]
        # Initialize the model with the calculated input dimensions, embedding dimensions, number of continuous features, and output dimension
        self.model = TiDEModel(input_dims, embedding_dims, cont_train.shape[1], target_size)

    def preprocess_data(self, data, target_size):
        data_df = pd.DataFrame(data)
        cat_columns = data_df.columns[:len(self.embedding_dims)]
        cont_columns = data_df.columns[len(self.embedding_dims):-target_size - 1]
        # Extract prices from the last column
        prices = data_df.iloc[:, -1].values  # Assuming prices are in the last column

        # Label encode categorical columns
        for col in cat_columns:
            encoder = LabelEncoder()
            data_df[col] = encoder.fit_transform(data_df[col])
            self.label_encoders[col] = encoder

        # Normalize continuous columns and store the mean and std for each column
        self.cont_means = {}
        self.cont_stds = {}
        for col in cont_columns:
            mean = data_df[col].mean()
            std = data_df[col].std()
            data_df[col] = (data_df[col] - mean) / std
            self.cont_means[col] = mean
            self.cont_stds[col] = std

        cat_data = data_df[cat_columns].values
        cont_data = data_df[cont_columns].values
        targets = data_df.iloc[:, -target_size - 1:-1].values  # Adjust target extraction if necessary
        return cat_data, cont_data, targets, prices

    def train_model(self, num_epochs=10, lr=0.001, batch_size=32, patience=5, criterion_=None):
        # Create DataLoader for training data
        train_dataset = CustomDataset(self.train_data['cat'], self.train_data['cont'], self.train_targets,
                                      self.train_prices)
        train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        # Create DataLoader for validation data
        val_dataset = CustomDataset(self.val_data['cat'], self.val_data['cont'], self.val_targets, self.val_prices)
        val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # Define optimizer and loss function
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.L1Loss()

        # Define ReduceLROnPlateau scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=patience // 2,
                                                         verbose=True)

        best_val_loss = float('inf')  # Initialize best validation loss for early stopping
        no_improvement_count = 0  # Counter to track epochs without improvement in validation loss

        # Training loop
        for epoch in range(num_epochs):
            self.model.train()  # Set the model to training mode
            train_losses = []  # List to store loss values for each batch

            for cat_x, cont_x, y, prices in train_dataloader:
                optimizer.zero_grad()  # Clear gradients
                outputs = self.model(cat_x, cont_x)  # Forward pass: compute model output
                # print(outputs.shape)  # Should show something like [batch_size, 12]
                # print(prices.unsqueeze(1).shape)   # Should be compatible with the shape of outputs for element-wise multiplication
                weighted_outputs = outputs * prices.unsqueeze(1)
                weighted_actuals = y * prices.unsqueeze(1)
                loss = criterion(weighted_outputs, weighted_actuals)  # Compute loss
                loss.backward()  # Backward pass: compute gradient of the loss with respect to model parameters
                optimizer.step()  # Perform a single optimization step (parameter update)
                train_losses.append(loss.item())  # Store the loss

            avg_train_loss = sum(train_losses) / len(train_losses)  # Calculate average training loss for the epoch

            # Validation phase
            self.model.eval()  # Set the model to evaluation mode
            val_losses = []  # List to store loss values for each validation batch

            with torch.no_grad():  # Disable gradient calculation
                for cat_x, cont_x, y, prices in val_dataloader:
                    outputs = self.model(cat_x, cont_x)  # Forward pass: compute model output
                    weighted_outputs = outputs * prices.unsqueeze(1)
                    weighted_actuals = y * prices.unsqueeze(1)
                    loss = criterion(weighted_outputs, weighted_actuals)  # Compute loss
                    val_losses.append(loss.item())  # Store the loss

            avg_val_loss = sum(val_losses) / len(val_losses)  # Calculate average validation loss for the epoch

            print(f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")
            # Step the scheduler on validation loss
            scheduler.step(avg_val_loss)
            # Check for improvement in validation loss for early stopping
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss  # Update best validation loss
                no_improvement_count = 0  # Reset counter
            else:
                no_improvement_count += 1  # Increment counter

            # Early stopping condition
            if no_improvement_count >= patience:
                print(f"Early stopping triggered. No improvement in validation loss for {patience} consecutive epochs.")
                break  # Exit the training loop

    def predict(self, new_data):
        new_data_df = pd.DataFrame(new_data) if not isinstance(new_data, pd.DataFrame) else new_data.copy()

        # Apply label encoders to the categorical columns
        for col in self.label_encoders.keys():
            new_data_df[col] = new_data_df[col].apply(
                lambda x: self.label_encoders[col].transform([x])[0] if x in self.label_encoders[col].classes_ else 0)

        # Normalize the continuous columns using the stored means and stds
        for col, mean in self.cont_means.items():
            std = self.cont_stds[col]
            new_data_df[col] = (new_data_df[col] - mean) / std

        cat_data = new_data_df.iloc[:, :len(self.embedding_dims)].values
        cont_data = new_data_df.iloc[:, len(self.embedding_dims):].values
        cat_data_tensor = torch.tensor(cat_data).long()
        cont_data_tensor = torch.tensor(cont_data).float()

        self.model.eval()
        with torch.no_grad():
            predictions = self.model(cat_data_tensor, cont_data_tensor)

        # Convert predictions from log scale back to original scale
        predictions_exp = np.exp(predictions.numpy())

        return pd.DataFrame(predictions_exp, columns=[f'Prediction_{i}' for i in range(predictions_exp.shape[1])])

    def get_embeddings(self, new_data):
        # Convert the new data into a DataFrame if it's not already in that format
        new_data_df = pd.DataFrame(new_data)

        # Iterate over each column that has a corresponding label encoder
        for col in self.label_encoders:
            # Check if the column exists in the new data DataFrame
            if col in new_data_df.columns:
                # Apply label encoding to the column, mapping unseen categories to 0
                # This uses the label encoder to transform each value in the column
                # If a category is unseen (not in label encoder classes), it maps to 0
                # new_data_df[col] = new_data_df[col].map(lambda x: self.label_encoders[col].transform([x])[0] if x in self.label_encoders[col].classes_ else 0)
                new_data_df[col] = new_data_df[col].apply(
                    lambda x: self.label_encoders[col].transform([x])[0] if pd.notna(x) and x in self.label_encoders[
                        col].classes_ else 0)

        # Convert the processed DataFrame into a PyTorch tensor for model input
        # The values are converted to long integers, as they are categorical indices
        new_data_tensor = torch.tensor(new_data_df.values).long()

        # Set the model to evaluation mode. This is important as it disables dropout and batch normalization layers
        self.model.eval()
        with torch.no_grad():  # Disable gradient computation for efficiency and to prevent changes to the model weights
            # Obtain embeddings from the model by passing in the input tensor
            embeddings_list = self.model.get_embeddings(new_data_tensor)

            # Initialize an empty list to store the pandas Series for each embedding dimension
            columns = []
            # Iterate over the list of embedding tensors and their corresponding input column
            for i, embedding_tensor in enumerate(embeddings_list):
                col = new_data_df.columns[i]  # Get the name of the current column
                # Iterate over each dimension of the embedding for the current feature
                for j in range(self.embedding_dims[i]):
                    # Convert the tensor slice for the current dimension to a numpy array, then to a pandas Series
                    # The use of `.cpu()` ensures compatibility if using CUDA tensors, moving tensor to CPU memory
                    column_series = pd.Series(embedding_tensor[:, j].cpu().numpy(), name=f'{col}_emb_dim{j}')
                    columns.append(column_series)  # Add the Series to the list

            # Concatenate all Series in the list into a single DataFrame along the columns (axis=1)
            # This results in a DataFrame where each column represents one dimension of an embedding
            embeddings_df = pd.concat(columns, axis=1)

            return embeddings_df  # Return the DataFrame containing all the embeddings
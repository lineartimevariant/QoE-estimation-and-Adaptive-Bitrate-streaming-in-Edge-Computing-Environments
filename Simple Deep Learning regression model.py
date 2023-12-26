import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

# Load the processed data
processed_data = pd.read_csv('processed_data.csv')

# Check the columns in your DataFrame
print(processed_data.columns)

# Handle categorical variables (e.g., 'Source IP', 'Destination IP', 'Protocol Type')
categorical_columns = ['Source IP', 'Destination IP']  # Add 'Protocol Type' if it exists
processed_data = pd.get_dummies(processed_data, columns=categorical_columns, drop_first=True)

# Select features and target variable
features = processed_data.drop(['Timestamp', 'Latency', 'Latency Category'], axis=1)  # Adjust columns as needed
target = processed_data['Latency']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Standardize features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define a simple deep-learning model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # Output layer for regression task

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model and capture the training history
history = model.fit(X_train_scaled, y_train, epochs=200, batch_size=32, validation_data=(X_test_scaled, y_test))

# Evaluate the model on the test set
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error on Test Set: {mse}')

# Plot the training loss and validation loss over epochs
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.show()

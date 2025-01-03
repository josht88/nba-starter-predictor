import os
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report

# Connect to the merged data database
conn = sqlite3.connect('merged_data.db')

# Load data
query = 'SELECT * FROM merged_data'
df = pd.read_sql(query, conn)

# Separate features and target
X = df.drop(columns=['Player', 'is_starter'])  # Drop non-numeric columns and target
y = df['is_starter']  # Target variable

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression Model for Prediction
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate Logistic Regression
print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Display Feature Weights
feature_weights = pd.DataFrame({'Feature': X.columns, 'Weight': model.coef_[0]})
feature_weights = feature_weights.sort_values(by='Weight', ascending=False)
print("Feature Weights:")
print(feature_weights)

# KMeans Clustering for Multiclustering Analysis
numeric_df = df.drop(columns=['Player', 'is_starter'])  # Ensure only numeric columns are used
kmeans = KMeans(n_clusters=2, random_state=42)  # 2 clusters for starters and non-starters
clusters = kmeans.fit_predict(numeric_df)
df['Cluster'] = clusters

# Analyze Cluster Characteristics (numeric only)
cluster_0 = numeric_df[df['Cluster'] == 0].mean()
cluster_1 = numeric_df[df['Cluster'] == 1].mean()

print("Cluster 0 Mean Values:\n", cluster_0)
print("Cluster 1 Mean Values:\n", cluster_1)

# Close database connection
conn.close()

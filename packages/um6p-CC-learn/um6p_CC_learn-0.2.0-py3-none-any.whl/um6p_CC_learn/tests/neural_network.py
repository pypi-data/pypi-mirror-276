import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from neural_network.multilayer_perceptron import NeuralNetwork
import time

# Load data
data = load_iris()
X = data.data
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train custom neural network
nn = NeuralNetwork(layers=[X_train.shape[1], 10, len(np.unique(y))], learning_rate=0.01, epochs=10000)
start_time = time.time()
nn.fit(X_train, y_train)
nn_fit_time = time.time() - start_time

# Predict with custom neural network
nn_predictions = nn.predict(X_test)

# Metrics for custom neural network
nn_accuracy = accuracy_score(y_test, nn_predictions)
nn_precision = precision_score(y_test, nn_predictions, average='weighted')
nn_recall = recall_score(y_test, nn_predictions, average='weighted')
nn_f1 = f1_score(y_test, nn_predictions, average='weighted')

print(f"Custom Neural Network - Fit Time: {nn_fit_time:.4f}s, Accuracy: {nn_accuracy:.4f}, Precision: {nn_precision:.4f}, Recall: {nn_recall:.4f}, F1 Score: {nn_f1:.4f}")

# Create and train scikit-learn neural network
sk_nn = MLPClassifier(hidden_layer_sizes=(10,), max_iter=10000, learning_rate_init=0.01, random_state=42)
start_time = time.time()
sk_nn.fit(X_train, y_train)
sk_nn_fit_time = time.time() - start_time

# Predict with scikit-learn neural network
sk_nn_predictions = sk_nn.predict(X_test)

# Metrics for scikit-learn neural network
sk_nn_accuracy = accuracy_score(y_test, sk_nn_predictions)
sk_nn_precision = precision_score(y_test, sk_nn_predictions, average='weighted')
sk_nn_recall = recall_score(y_test, sk_nn_predictions, average='weighted')
sk_nn_f1 = f1_score(y_test, sk_nn_predictions, average='weighted')

print(f"Scikit-learn Neural Network - Fit Time: {sk_nn_fit_time:.4f}s, Accuracy: {sk_nn_accuracy:.4f}, Precision: {sk_nn_precision:.4f}, Recall: {sk_nn_recall:.4f}, F1 Score: {sk_nn_f1:.4f}")

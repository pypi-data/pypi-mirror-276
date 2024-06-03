import numpy as np
from um6p_CC_learn.base.base import BaseEstimator, ClassifierMixin

class NeuralNetwork(ClassifierMixin, BaseEstimator):
    def __init__(self, layers, learning_rate=0.01, epochs=1000):
        """
        Initialize the neural network.

        Parameters:
        layers (list): List of integers representing the number of nodes in each layer.
        learning_rate (float): Learning rate for gradient descent.
        epochs (int): Number of iterations for training.
        """
        self.layers = layers
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = []
        self.biases = []
        
        # Initialize weights and biases
        for i in range(len(layers) - 1):
            weight_matrix = np.random.randn(layers[i], layers[i + 1]) * 0.01
            bias_vector = np.zeros((1, layers[i + 1]))
            self.weights.append(weight_matrix)
            self.biases.append(bias_vector)

    def softmax(self, z):
        """
        Softmax activation function.

        Parameters:
        z (np.ndarray): Input array.

        Returns:
        np.ndarray: Output array after applying softmax.
        """
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def softmax_derivative(self, output, y):
        """
        Derivative of the softmax function for backpropagation.

        Parameters:
        output (np.ndarray): Output array from softmax function.
        y (np.ndarray): True labels.

        Returns:
        np.ndarray: Gradient of the loss with respect to softmax inputs.
        """
        return output - y

    def sigmoid(self, z):
        """
        Sigmoid activation function.

        Parameters:
        z (np.ndarray): Input array.

        Returns:
        np.ndarray: Output array after applying sigmoid.
        """
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivative(self, z):
        """
        Derivative of the sigmoid function.

        Parameters:
        z (np.ndarray): Input array.

        Returns:
        np.ndarray: Derivative of sigmoid.
        """
        return z * (1 - z)

    def one_hot_encode(self, y, num_classes):
        """
        One hot encode the target variable.

        Parameters:
        y (np.ndarray): Target values.
        num_classes (int): Number of classes.

        Returns:
        np.ndarray: One hot encoded target values.
        """
        return np.eye(num_classes)[y]

    def forward(self, X):
        """
        Perform a forward pass through the network.

        Parameters:
        X (np.ndarray): Input data.

        Returns:
        list: List of activations for each layer.
        """
        activations = [X]
        for i in range(len(self.weights) - 1):
            z = np.dot(activations[-1], self.weights[i]) + self.biases[i]
            a = self.sigmoid(z)
            activations.append(a)
        # Output layer with softmax activation
        z = np.dot(activations[-1], self.weights[-1]) + self.biases[-1]
        a = self.softmax(z)
        activations.append(a)
        return activations

    def backward(self, X, y, activations):
        """
        Perform a backward pass and update weights and biases.

        Parameters:
        X (np.ndarray): Input data.
        y (np.ndarray): Target values.
        activations (list): List of activations for each layer.
        """
        m = X.shape[0]
        dz = self.softmax_derivative(activations[-1], y)
        for i in reversed(range(len(self.weights))):
            dw = np.dot(activations[i].T, dz) / m
            db = np.sum(dz, axis=0, keepdims=True) / m
            dz = np.dot(dz, self.weights[i].T) * self.sigmoid_derivative(activations[i])
            self.weights[i] -= self.learning_rate * dw
            self.biases[i] -= self.learning_rate * db

    def fit(self, X, y):
        """
        Train the neural network.

        Parameters:
        X (np.ndarray): Input data.
        y (np.ndarray): Target values.
        """
        y_encoded = self.one_hot_encode(y, self.layers[-1])
        for epoch in range(self.epochs):
            activations = self.forward(X)
            self.backward(X, y_encoded, activations)

    def predict(self, X):
        """
        Predict the output for given input data.

        Parameters:
        X (np.ndarray): Input data.

        Returns:
        np.ndarray: Predicted output.
        """
        activations = self.forward(X)
        return np.argmax(activations[-1], axis=1)

    def predict_proba(self, X):
        """
        Predict the probabilities for given input data.

        Parameters:
        X (np.ndarray): Input data.

        Returns:
        np.ndarray: Predicted probabilities.
        """
        activations = self.forward(X)
        return activations[-1]

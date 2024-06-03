import numpy as np
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')
class Tensor:
    def __init__(self, data):
        if isinstance(data, (list, np.ndarray)):
            self.data = np.array(data)
        else:
            raise TypeError("Unsupported type. Data should be a list or a numpy array.")

    def __add__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self.data + other.data)
        else:
            return Tensor(self.data + other)

    def __sub__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self.data - other.data)
        else:
            return Tensor(self.data - other)

    def __mul__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self.data * other.data)
        else:
            return Tensor(self.data * other)

    def __truediv__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self.data / other.data)
        else:
            return Tensor(self.data / other)

    def reshape(self, new_shape):
        return Tensor(self.data.reshape(new_shape))

    def sum(self, axis=None):
        return Tensor(self.data.sum(axis=axis))

    def transpose(self):
        return Tensor(self.data.T)

    def __repr__(self):
        return f"Tensor({self.data})"
    

class Layer(ABC):
    def __init__(self):
        super().__init__()
        self.input = None
        self.output = None

    @abstractmethod
    def forward(self, input):
        """
        Processes the input data and returns the output.
        This method should also store the input for use during backpropagation.
        """
        pass

    @abstractmethod
    def backward(self, output_gradient):
        """
        Backpropagates the gradient through the layer and returns the gradient with respect to the input.
        """
        pass

    @abstractmethod
    def update(self, learning_rate):
        """
        Updates the parameters of the layer using the stored gradients.
        """
        pass

class ReLU:
    def forward(self, input):
        self.input = input
        return np.maximum(0, input)

    def backward(self, output_gradient):
        # Gradient of ReLU is 0 for input values less than 0, and 1 for input values greater than 0
        input_gradient = (self.input > 0) * output_gradient
        return input_gradient

class Sigmoid:
    def forward(self, input):
        self.output = 1 / (1 + np.exp(-input))
        return self.output

    def backward(self, output_gradient):
        # Gradient of the sigmoid function
        return output_gradient * self.output * (1 - self.output)
    

class Softmax:
    def __init__(self):
        self.output = None  # This will store the output of the softmax from the forward pass

    def forward(self, input):
        shift_x = input - np.max(input, axis=1, keepdims=True)
        exps = np.exp(shift_x)
        self.output = exps / np.sum(exps, axis=1, keepdims=True)
        return self.output

    def backward(self, output_gradient):
    # Use the output from the forward pass
        S = self.output

        # Simplified gradient computation for softmax
        input_gradient = S * (output_gradient - np.sum(S * output_gradient, axis=1, keepdims=True))
        return input_gradient
    
class Dense(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        # Initialize weights with small random values (using He initialization for ReLU activation)
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2. / input_size)
        self.biases = np.zeros(output_size)
        self.gradient_weights = None
        self.gradient_biases = None

    def forward(self, input):
        self.input = input
        return np.dot(input, self.weights) + self.biases

    def backward(self, output_gradient):
        # Gradient with respect to input
        input_gradient = np.dot(output_gradient, self.weights.T)
        # Gradient with respect to weight
        self.gradient_weights = np.dot(self.input.T, output_gradient)
        # Gradient with respect to biases
        self.gradient_biases = np.sum(output_gradient, axis=0)
        return input_gradient

    def update(self, learning_rate):
        # Update weights and biases using the gradient and learning rate
        self.weights -= learning_rate * self.gradient_weights
        self.biases -= learning_rate * self.gradient_biases

    def __repr__(self):
        return f"Dense({self.input_size} -> {self.output_size})"
    
class NeuralNetwork:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, input):
        for layer in self.layers:
            input = layer.forward(input)
        return input

    def backward(self, gradient):
        for layer in reversed(self.layers):
            gradient = layer.backward(gradient)

    def update(self, learning_rate):
        for layer in self.layers:
            # Check if the layer has the 'update' method (i.e., if it has parameters to update)
            if hasattr(layer, 'update'):
                layer.update(learning_rate)


    def compute_mse_loss_and_gradient(self, predicted, true):
        # Compute mean squared error loss
        loss = np.mean((predicted - true) ** 2)
        # Compute gradient of the loss function with respect to the output of the last layer
        gradient = 2 * (predicted - true) / true.size
        return loss, gradient

    def train(self, x_train, y_train, epochs, learning_rate):
        for epoch in range(epochs):
            # Forward pass for all examples
            outputs = self.forward(x_train)
            # Compute loss and gradient for all examples
            loss, gradients = self.compute_mse_loss_and_gradient(outputs, y_train)
            # Backward pass for all examples
            self.backward(gradients)
            # Update weights once based on average gradient
            self.update(learning_rate)
            # Calculate and print average loss
            print(f'Epoch {epoch+1}, Loss: {loss}')
    
    def train_batches(self, x_train, y_train, epochs, learning_rate, batch_size=128):
        num_examples = len(x_train)
        num_batches = num_examples // batch_size
        
        for epoch in range(epochs):
            # Shuffle dataset at the beginning of each epoch
            indices = np.random.permutation(num_examples)
            x_train_shuffled = x_train[indices]
            y_train_shuffled = y_train[indices]

            for batch in range(num_batches):
                start = batch * batch_size
                end = start + batch_size
                x_batch = x_train_shuffled[start:end]
                y_batch = y_train_shuffled[start:end]
                
                # Forward pass
                output = self.forward(x_batch)
                # Compute loss and gradient
                loss, gradient = self.compute_mse_loss_and_gradient(output, y_batch)
                # Backward pass
                self.backward(gradient)
                # Update weights
                self.update(learning_rate)
            
            # Optional: Print loss every epoch or every few epochs
            print(f'Epoch {epoch+1}, Loss: {loss}')

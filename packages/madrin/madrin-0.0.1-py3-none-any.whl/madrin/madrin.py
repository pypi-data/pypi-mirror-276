import numpy as np
class Linear():
    def __init__(self,no_of_neurons,input_size,gain=1):
        self.no_of_neurons=no_of_neurons
        self.input_size=input_size

        self.weights=np.random.randn(input_size,no_of_neurons) * (gain / (input_size)**0.5)
        self.biases=np.zeros((1,no_of_neurons))

        self.gradient_w=np.zeros((input_size,no_of_neurons))
        self.gradient_b=np.zeros((1,no_of_neurons))

    def forward(self,inputs):
        self.inputs = inputs
        return np.dot(inputs,self.weights)+self.biases

    def backward(self,gradient_outputs,lr):
        self.gradient_w = (1/len(gradient_outputs))*np.dot(self.inputs.T,gradient_outputs)
        self.gradient_b = np.mean(gradient_outputs, axis=0, keepdims= True)
        self.gradient_descent(lr)
        return np.dot(gradient_outputs,self.weights.T)

    def gradient_descent(self,lr):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                self.weights[i][j]-=lr*self.gradient_w[i][j]

        self.biases-=lr*self.gradient_b

class Sigmoid():
    def forward(self,inputs):
        self.activations = np.exp(np.fmin(inputs, 0)) / (1 + np.exp(-np.abs(inputs)))
        return self.activations

    def backward(self,gradient_outputs,lr):
        A_prime = self.activations*(1-self.activations)
        return A_prime * gradient_outputs

class Relu():
    def forward(self,inputs):
        self.activations = np.maximum(np.zeros(inputs.shape),inputs)
        return self.activations

    def backward(self,gradient_outputs,lr):
        return gradient_outputs * (self.activations > 0)

class Tanh():
    def forward(self,inputs):
        self.activations = np.tanh(inputs)
        return self.activations

    def backward(self,gradient_outputs,lr):
        return gradient_outputs * (1 - self.activations ** 2)

class Softmax():
    def forward(self, inputs):
        expo = np.exp(inputs -  np.max(inputs, axis=1, keepdims=True))
        self.activations = expo / np.sum(expo, axis=1, keepdims=True)
        return self.activations
    
    def backward(self,gradient_outputs,lr):
        num_samples = self.activations.shape[0]
        num_classes = self.activations.shape[1]

        # Initialize the gradient with respect to inputs
        gradient_inputs = np.zeros_like(self.activations)

        for i in range(num_samples):
            # Flatten activations and gradient for easier manipulation
            s = self.activations[i].reshape(-1, 1)
            d_out = gradient_outputs[i].reshape(-1, 1)
            
            # Compute the Jacobian matrix of the softmax function
            jacobian_matrix = np.diagflat(s) - np.dot(s, s.T)
            
            # Compute the gradient with respect to the input
            gradient_inputs[i] = np.dot(jacobian_matrix, d_out).reshape(-1)
        
        return gradient_inputs
    

class Network():
    def __init__(self, layers, loss='mse'):
        self.layers = layers
        self.loss='mse'
        self.costs=[]

    def forward(self,inputs):
        for layer in self.layers:
            inputs=layer.forward(inputs)
        return inputs

    def backward(self,x,y,lr):
        gradient_outputs=self.derivative_of_loss(x,y)
        for layer in reversed(self.layers):
            gradient_outputs=layer.backward(gradient_outputs,lr)

    def derivative_of_loss(self,samples,labels):
        outputs = self.forward(samples)
        if self.loss == 'mse':
            return 2*(outputs-labels)
        
        elif self.loss == 'categorical_crossentropy':
            one_hot=np.zeros((labels.shape[0], self.layers[-1].activations.shape[1]))
            one_hot[np.arange(labels.shape[0]), labels] = 1
            clipped_outputs = np.clip(outputs, 1e-15, 1 - 1e-15)
            return -(one_hot/clipped_outputs)

    def fit(self, x, y, lr, epochs, loss='mse'):
        self.loss=loss
        for i in range(epochs):
            self.backward(x,y,lr)
            self.costs.append(self.cost(x,y))

    def cost(self,samples,labels):
        outputs = self.forward(samples)
        if self.loss == 'mse':
            return np.mean(np.sum(((outputs-labels)**2),axis=1,keepdims=True))
        
        elif self.loss == 'categorical_crossentropy':
            clipped_outputs = np.clip(outputs, 1e-15, 1 - 1e-15)
            correct_class_probs = clipped_outputs[np.arange(samples.shape[0]), labels]
            return np.mean(-np.log(correct_class_probs))
        
        else:
            print("Specify a valid loss function(mse or categorical_crossentropy)")

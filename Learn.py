from H5_trigger_states import (mlpfunc,numerical_features)
import numpy as np

def newmlp():
    numeric_features = numerical_features()
    incoming_vec = mlpfunc(numeric_features)

    X = np.array(incoming_vec)
    np.random.seed(42)#seeding
    W1 = np.random.randn(386, 256)
    b1 = np.zeros(256)

    W2 = np.random.randn(256, 512)
    b2 = np.zeros(512)

    y = np.random.randint(0, 2, size=X.shape[0])

    #optionA - actual used in function - "LEARNABLE VECTOR"
    W3 = np.random.randn(512, 1)
    b3 = np.zeros(1)
    
    for i in range(100):
        Z1 = np.dot(X, W1) + b1
        A1 = np.maximum(0, Z1)
        Z2 = np.dot(A1, W2) + b2
        Z2 = Z2 / (np.linalg.norm(Z2, axis=1, keepdims=True) + 1e-8)

        Z3 = np.dot(Z2, W3) + b3
        y_pred = Z3.flatten()
        error = y_pred - y
        loss = np.mean(error ** 2) # can also be
                                       # sq_error = np.square(error)
                                       # loss = np.average(sq_error)
        grad_W3 = np.dot(Z2.T, (2 * error / X.shape[0]).reshape(-1, 1))
        #grad_b3 = np.sum(2 * error / X.shape[0])
        grad_b3 = np.mean(2 * error) #more cleaner

        lr = 0.01
        W3 = W3 - lr * grad_W3
        b3 = b3 - lr * grad_b3

        if i % 10 == 0: #for debugging
            print( i, loss)

    return Z2
        





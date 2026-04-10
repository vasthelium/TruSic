from app.services.H5_trigger_states import (mlpfunc,numerical_features)
import numpy as np
import random

def newmlp():
    numeric_features = numerical_features()
    incoming_vec = mlpfunc(numeric_features)

    X = np.array(incoming_vec)
    np.random.seed(42)#seeding
    W1 = np.random.randn(386, 256)
    b1 = np.zeros(256)

    W2 = np.random.randn(256, 512)
    b2 = np.zeros(512)
    # y = np.random.randint(0, 2, size=X.shape[0])
    """
    instead of random y we are deriving y from classification
    """
    skips = []
    for samples in X:
        duration = random.randint(0,200)
        if duration < 10:
            y_skip = 0
        elif duration < 30:
            y_skip = 1
        elif duration < 120:
            y_skip = 2
        else:
            y_skip = 3
        skips.append(y_skip)
    y = np.array(skips)
    
    W3 = np.random.randn(512, 1)
    b3 = np.zeros(1)
    v_W3 = np.zeros_like(W3)
    v_b3 = np.zeros_like(b3)
    m_W3 = np.zeros_like(W3)
    m_b3 = np.zeros_like(b3)
    beta_1 = 0.9
    beta_2 = 0.999
    e = 1e-8

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
        m_W3 = beta_1 * m_W3 + (1 - beta_1) * grad_W3
        m_b3 = beta_1 * m_b3 + (1 - beta_1) * grad_b3
        v_W3 = beta_2 * v_W3 + (1 - beta_2) * (grad_W3 ** 2)
        v_b3 = beta_2 * v_b3 + (1 - beta_2) * (grad_b3 ** 2)
        W3 = W3 - lr * (m_W3 / (np.sqrt(v_W3) + e))
        b3 = b3 - lr * (m_b3 / (np.sqrt(v_b3) + e))

        if i % 10 == 0: #for debugging
            print( i, loss)

    return Z2




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
    
    W3 = np.random.randn(512, 4)
    b3 = np.zeros(4)

    # Adam params for all layers
    v_W3 = np.zeros_like(W3); v_b3 = np.zeros_like(b3)
    m_W3 = np.zeros_like(W3); m_b3 = np.zeros_like(b3)

    v_W2 = np.zeros_like(W2); v_b2 = np.zeros_like(b2)
    m_W2 = np.zeros_like(W2); m_b2 = np.zeros_like(b2)

    v_W1 = np.zeros_like(W1); v_b1 = np.zeros_like(b1)
    m_W1 = np.zeros_like(W1); m_b1 = np.zeros_like(b1)

    beta_1 = 0.9
    beta_2 = 0.999
    e = 1e-8

    for i in range(100):
        # -------------FORWARD------------------------
        Z1 = np.dot(X, W1) + b1
        A1 = np.maximum(0, Z1)

        Z2 = np.dot(A1, W2) + b2
        Z2_norm = Z2 / (np.linalg.norm(Z2, axis=1, keepdims=True) + 1e-8)

        Z3 = np.dot(Z2_norm, W3) + b3

        exp_Z3 = np.exp(Z3 - np.max(Z3, axis=1, keepdims=True))
        y_pred = exp_Z3 / np.sum(exp_Z3, axis=1, keepdims=True)

        # print(y_pred.shape) - DEBUG LINE
        correct_probs = y_pred[np.arange(X.shape[0]), y]
        log_probs = np.log(correct_probs + 1e-8)
        loss = -np.mean(log_probs)
        #error = y_pred - y
        #loss = np.mean(error ** 2) # can also be
                                       # sq_error = np.square(error)
                                       # loss = np.average(sq_error)
        #---------------ONEHOT-------------------------
        y_one_hot = np.zeros((X.shape[0], 4))
        y_one_hot[np.arange(X.shape[0]), y] = 1

        #---------------BACK PROP----------------------
        error = y_pred - y_one_hot

        #W3
        grad_W3 = np.dot(Z2_norm.T, error) / X.shape[0]
        grad_b3 = np.mean(error, axis=0)

        # Backprop into Z2_norm
        dZ2_norm = np.dot(error, W3.T)

        # Backprop through normalization (approximate simplification)
        norm = np.linalg.norm(Z2, axis=1, keepdims=True) + 1e-8
        dZ2 = dZ2_norm / norm

        # W2
        grad_W2 = np.dot(A1.T, dZ2) / X.shape[0]
        grad_b2 = np.mean(dZ2, axis=0)

        # Backprop through ReLU
        dA1 = np.dot(dZ2, W2.T)
        dZ1 = dA1 * (Z1 > 0)

        # W1
        grad_W1 = np.dot(X.T, dZ1) / X.shape[0]
        grad_b1 = np.mean(dZ1, axis=0)

        #---------------Learning Rate----------------------
        base_lr = 0.01
        lr = base_lr * (0.95 ** i)

        #W3
        m_W3 = beta_1 * m_W3 + (1 - beta_1) * grad_W3
        v_W3 = beta_2 * v_W3 + (1 - beta_2) * (grad_W3 ** 2)
        W3 -= lr * (m_W3 / (np.sqrt(v_W3) + e))

        m_b3 = beta_1 * m_b3 + (1 - beta_1) * grad_b3
        v_b3 = beta_2 * v_b3 + (1 - beta_2) * (grad_b3 ** 2)
        b3 -= lr * (m_b3 / (np.sqrt(v_b3) + e))

        # W2
        m_W2 = beta_1 * m_W2 + (1 - beta_1) * grad_W2
        v_W2 = beta_2 * v_W2 + (1 - beta_2) * (grad_W2 ** 2)
        W2 -= lr * (m_W2 / (np.sqrt(v_W2) + e))

        m_b2 = beta_1 * m_b2 + (1 - beta_1) * grad_b2
        v_b2 = beta_2 * v_b2 + (1 - beta_2) * (grad_b2 ** 2)
        b2 -= lr * (m_b2 / (np.sqrt(v_b2) + e))

        # W1
        m_W1 = beta_1 * m_W1 + (1 - beta_1) * grad_W1
        v_W1 = beta_2 * v_W1 + (1 - beta_2) * (grad_W1 ** 2)
        W1 -= lr * (m_W1 / (np.sqrt(v_W1) + e))

        m_b1 = beta_1 * m_b1 + (1 - beta_1) * grad_b1
        v_b1 = beta_2 * v_b1 + (1 - beta_2) * (grad_b1 ** 2)
        b1 -= lr * (m_b1 / (np.sqrt(v_b1) + e))

        if i % 10 == 0: #for debugging
            print( i, loss)

    return Z2_norm




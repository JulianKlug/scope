import tensorflow as tf
from tensorflow.keras import backend as K
import numpy as np

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


class RegressionAUC(tf.keras.metrics.Metric):
    def __init__(self, name='auc', **kwargs):
        super(RegressionAUC, self).__init__(name=name, **kwargs)
        self.internal_model = tf.keras.metrics.AUC()

    def update_state(self, y_true, y_pred, sample_weight=None):
        # binarize using 4.5h threshold
        y_true = y_true / 60 > 4.5
        y_pred = y_pred / 60 > 4.5

        y_true = tf.cast(y_true, tf.bool)
        y_pred = tf.cast(y_pred, tf.bool)

        self.internal_model.update_state(y_true, y_pred, sample_weight)

    def result(self):
        return self.internal_model.result()

    def reset_state(self):
        self.internal_model.reset_state()


def running_average(x:[np.array, list], N:int=10) -> np.array:
    '''
    Compute the running average of a sequence of values and return a sequence of the same length.
    Args:
        x: sequence of values
        N: size of the running average window
        if N is even, window will extend N/2 to the left and N/2 to the right
        if N is odd, window will extend (N-1)/2 to the left and (N-1)/2 to the right
    Returns: np.array with the same length as x
    '''
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    out = np.zeros(x.shape)
    for i in range(x.shape[0]):
        if i < N//2:
            out[i] = np.mean(x[:i+(N//2+1)])
        elif i > x.shape[0] - (N//2+1):
            out[i] = np.mean(x[i-N//2:])
        else:
            out[i] = np.mean(x[i-N//2: i+(N//2+1)])
    return out


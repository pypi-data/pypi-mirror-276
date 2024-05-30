import os
import numpy as np
import tensorflow as tf
import keras
from keras.api.layers import Dense, Input
from keras.api.callbacks import Callback

TEXTURE_MODEL_DIR = "models"
TRAIN_RATIO = 0.8


def standardize(data):
    mean = tf.reduce_mean(data, axis=0)
    stddev = tf.math.reduce_std(data, axis=0)
    return (data - mean) / stddev


class ModelBuilder:
    def __init__(self):
        self.red = None
        self.blue = None

    def add_red(self, features):
        if self.red is None:
            self.red = features
        else:
            self.red = np.vstack((self.red, features))

    def add_blue(self, features):
        if self.blue is None:
            self.blue = features
        else:
            self.blue = np.vstack((self.blue, features))

    def save(self, name):
        os.makedirs(TEXTURE_MODEL_DIR, exist_ok=True)
        model_path = os.path.join(TEXTURE_MODEL_DIR, f"{name}.keras")
        model = ClassificationModel(self.model)
        model.save(model_path)

        return model_path
    
    def _build_model(self, input_shape):
        model = keras.Sequential()
        model.add(Input(input_shape))
        model.add(Dense(60, activation="relu"))
        model.add(Dense(10, activation="relu"))
        model.add(Dense(1, activation="sigmoid"))

        return model

    def train(self, callback=None):
        # Combine the feature vectors
        X = np.vstack((self.red, self.blue))
        # Create labels (0 for the first set, 1 for the second set)
        y = np.array([0] * len(self.red) + [1] * len(self.blue))

        total_samples = X.shape[0]
        train_samples = int(total_samples * TRAIN_RATIO)

        # Shuffle the data
        indices = tf.range(start=0, limit=total_samples, dtype=tf.int32)
        shuffled_indices = tf.random.shuffle(indices)

        X = tf.gather(X, shuffled_indices).numpy()
        y = tf.gather(y, shuffled_indices).numpy()

        # Split the data
        X_train, X_test = X[:train_samples], X[train_samples:]
        y_train, y_test = y[:train_samples], y[train_samples:]

        X_train = standardize(X_train)
        X_test = standardize(X_test)

        self.model = self._build_model(input_shape=(X_train.shape[1],))

        # Compile the model
        self.model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

        # Train the model
        callbacks = []
        if callback is not None:
            callbacks.append(callback)
        self.model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, callbacks=callbacks, verbose=False)

        # Evaluate the model
        loss, accuracy = self.model.evaluate(X_test, y_test, callbacks=callbacks, verbose=False)
        print(f"Test accuracy: {accuracy}")

        classification_model = ClassificationModel(self.model)
        classification_model.save("keras_mlp_model.keras")
        
        return classification_model

class ClassificationModel:
    def __init__(self, model: keras.Sequential):
        self.model = model

    def save(self, path):
        self.model.save(path)

    def predict(self, X):
        y = self.model.predict(standardize(X), batch_size=10000)

        return y

    @staticmethod
    def load(path):
        model = keras.models.load_model(path)
        return ClassificationModel(model)
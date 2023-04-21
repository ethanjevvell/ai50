# TRAINING RUNS

1.            model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 2s - loss: 0.7633 - accuracy: 0.9134 - 2s/epoch - 5ms/step

2.           model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.5258 - accuracy: 0.8670 - 866ms/epoch - 3ms/step

3.           model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 2s - loss: 0.4123 - accuracy: 0.9185 - 2s/epoch - 6ms/step

4.          model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.5566 - accuracy: 0.8509 - 631ms/epoch - 2ms/step

5.        model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            16, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 0s - loss: 0.5797 - accuracy: 0.8462 - 367ms/epoch - 1ms/step

6.  model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(
    64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.3721 - accuracy: 0.9417 - 1s/epoch - 3ms/step

# Observations

- Changing activation functions:

ReLu tend to outperform sigmoid.

- Increasing number of nodes in layer:

High numbers of sigmoid nodes tends to decrease accuracy.

# Dimensions we can experiment with

- Increase total number of layers
- Change type of layers (Convolution, Pooling, Dense, etc.)
- Change loss function
- Change activation functions
- Change dropout rates
- Change pooling techniques

# Types of layers

- Dense: Each node connects to every other node in the previous layer
- Convolution: Convoluting images to extract features
- Pooling: Reducing size of images (already done)

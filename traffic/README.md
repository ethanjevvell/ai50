# Post-training observations:

I experimented with changing the number of neuron layers, their activation functions, and employing one or more convolution/pooling layers. In general, ReLu activation functions tended to outperform layers with sigmoid activations. Initial testing found that there was a "sweet spot" for how many neurons should be in activation layers. In general, layers between 128 and 256 neurons performed well without taking too long to train. Larger networks also produced near or equivalent accuracy, but at the cost of training time. For this reason, I decided to submit a network with slightly fewer neurons at the cost of a few hundredths of a percent of accuracy.

Convolution layers demonstrated a similar behavior. 32 filters vastly outperformed 16 or 64 filters. An input shape of 5 x 5 outperformed 3 x 3 or 10 x 10. As a result, optimizing the network involved several dozen training runs (some, but not all, of which are recorded below), and slowly building more successful networks. Higher performance could likely be achieved with more testing, but a more structured or programmatic approach would be ideal, such as a way to quickly generate several dozen permutations, and then graphing their performance.

# TRAINING RUNS

1.                                             model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 2s - loss: 0.7633 - accuracy: 0.9134 - 2s/epoch - 5ms/step

2.                                            model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.5258 - accuracy: 0.8670 - 866ms/epoch - 3ms/step

3.                                            model = tf.keras.models.Sequential([
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

4.                                           model = tf.keras.models.Sequential([
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

5.                                         model = tf.keras.models.Sequential([
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

7.                                     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            20, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.5665 - accuracy: 0.9022 - 654ms/epoch - 2ms/step

8.                                    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (2, 2), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: Poor; did not finish test

9.                                   model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 0s - loss: 0.5009 - accuracy: 0.8910 - 439ms/epoch - 1ms/step

10.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            16, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 0s - loss: 0.5640 - accuracy: 0.9026 - 425ms/epoch - 1ms/step

11.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            16, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 0s - loss: 0.4754 - accuracy: 0.9091 - 412ms/epoch - 1ms/step

12.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            16, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 0s - loss: 0.5647 - accuracy: 0.9054 - 421ms/epoch - 1ms/step

13.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.4630 - accuracy: 0.9033 - 639ms/epoch - 2ms/step

14.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.4696 - accuracy: 0.9119 - 592ms/epoch - 2ms/step

15.         model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 2s - loss: 0.2695 - accuracy: 0.9501 - 2s/epoch - 5ms/step

16.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 2s - loss: 0.2077 - accuracy: 0.9556 - 2s/epoch - 6ms/step

17.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.1843 - accuracy: 0.9574 - 832ms/epoch - 2ms/step

18.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.1856 - accuracy: 0.9622 - 785ms/epoch - 2ms/step

19.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.1792 - accuracy: 0.9522 - 1s/epoch - 3ms/step

20.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.2218 - accuracy: 0.9481 - 886ms/epoch - 3ms/step

21.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")

    ])

- Outcome: 333/333 - 0s - loss: 0.1681 - accuracy: 0.9625 - 498ms/epoch - 1ms/step

22.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.1326 - accuracy: 0.9678 - 557ms/epoch - 2ms/step

23.     model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(
            32, (5, 5), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

- Outcome: 333/333 - 1s - loss: 0.3313 - accuracy: 0.9089 - 905ms/epoch - 3ms/step

# Observations

- ReLu tend to outperform sigmoid.

- High numbers of sigmoid nodes tends to decrease accuracy.

- Larger layers of neurons do not necessarily improve accuracy.

- Multiple rounds of pooling and convolution tend to improve accuracy.

- 32 filters in convolution layer tends to outperform higher or lower values.

- Too many neuron layers can decrease performance

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

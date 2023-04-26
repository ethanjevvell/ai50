import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):

    images = []
    labels = []

    for category in range(NUM_CATEGORIES):
        category_dir = os.path.join(data_dir, str(category))

        for filename in os.listdir(category_dir):
            file_path = os.path.join(category_dir, filename)

            img = cv2.imread(file_path)
            img_resized = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

            images.append(img_resized)
            labels.append(category)

    return (images, labels)


def get_model():

    # Model construction
    model = tf.keras.models.Sequential([
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

    loss_fn = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

    model.compile(optimizer="adam",
                  loss=loss_fn,
                  metrics=["accuracy"])

    return model


if __name__ == "__main__":
    main()

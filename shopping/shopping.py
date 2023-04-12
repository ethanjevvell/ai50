import csv
import sys
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):

    evidence = []
    labels = []

    with open(filename) as data_file:
        reader = csv.reader(data_file, delimiter=",")
        # Skip header
        next(reader)
        for row in reader:
            evidence_row = row[0:17]
            label_row = row[-1]
            evidence.append(evidence_row)
            labels.append(label_row)

    # Maps for data cleaning
    month_map = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
                 "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}
    weekend_map = {"TRUE": 1, "FALSE": 0}
    visitor_map = {"Returning_Visitor": 1, "New_Visitor": 0, "Other": 0}
    revenue_map = {"TRUE": 1, "FALSE": 0}
    float_cols = [1, 3, 5, 6, 7, 8, 9]
    int_cols = [0, 2, 4, 11, 12, 13, 14]

    for row in evidence:
        row[10] = month_map[row[10]]
        row[-1] = weekend_map[row[-1]]
        row[-2] = visitor_map[row[-2]]
        for index, value in enumerate(row):
            if index in float_cols:
                row[index] = float(value)
            if index in int_cols:
                row[index] = int(value)

    for index, item in enumerate(labels):
        labels[index] = revenue_map[item]

    return (evidence, labels)


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):

    correct_positives = 0
    correct_negatives = 0

    true_positives = 0
    true_negatives = 0

    for label, prediction in zip(labels, predictions):
        if label == 0 and prediction == 0:
            true_negatives += 1
            correct_negatives += 1
        elif label == 1 and prediction == 1:
            true_positives += 1
            correct_positives += 1
        elif label == 0 and prediction == 1:
            true_negatives += 1
        elif label == 1 and prediction == 0:
            true_positives += 1

    sensitivity = correct_positives / true_positives
    specificity = correct_negatives / true_negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()

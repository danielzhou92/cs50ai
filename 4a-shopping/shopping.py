import csv
import sys

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
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        # read csv file line by line and put into a tuple of lists
        evidence = []
        labels = []
        for row in reader:
            administrative = int(row[0])
            administrative_duration = float(row[1])
            informational = int(row[2])
            informational_duration = float(row[3])
            productRelated = int(row[4])
            productRelated_duration = float(row[5])
            bounceRates = float(row[6])
            exitRates = float(row[7])
            pageValues = float(row[8])
            specialDay = float(row[9])
            month = monthToNum(row[10])
            operatingSystems = int(row[11])
            browser = int(row[12])
            region = int(row[13])
            trafficType = int(row[14])
            visitorType = 1 if row[15] == "Returning_Visitor" else 0
            weekend = 1 if row[16] == "TRUE" else 0

            evidence.append([administrative, administrative_duration,
                             informational, informational_duration,
                             productRelated, productRelated_duration,
                             bounceRates, exitRates,
                             pageValues, specialDay,
                             month, operatingSystems,
                             browser, region,
                             trafficType, visitorType,
                             weekend])
            labels.append(1 if row[17] == "TRUE" else 0)

        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # the dataset is split in the main function already, into training set and testing set, no need to split again
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # declare coutner variables
    actualPositive = 0
    actualNegative = 0
    predictedPositive = 0
    predictedNegative = 0

    # loop through all variables and count through everything
    for i in range(len(labels)):
        if labels[i] == 1:
            actualPositive += 1
            if predictions[i] == 1:
                predictedPositive += 1
        else:
            actualNegative += 1
            if predictions[i] == 0:
                predictedNegative += 1

    # calculate sensitivity and specificity
    sensitivity = predictedPositive / actualPositive
    specificity = predictedNegative / actualNegative

    return (sensitivity, specificity)


def monthToNum(shortMonth):
    return {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'June': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }[shortMonth]


if __name__ == "__main__":
    main()
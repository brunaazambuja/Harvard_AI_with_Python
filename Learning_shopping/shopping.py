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


    with open(filename, 'r') as fp:
        fp.readline()
        reader = csv.reader(fp)
        evidence = []
        labels = []

        for row in reader:
            values = []
            values.append(int(row[0]))
            values.append(float(row[1]))
            values.append(int(row[2]))
            values.append(float(row[3]))
            values.append(int(row[4]))
            values.append(float(row[5]))
            values.append(float(row[6]))
            values.append(float(row[7]))
            values.append(float(row[8]))
            values.append(float(row[9]))

            months = dict()
            months['Jan'] = 0
            months['Feb'] = 1
            months['Mar'] = 2
            months['Apr'] = 3
            months['May'] = 4
            months['June'] = 5
            months['Jul'] = 6
            months['Aug'] = 7
            months['Sep'] = 8
            months['Oct'] = 9
            months['Nov'] = 10
            months['Dec'] = 11

            values.append(months[row[10]])
            values.append(int(row[11]))
            values.append(int(row[12]))
            values.append(int(row[13]))
            values.append(int(row[14]))
            if (row[15] == 'Returning_Visitor'):
                values.append(1)
            else:
                values.append(0)
            
            if (row[16] == 'TRUE'):
                values.append(1)
            else:
                values.append(0)
            
            evidence.append(values)
                
            if (row[17] == 'TRUE'):
                labels.append(1)
            else:
                labels.append(0)
   

    return (evidence, labels)

    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    
    return model.fit(evidence, labels)



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

    sensitivity = float(0)
    positives = 0

    specificity = float(0)
    negatives = 0

    for value, predicted in zip(labels, predictions):
        if (value == 1 and predicted == 1):
            sensitivity += 1
        elif (value == 0 and predicted == 0):
            specificity += 1
        
        if (value == 1):
            positives += 1
        else:
            negatives += 1

    sensitivity /= positives
    specificity /= negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()

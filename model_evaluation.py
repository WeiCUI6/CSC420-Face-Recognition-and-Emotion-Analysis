"""
 Module for evaluating the performance of different type of models
    - ROC curve
    - Mean Squared Error (MSE)
    - Confusion Matrix
    - Classification report
"""


import numpy as np
import matplotlib.pyplot as plt

from keras.utils import to_categorical
from itertools import cycle
from sklearn.preprocessing import label_binarize
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_squared_error, roc_curve, auc


def evaluate_model(model_trained, model_type, test, test_label, algorithm=None):
    """
    The function for evaluating the input model with the input test dataset and
    corresponding labels for the test dataset.

    Args:
        model_trained:     the input trained model for the purpose of evaluating.
        model_type:        kind of the input model.
        test:              the test dataset.
        test_label:        the labels for the test dataset.
        algorithm:         the feature algorithm that we want to perform.

    Returns:
        None.

    Notes: we will show the performance of each model in several ways.
    """
    if model_type == 'cnn':
        if algorithm == 'eigenfaces':
            # Reshape the input datasets to accord the cnn model
            test = test.reshape(-1, 1, 625)

            # One-hot encoding for the test labels
            test_label_hotcoder = to_categorical(test_label)

            # Use the model to predict
            test_pred = model_trained.predict(test)

            # Print classification report
            plot_ROC(test_label, test_pred)
            print('\nModel Evaluations:\n')
            print(f'{model_type} mse:', mean_squared_error(test_label, np.argmax(test_pred, axis=1)), '\n')
            print(f'{model_type} confusion matrix:\n', confusion_matrix(test_label, np.argmax(test_pred, axis=1)), '\n')
            print(f'{model_type} classification report:\n',
                  classification_report(test_label, np.argmax(test_pred, axis=1)), '\n')

        elif algorithm == 'fisherfaces':

            # Reshape the input datasets to accord the cnn model
            test = test.reshape(-1, 1, 6)

            # One-hot encoding for the test labels
            test_label_hotcoder = to_categorical(test_label)

            # Use the model to predict
            test_pred = model_trained.predict(test)

            # Print classification report
            plot_ROC(test_label, test_pred)
            print('\nModel Evaluations:\n')
            print(f'{model_type} mse:', mean_squared_error(np.argmax(test_label_hotcoder, axis=1), np.argmax(test_pred, axis=1)), '\n')
            print(f'{model_type} confusion matrix:\n', confusion_matrix(np.argmax(test_label_hotcoder, axis=1), np.argmax(test_pred, axis=1)), '\n')
            print(f'{model_type} classification report:\n',
                  classification_report(np.argmax(test_label_hotcoder, axis=1), np.argmax(test_pred, axis=1)), '\n')

        else:
            print("ERROR: invalid algorithm for CNN!")
            return None

    elif model_type == 'svm' or model_type == 'adaboost' or model_type == 'mlp':
        # get predictions on test data and plot roc curve
        grid_predictions = model_trained.predict(test)
        predict_score = model_trained.decision_function(test)
        plot_ROC(test_label, predict_score)

        # print other prediction metrics
        print('\nModel Evaluations:\n')
        print(f'{model_type} mse:', mean_squared_error(test_label, grid_predictions), '\n')
        print(f'{model_type} confusion matrix:\n', confusion_matrix(test_label, grid_predictions), '\n')
        print(f'{model_type} classification report:\n', classification_report(test_label, grid_predictions), '\n')

    else:
        print("ERROR: invalid model type!")
        return None


def plot_ROC(test_labels, grid_predictions):
    # Compute ROC curve and ROC area for each class
    n_classes = len(grid_predictions[0])
    class_count = [i for i in range(n_classes)]
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        true = label_binarize(test_labels, classes=class_count)
        fpr[i], tpr[i], _ = roc_curve(true[:, i], grid_predictions[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Plot all ROC curves
    colors = cycle(['purple', 'orange', 'green', 'blue', 'pink', 'red', 'yellow', 'aqua', 'lightblue', 'lightgreen'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, label='Class {0} (area = {1:0.2f})'.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Multi-class ROC curve')
    plt.legend(loc="lower right")
    plt.show()
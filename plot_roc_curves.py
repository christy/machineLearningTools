"""Plot train, valid, test ROC curves on top of each other in same plot"""

from collections import namedtuple

# Nametuple used for feeding values to plots.
SetValidation = namedtuple(
    "SetValidation", ["y_true", "y_pred", "title"]
)

"""Module to help when building classification related plot"""
import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from typing import Tuple


def plot_precision_recall_vs_threshold(*tuples: Tuple[models.SetValidation]):
    """Plot both precision and recall curves for different data
    sets (Typically: train, validation and test)

    Keyword Arguments:
        tuples {Tuple[pyazlo.plots.models.SetValidation]} -- Different
            SetValidation instances, defining ground truths and
            predictions for different sets of data.

    Raises:
        exceptions.PyazloPlotBadArgumentException: [description]
        ValueError: [description]
    """
    no_tuples = len(tuples)

    if no_tuples < 1:
        raise exceptions.PyazloPlotBadArgumentException(
            "You shall not pass with no inputs"
        )

    if no_tuples <= 3:
        fig, axes = plt.subplots(1, no_tuples)
        for ax_i, tuple_i in zip(axes, tuples):
            true_i = tuple_i.y_true
            pred_i = tuple_i.y_pred
            title_i = tuple_i.title
            precisions_i, recalls_i, thresholds_i = \
                metrics.precision_recall_curve(true_i, pred_i)
            ax_i.plot(
                thresholds_i, precisions_i[:-1], "b--", label="Precision"
            )
            ax_i.plot(thresholds_i, recalls_i[:-1], "g-", label="Recall")
            ax_i.set_ylabel("Score")
            ax_i.set_xlabel("Decision Threshold")
            ax_i.legend(loc='best')
            ax_i.grid()
            ax_i.set_title(title_i)

        fig.tight_layout()

    else:
        error_message = "You should not pass more than 3 sets yet."
        logger.error(error_message)
        raise ValueError(error_message)


def plot_rocs(*tuples: Tuple[models.SetValidation]):
    """Plots ROC curves for multiple sets of data.

    Arguments:
        tuples {pyazlo.plots.models.SetValidation}:
            Tuple containing a list of validation sets objects.

    Raises:
        exceptions.PyazloPlotBadArgumentException: When there are no
            tuples provided
        ValueError: When more than 3 sets are provided.
    """
    no_tuples = len(tuples)

    if no_tuples < 1:
        raise exceptions.PyazloPlotBadArgumentException(
            "You shall not pass with no inputs"
        )

    if no_tuples <= 3:
        plt.figure()

        for tuple_i in tuples:
            fpri, tpri, thi = metrics.roc_curve(tuple_i.y_true, tuple_i.y_pred)
            auci = metrics.auc(fpri, tpri)
            label_i = "{}: {:0.4f}".format(
                tuple_i.title, auci
            )

            plt.plot(fpri, tpri, linewidth=2, label=label_i)

        plt.title('ROC Curve')

        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([-0.005, 1, 0, 1.005])
        plt.xticks(np.arange(0, 1, 0.05), rotation=90)

        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate (Recall)")
        plt.legend(loc='best')
        plt.grid()
        plt.tight_layout()

    else:
        error_message = "You should not pass more than 3 sets yet."
        logger.error(error_message)
        raise ValueError(error_message)


# EXAMPLE FUNCTION CALL
nameYActual = 'fraudLong'
y_train_pred = trainDataAndPredictions['glm_p1'] #train fraud probability
y_test_pred = validDataAndPredictions['glm_p1']  #valid fraud probability
y_oot_pred = ootDataAndPredictions['glm_p1']     #oot fraud probability
train_set_validation = SetValidation(trainDataAndPredictions[nameYActual], y_train_pred, "Train")
valid_set_validation = SetValidation(validDataAndPredictions[nameYActual], y_test_pred, "Valid")
oot_set_validation = SetValidation(ootDataAndPredictions[nameYActual], y_oot_pred, "OOT")

plot_rocs(train_set_validation, valid_set_validation, oot_set_validation)

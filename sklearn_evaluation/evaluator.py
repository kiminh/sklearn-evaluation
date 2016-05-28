import matplotlib.pyplot as plt

from .util import estimator_type, class_name
from . import plots
from .report import generate


def gen_ax():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    return ax


class ClassifierEvaluator(object):
    """
     Encapsuates results from an estimator on a testing set to provide a
     simplified API from other modules. All parameters are optional, just
     fill the ones you need for your analysis.

    Parameters
    ----------
    estimator : sklearn estimator
        This object is only used to get feature importances via
        model.feature_parameters_
    y_true : array-like
        Target predicted classes (estimator predictions).
    y_pred : array-like
        Correct target values (ground truth).
     y_score : array-like
        Target scores (estimador predictions).
    feature_names : array-like
        Feature names.
    target_names : list
        List containing the names of the target classes
    estimator_name : str
        Identifier for the model. This can be later used to idenfity the
        estimator when generaing reports.
    """
    def __init__(self, estimator=None, y_true=None, y_pred=None, y_score=None,
                 feature_names=None, target_names=None, estimator_name=None):
        self._estimator = estimator
        self._y_true = y_true
        self._y_pred = y_pred
        self._y_score = y_score
        self._feature_names = feature_names
        self._target_names = target_names
        self._estimator_name = estimator_name
        # TODO: perform basic logic checking,
        # raise Exception if necessary

    @property
    def estimator_type(self):
        return estimator_type(self.estimator)

    @property
    def estimator_class(self):
        return class_name(self.estimator)

    # Properties should be read-only to ensure instance integrity
    @property
    def estimator(self):
        return self._estimator

    @property
    def y_true(self):
        return self._y_true

    @property
    def y_pred(self):
        return self._y_pred

    @property
    def y_score(self):
        return self._y_score

    @property
    def feature_names(self):
        return self._feature_names

    @property
    def target_names(self):
        return self._target_names

    @property
    def estimator_name(self):
        return self._estimator_name

    @property
    def confusion_matrix(self):
        return plots.confusion_matrix(self.y_true, self.y_pred,
                                      self.target_names, ax=gen_ax())

    @property
    def roc(self):
        return plots.roc(self.y_true, self.y_score, ax=gen_ax())

    @property
    def precision_recall(self):
        return plots.precision_recall(self.y_true, self.y_score, ax=gen_ax())

    @property
    def feature_importances(self):
        return plots.feature_importances(self.estimator,
                                         self.estimator.feature_importances_,
                                         ax=gen_ax())

    @property
    def precision_at_proportions(self):
        return plots.precision_at_proportions(self.y_true, self.y_score,
                                              ax=gen_ax())

    def generate_report(self, template, path=None):
        """
         Generate HTML report

        Parameters
        ----------
        template : markdown-formatted string or path to markdown file
            Template used for rendeing the report. Any attribute of this
            object can be included in the report using the {tag} format.
            e.g.'# Report{estimator_name}{roc}{precision_recall}'.
            Apart from every attribute, you can also use {date} and {date_utc}
            tags to include the date for the report generation using local
            and UTC timezones repectively.

        path : str
            Path to save the HTML report. If None, the function will return
            the HTML code.

        Returns
        -------
        report: str
            Returns the contents of the report if path is None.

        """
        return generate(self, template, path)

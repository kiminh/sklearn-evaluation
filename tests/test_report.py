from unittest import TestCase

from sklearn.dummy import DummyClassifier
from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split

from sklearn_evaluation.evaluate import ClassifierEvaluator

from sklearn_evaluation.report import parse_tags

class TestTagParsing(TestCase):
    def test_basic_parse(self):
        tags = parse_tags('{a}{b}{c}')
        self.assertEqual(tags, ['a', 'b', 'c'])

    def test_ignores_tags_with_spaces(self):
        tags = parse_tags('{a}{b}{ c }')
        self.assertEqual(tags, ['a', 'b'])

class TestReportGeneration(TestCase):
    def setUp(self):
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data,
                                                            iris.target,
                                                            test_size=0.30,
                                                            random_state=0)

        model = DummyClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_score = model.predict_proba(X_test)
        target_names = ['setosa', 'versicolor', 'virginica']
        feature_names = range(4)
        model_name = 'a model'

        self.results = ClassifierEvaluator(model=model, y_true=y_test,
                                           y_pred=y_pred, y_score=y_score,
                                           feature_names=feature_names,
                                           target_names=target_names,
                                           model_name=model_name)

        self.template = '# Report {confusion_matrix}{roc}{precision_recall}'

    def test_stuff(self):
        self.results.generate_report(self.template, '~/Desktop/report.html')

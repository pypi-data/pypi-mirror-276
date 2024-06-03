import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import unittest
from metrics_model_evaluation import (accuracy_score, 
                     confusion_matrix, 
                     f1_score,
                     mean_absolute_error, 
                     mean_squared_error,
                     precision_score, 
                     r2_score, 
                     recall_score)
from sklearn.metrics import (accuracy_score as sklearn_accuracy,
                             confusion_matrix as sklearn_confusion_matrix,
                             f1_score as sklearn_f1_score,
                             mean_absolute_error as sklearn_mae,
                             mean_squared_error as sklearn_mse,
                             precision_score as sklearn_precision,
                             r2_score as sklearn_r2,
                             recall_score as sklearn_recall)

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.y_true = [0, 2, 1, 3]
        self.y_pred = [0, 1, 2, 3]

    def test_accuracy_score(self):
        acc_custom = accuracy_score(self.y_true, self.y_pred)
        acc_sklearn = sklearn_accuracy(self.y_true, self.y_pred)
        self.assertAlmostEqual(acc_custom, acc_sklearn, places=5)

    def test_confusion_matrix(self):
        cm_custom = confusion_matrix(self.y_true, self.y_pred)
        cm_sklearn = sklearn_confusion_matrix(self.y_true, self.y_pred)
        self.assertTrue((cm_custom == cm_sklearn).all())

    def test_f1_score(self):
        f1_custom = f1_score(self.y_true, self.y_pred, average='micro')
        f1_sklearn = sklearn_f1_score(self.y_true, self.y_pred, average='micro')
        self.assertAlmostEqual(f1_custom, f1_sklearn, places=5)

    def test_mean_absolute_error(self):
        mae_custom = mean_absolute_error(self.y_true, self.y_pred)
        mae_sklearn = sklearn_mae(self.y_true, self.y_pred)
        self.assertAlmostEqual(mae_custom, mae_sklearn, places=5)

    def test_mean_squared_error(self):
        mse_custom = mean_squared_error(self.y_true, self.y_pred)
        mse_sklearn = sklearn_mse(self.y_true, self.y_pred)
        self.assertAlmostEqual(mse_custom, mse_sklearn, places=5)

    def test_precision_score(self):
        precision_custom = precision_score(self.y_true, self.y_pred, average='micro')
        precision_sklearn = sklearn_precision(self.y_true, self.y_pred, average='micro')
        self.assertAlmostEqual(precision_custom, precision_sklearn, places=5)

    def test_r2_score(self):
        r2_custom = r2_score(self.y_true, self.y_pred)
        r2_sklearn = sklearn_r2(self.y_true, self.y_pred)
        self.assertAlmostEqual(r2_custom, r2_sklearn, places=5)

    def test_recall_score(self):
        recall_custom = recall_score(self.y_true, self.y_pred, average='micro')
        recall_sklearn = sklearn_recall(self.y_true, self.y_pred, average='micro')
        self.assertAlmostEqual(recall_custom, recall_sklearn, places=5)

if __name__ == '__main__':
    unittest.main()

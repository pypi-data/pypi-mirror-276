import unittest
import pandas as pd
from fairbalance.mitigation_strategies import BalanceOutput, BalanceAttributes, BalanceOutputForAttributes
from fairbalance.processors import RandomOverSamplerProcessor


class TestBalanceOutput(unittest.TestCase) :
    
    def setUp(self) :
        data = {
            'feature1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'feature2': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'protected_attribute': ['A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'B'],
        }
        
        target = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        self.dataset = pd.DataFrame(data)
        self.target = pd.DataFrame(target, columns=["target"])
        self.protected_attribute = ["protected_attribute"]
        self.privilieged_group = {"protected_attribute" : "A"}
        self.cont_columns = ["feature2"]
        self.cat_columns = ["feature1", "protected_attribute"]
        self.mitigator = BalanceOutput(sampler = RandomOverSamplerProcessor())
        
    def test_balance(self) :
        self.setUp()
        X_balanced, y_balanced = self.mitigator.balance(self.dataset, self.target, self.protected_attribute, self.cont_columns, self.cat_columns)
        # assert that the transformed dataset has the same shape as the initial one 
        self.assertListEqual(self.dataset.columns.to_list(), X_balanced.columns.to_list())
        self.assertListEqual(self.target.columns.to_list(), y_balanced.columns.to_list())
        
        # assert that the output is balanced
        self.assertEqual(y_balanced.value_counts()[0], y_balanced.value_counts()[1])


class TestBalanceAttribute(unittest.TestCase) :
    
    def setUp(self) :
        data = {
            'feature1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'feature2': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'protected_attribute': ['A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'B'],
        }
        
        target = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        self.dataset = pd.DataFrame(data)
        self.target = pd.DataFrame(target, columns=["target"])
        self.protected_attribute = ["protected_attribute"]
        self.privilieged_group = {"protected_attribute" : "A"}
        self.cont_columns = ["feature2"]
        self.cat_columns = ["feature1", "protected_attribute"]
        self.mitigator = BalanceAttributes(sampler = RandomOverSamplerProcessor())
        
    def test_balance(self) :
        self.setUp()
        X_balanced, y_balanced = self.mitigator.balance(self.dataset, self.target, self.protected_attribute, self.cont_columns, self.cat_columns)
        # assert that the transformed dataset has the same shape as the initial one 
        self.assertListEqual(self.dataset.columns.to_list(), X_balanced.columns.to_list())
        self.assertListEqual(self.target.columns.to_list(), y_balanced.columns.to_list())
        
        # assert that the output is balanced
        self.assertEqual(X_balanced["protected_attribute"].value_counts()["A"], X_balanced["protected_attribute"].value_counts()["B"])
        
    
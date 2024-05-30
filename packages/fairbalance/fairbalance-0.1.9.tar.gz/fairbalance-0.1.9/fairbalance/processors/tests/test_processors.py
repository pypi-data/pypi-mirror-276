# import unittest
# import pandas as pd
# from _processors import RandomOverSamplerProcessor 

# class TestRandomOverProcessor(unittest.TestCase):
    
#     def __init__(self, methodName: str = "runTest") -> None:
#         super().__init__(methodName)
#         self.setUp()
        
#     def setUp(self) :
#         data = {
#             'feature1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#             'feature2': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
#             'protected_attribute': ['A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'B'],
#         }
        
#         target = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
#         self.dataset = pd.DataFrame(data)
#         self.target = pd.DataFrame(target, columns=["target"])
#         self.protected_attribute = ["protected_attribute"]
#         self.privilieged_group = {"protected_attribute" : "A"}
        
#         self.processor = RandomOverSamplerProcessor()
    
#     def test_process(self) :
#         self.X_processed, self.y_processed = self.processor._process(self.dataset, self.target)
#         self.assertTrue(self.dataset.equals(self.X_processed))
#         self.assertTrue(self.target.equals(self.y_processed))
        
#     def test_unprocess(self) :
#         self.X_unprocessed, self.y_unprocessed = self.processor._unprocess(self.X_processed, self.y_processed)
#         self.assertTrue(self.dataset.equals(self.X_unprocessed))
#         self.assertTrue(self.target.equals(self.y_unprocessed))
        

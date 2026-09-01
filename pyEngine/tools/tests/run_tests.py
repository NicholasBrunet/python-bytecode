import unittest
from .GenericPrettyTestRunner import GenericPrettyTestRunner 

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    suite = loader.discover(
        start_dir="tests", 
        pattern="FunctionTest.py",
        # top_level_dir="."
    )
    
    runner = GenericPrettyTestRunner()
    runner.run(suite)


import unittest
from utils.config import Config
from utils.langutils import *


class MyTestCase(unittest.TestCase):

    def test_something(self):
        conf = Config("../resources/devices.yaml")
        self.assertNotEqual(tree_fetch(lambda: conf.inputs["digital"]["name"], None), None, "structure exists")
        self.assertNotEqual(conf.rules[0]["from"], None, "structure exists")





if __name__ == '__main__':
    unittest.main()

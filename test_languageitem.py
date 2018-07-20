"""
Test module for languageitem 
"""

import unittest
from lexis import *

class LexisTest(unittest.TestCase):
    def setUp(self):
        self.lexis = Lexis()

    def test_lexis(self):
        self.assertEqual(self.lexis.__class__, Lexis)

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(LexisTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

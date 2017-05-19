import unittest


class FlowUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    suite1 = unittest.makeSuite(FlowUtilsTestCase, 'test')
    unittest.main()

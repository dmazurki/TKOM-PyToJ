import unittest
import ptj_lex_tests

testList =[
    ptj_lex_tests.IndentTest,
    ptj_lex_tests.LiteralTest]

testLoad = unittest.TestLoader()

caseList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    caseList.append(testSuite)

testSuite = unittest.TestSuite(caseList)

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(testSuite)
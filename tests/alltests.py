import unittest, environmenttest, membertest, braintest, helpertest
runner = unittest.TextTestRunner()
runner.run(environmenttest.EnvironmentTest.buildSuite())
runner.run(membertest.MemberTest.buildSuite())
runner.run(braintest.BrainTest.buildSuite())
runner.run(helpertest.HelperTest.buildSuite())
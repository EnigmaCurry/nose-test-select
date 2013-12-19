import unittest
import subprocess
import shlex
import re
import os

CLASS_TEST = re.compile('(.*) \((.*)\) ... .*')
FUNCTION_TEST = re.compile('(.*) ... .*')

class NoseTestSelectTests(unittest.TestCase):
    
    def testBlankConfig(self):
        tests = self.runnyNose('nosetests -v --test-select-config=blank.cfg suite1')
        self.assertEquals(tests, set(
            ['module_test1.submodule_test1.test1.Tester.method_test',
             'module_test1.submodule_test1.test1.Tester.method_test2',
             'module_test1.submodule_test1.test1.function_test',
             'module_test1.submodule_test1.test2.Tester.method_test',
             'module_test1.submodule_test1.test2.Tester.method_test2',
             'module_test1.submodule_test1.test2.function_test',
             'module_test2.submodule_test1.test1.Tester.method_test',
             'module_test2.submodule_test1.test1.Tester.method_test2',
             'module_test2.submodule_test1.test1.function_test',
             'module_test2.submodule_test1.test2.Tester.method_test',
             'module_test2.submodule_test1.test2.Tester.method_test2',
             'module_test2.submodule_test1.test2.function_test']))

    def testExcludeAllButOneMethod(self):
        tests = self.runnyNose('nosetests -v --test-select-config=exclude_all_but_one_method.cfg suite1')
        self.assertEquals(tests, set(
            ['module_test1.submodule_test1.test1.Tester.method_test']))

    def testExcludeAllButOneFunction(self):
        tests = self.runnyNose('nosetests -v --test-select-config=exclude_all_but_one_function.cfg suite1')
        self.assertEquals(tests, set(
            ['module_test1.submodule_test1.test1.function_test']))        

    def testIncludeAllButOneModule(self):
        tests = self.runnyNose('nosetests -v --test-select-config=include_all_but_one_module.cfg suite1')
        self.assertEquals(tests, set([
             'module_test1.submodule_test1.test2.Tester.method_test',
             'module_test1.submodule_test1.test2.Tester.method_test2',
             'module_test1.submodule_test1.test2.function_test',
             'module_test2.submodule_test1.test1.Tester.method_test',
             'module_test2.submodule_test1.test1.Tester.method_test2',
             'module_test2.submodule_test1.test1.function_test',
             'module_test2.submodule_test1.test2.Tester.method_test',
             'module_test2.submodule_test1.test2.Tester.method_test2',
             'module_test2.submodule_test1.test2.function_test']))

    def testExcludeModuleButIncludeSingleMethod(self):
        tests = self.runnyNose('nosetests -v --test-select-config=exclude_module_but_include_method.cfg suite1')
        self.assertEquals(tests, set(
            ['module_test1.submodule_test1.test1.Tester.method_test',
             'module_test1.submodule_test1.test2.Tester.method_test',
             'module_test1.submodule_test1.test2.Tester.method_test2',
             'module_test1.submodule_test1.test2.function_test',
             'module_test2.submodule_test1.test1.Tester.method_test',
             'module_test2.submodule_test1.test1.Tester.method_test2',
             'module_test2.submodule_test1.test1.function_test',
             'module_test2.submodule_test1.test2.Tester.method_test',
             'module_test2.submodule_test1.test2.Tester.method_test2',
             'module_test2.submodule_test1.test2.function_test']))
    
    def testWildCardMethod(self):
        tests = self.runnyNose('nosetests -v --test-select-config=include_wildcard_method.cfg suite1')
        self.assertEquals(tests, set(
            ['module_test1.submodule_test1.test1.Tester.method_test2',
             'module_test1.submodule_test1.test2.Tester.method_test2',
             'module_test2.submodule_test1.test1.Tester.method_test2',
             'module_test2.submodule_test1.test2.Tester.method_test2']))
        
    def testExcludeModuleMethod(self):
        tests = self.runnyNose('nosetests -v --test-select-config=exclude_module_method.cfg suite2')
        self.assertEquals(tests, set([
            'sstable_generation_loading_test.TestSSTableGenerationAndLoading.sstableloader_compression_snappy_to_deflate_test',
'sstable_generation_loading_test.TestSSTableGenerationAndLoading.sstableloader_compression_snappy_to_none_test',
'sstable_generation_loading_test.TestSSTableGenerationAndLoading.sstableloader_compression_snappy_to_snappy_test',
'sstable_generation_loading_test.TestSSTableGenerationAndLoading.sstableloader_compression_none_to_snappy_test'
        ]))


    def runnyNose(self, cmd):
        """run nosetests, return a list of the tests that ran"""
        assert('-v' in cmd)
        tests = []
        env = os.environ
        env['PYTHONPATH'] = os.path.abspath(os.path.join(os.getcwd(),os.path.pardir))
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE, env=env)
        for line in proc.communicate()[1].split('\n'):
            m = CLASS_TEST.match(line)
            if m:
                tests.append(m.groups(1)[1]+"."+m.groups(1)[0])
                continue
            m = FUNCTION_TEST.match(line)
            if m:
                tests.append(m.groups(1)[0])
                continue
            break
        return set(tests)


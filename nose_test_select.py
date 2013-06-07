import fnmatch
import os
import re
import logging
from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.nose_test_select')

class NoseTestSelect(Plugin):

    def options(self, parser, env=os.environ):
        super(NoseTestSelect, self).options(parser, env=env)
        parser.add_option(
            "--test-select-config", type="string",
            dest="test_select_config", metavar='FILE',
            default=env.get('NOSE_TEST_SELECT_CONFIG', False),
            help="A config file listing the patterns of tests to include "
            "and exclude.  [NOSE_TEST_SELECT_CONFIG]")
        
    def configure(self, options, conf):
        super(NoseTestSelect, self).configure(options, conf)
        
        self.current_context = None
        self.patterns = {'exclude':[], 'include':[]}

        if not options.test_select_config:
            self.enabled=False
            return
        self.enabled = True

        self.options = options
        
        if options.where:
            cwd = options.where
        else:
            cwd = os.getcwd()            

        # Read patterns from config file
        with open(options.test_select_config) as cfg:
            current_section = None
            for line in cfg:
                if line.strip().lower() == '[include]':
                    current_section = 'include'
                elif line.strip().lower() == '[exclude]':
                    current_section = 'exclude'
                else:
                    pattern = line.strip()
                    if pattern.startswith("#"):
                        continue # ignore comments
                    if len(pattern):
                        pattern = os.path.join(cwd, pattern)
                        if pattern.find(":") < 0:
                            # No method pattern was specified, match all:
                            pattern += ":*"
                        self.patterns[current_section].append(pattern)
                        
    def wantMethod(self, method):
        method_file = method.im_func.__code__.co_filename
        method_name = method.im_func.__name__
        class_name = method.im_class.__name__
        class_method_name = "%s.%s" % (class_name, method_name)

        for pattern in self.patterns['include']:
            file_pattern, method_pattern = pattern.split(':', 1)
            if fnmatch.fnmatch(method_file, file_pattern):
                # The file glob matches
                if fnmatch.fnmatch(class_method_name, method_pattern):
                    # The method glob matches
                    # but we still need to check if the regular nose
                    # testMatch pattern matches :
                    if re.match(self.options.testMatch, method_name):
                        log.info("Including method: %s:%s" % (method_file, class_method_name))
                        return True

        for pattern in self.patterns['exclude']:
            file_pattern, method_pattern = pattern.split(':', 1)
            if fnmatch.fnmatch(method_file, file_pattern) and \
               fnmatch.fnmatch(method_name, method_pattern):
                return False

        return None

    def wantFunction(self, function):
        pass

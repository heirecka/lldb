"""
Test lldb data formatter subsystem.
"""

from __future__ import print_function

import use_lldb_suite

import os, time
import lldb
from lldbtest import *
import lldbutil

class PtrToArrayDataFormatterTestCase(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    def test_with_run_command(self):
        """Test that LLDB handles the clang typeclass Paren correctly."""
        self.build()
        self.data_formatter_commands()

    def setUp(self):
        # Call super's setUp().
        TestBase.setUp(self)
        # Find the line number to break at.
        self.line = line_number('main.cpp', '// Set break point at this line.')

    def data_formatter_commands(self):
        """Test that LLDB handles the clang typeclass Paren correctly."""
        self.runCmd("file a.out", CURRENT_EXECUTABLE_SET)

        lldbutil.run_break_set_by_file_and_line (self, "main.cpp", self.line, num_expected_locations=1, loc_exact=True)

        self.runCmd("run", RUN_SUCCEEDED)

        # The stop reason of the thread should be breakpoint.
        self.expect("thread list", STOPPED_DUE_TO_BREAKPOINT,
            substrs = ['stopped',
                       'stop reason = breakpoint'])

        # This is the function to remove the custom formats in order to have a
        # clean slate for the next test case.
        def cleanup():
            self.runCmd('type format delete hex', check=False)
            self.runCmd('type summary clear', check=False)

        # Execute the cleanup function during test case tear down.
        self.addTearDownHook(cleanup)

        self.expect('p *(int (*)[3])foo',
            substrs = ['(int [3]) $','[0] = 1','[1] = 2','[2] = 3'])

        self.expect('p *(int (*)[3])foo', matching=False,
            substrs = ['01 00 00 00 02 00 00 00 03 00 00 00'])
        self.expect('p *(int (*)[3])foo', matching=False,
            substrs = ['0x000000030000000200000001'])
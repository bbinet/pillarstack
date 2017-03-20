import os
import unittest

import stack


class TestSlashConvert(unittest.TestCase):
    def test_relative(self):
        # start with unix-style
        source = "test/sub \n dir/file.txt"

        # convert to OS-specific separators; this is a no-op on unix-like systems
        os_slash = os.path.normpath(source)

        # check that the convert to unix-style gets us back to the start
        unix_slash = stack._to_unix_slashes(os_slash)
        self.assertEquals(unix_slash, source)


if __name__ == '__main__':
    unittest.main()
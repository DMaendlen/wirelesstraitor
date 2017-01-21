from unittest import TestSuite
from test_sigint import sigintsuite
from test_osint import osintsuite

alltests = TestSuite((sigintsuite, osintsuite))

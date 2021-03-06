import unittest
from mock import Mock, patch, call

from merkato.merkato import Merkato

class MerkatoTestCase(unittest.TestCase):
	def setUp(self):
		configuration = {"exchange": "tux", "privatekey": "abc123", "publickey": "def456"}
		self.merkato = Merkato(configuration, ticker='XMR', spread='15')

	def test_create_bid_ladder(self):
		pass

	def test_create_ask_ladder(self):
		pass

	def test_merge_orders(self):
		pass

	def test_update_order_book(self):
		pass

	def test_cancelrange(self):
		pass
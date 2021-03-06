import unittest
from mock import mock, patch, call
from freezegun import freeze_time

from merkato.exchanges.tux_exchange import TuxExchange

class TuxExchangeTestCase(unittest.TestCase):
	def setUp(self):
		auth = {"privatekey": "abc123", "publickey": "456def"}
		self.exchange = TuxExchange(auth)

	@freeze_time('2001-01-01T12:00:00.0000')
	@patch('merkato.exchanges.tux_exchange.requests.post')
	def test_create_signed_request(self, post_mock):
		query_params = {"foo": "bar"}

		self.exchange._create_signed_request(query_params)

		post_mock.assert_called_once_with(
			'https://tuxexchange.com/api', 
			data={
				'foo': 'bar', 
				'nonce': 978350400000
			}, 
			headers={
				'Key': '456def', 
				'Sign': 'fbc8f9574ddab11d841f25f33d02854fe4932c91695611a9262f444220c4eb09ea9544af45a17d398fa623fa983ba47d38cdfe0a65483444f241ef5b9b34c621'
			}, 
			timeout=15
		)

	@patch('merkato.exchanges.tux_exchange.TuxExchange._create_signed_request')
	def test_buy(self, signed_request_mock):
		response = self.exchange.buy(1, 0.001, 'XMR')

		signed_request_mock.assert_called_once_with({
			'method': 'buy', 
			'market': 'BTC', 
			'coin': 'XMR', 
			'amount': '1.00000000', 
			'price': '0.00100000'
		})

	@patch('merkato.exchanges.tux_exchange.TuxExchange._create_signed_request')
	def test_sell(self, signed_request_mock):
		response = self.exchange.sell(1, 0.001, 'XMR')

		signed_request_mock.assert_called_once_with({
			'method': 'sell', 
			'market': 'BTC', 
			'coin': 'XMR', 
			'amount': '1.00000000', 
			'price': '0.00100000'
		})

if __name__ == "__main__":
	unittest.main()

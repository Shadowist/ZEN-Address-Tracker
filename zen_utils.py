import requests
from datetime import datetime
import tzlocal

import exchange_utils

import logging
FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s(%(lineno)d): %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zen_tx_utils')
logger.setLevel(logging.INFO)

class zen_address_data():
	''' Stores relevant zen address data. '''
	zen_address = ""
	web_address = ""

	data = {}
	transactions = []
	tx_history = []

	def __init__(self, zen_address):
		self.zen_address = zen_address
		logger.info("Initializing: {}".format(self.zen_address))
		self.web_address = "http://explorer.zensystem.io/insight-api-zen/addr/{}".format(zen_address)
		self.refresh()
		logger.info("Initialization Complete!")

	def refresh(self):
		response = requests.post(self.web_address)
		self.data = response.json()
		self.poll_transactions()

	def poll_transactions(self):
		# Initialize Bittrex Class
		bittrex_api = exchange_utils.bittrex_api()

		logger.info("Polling transactions...".format(self.zen_address))
		self.transactions = self.data["transactions"]
		tx = []
		spent_addrs = []

		# Query receive transactions
		for index, entry in enumerate(self.transactions):
			zen_tx = zen_transaction_data(entry)
			logger.info("Query receive transaction: {0:s} ({1:.2f}%)".format(entry, (index + 1) / len(self.transactions) * 100))
			for tx_entry in zen_tx.data["vout"]:
				# We pull only the exact zen address we want
				if tx_entry['scriptPubKey']['addresses'][0] == self.zen_address:
					date = datetime.fromtimestamp(int(zen_tx.data['time']), tzlocal.get_localzone())
					logger.debug("value: {} time: {} spentTxId: {}".format(tx_entry['value'], date, tx_entry['spentTxId']))

					bittrex_data = bittrex_api.query(str(date))
					tx.append(
					[
						date,
						tx_entry['value'],
						None,
						None,
						bittrex_data[0],  # BTC-ZEN
						bittrex_data[1],  # USDT-BTC
						bittrex_data[2],  # USDT-ZEN
						float(tx_entry['value']) * bittrex_data[2],  # Received ($)
						0,  # Sent
						0,  # Fee
						0,  # After Fee
					])
					if tx_entry['spentTxId']:
						spent_addrs.append(tx_entry['spentTxId'])

		# Query spent transactions
		in_tx = []
		spent_addrs = list(dict.fromkeys(spent_addrs))
		for index, addr in enumerate(spent_addrs):
			zen_tx = zen_transaction_data(addr)
			logger.info("Query spent transaction: {0:s} ({1:.2f}%)".format(addr, (index + 1) / len(spent_addrs) * 100))
			date = datetime.fromtimestamp(int(zen_tx.data['time']), tzlocal.get_localzone())
			logger.debug("value: -{} fees: {} final: {} time: {}".format(zen_tx.data['valueIn'], zen_tx.data['fees'], zen_tx.data['valueOut'], date))
			bittrex_data = bittrex_api.query(str(date))
			in_tx.append(
			[
				date,
				"-{}".format(zen_tx.data['valueIn']),
				zen_tx.data['fees'],
				"-{}".format(zen_tx.data['valueOut']),
				bittrex_data[0],  # BTC-ZEN
				bittrex_data[1],  # USDT-BTC
				bittrex_data[2],  # USDT-ZEN
				0,  # Received ($)
				-1 * float(zen_tx.data['valueIn']) * bittrex_data[2],  # Sent ($)
				zen_tx.data['fees'] * bittrex_data[2],  # Fees ($)
				-1 * float(zen_tx.data['valueOut']) * bittrex_data[2]  # After Fees ($)
			])

		# Sort transactions by date
		for input_tx in in_tx:
			for index, entry in enumerate(tx):
				if entry[0] > input_tx[0]:
					pass
				else:
					tx.insert(index, input_tx)
					break

		self.tx_history = tx


class zen_transaction_data():
	''' Stores relevant transactions data. '''

	tx_address = ""
	web_address = ""
	data = {}

	def __init__(self, tx_address):
		self.tx_address = tx_address
		self.web_address = "http://explorer.zensystem.io/insight-api-zen/tx/{}".format(tx_address)
		self.refresh()

	def refresh(self):
		response = requests.post(self.web_address)
		self.data = response.json()

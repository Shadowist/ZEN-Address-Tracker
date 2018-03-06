import csv
import zen_utils

def main(zen_addr):
	zen_data = zen_utils.zen_address_data(zen_addr)

	with open(zen_addr + ".csv", 'w') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    wr.writerow(
		[
			"Date",
			"Value",
			"Fee",
			"After Fee",
			"BTC-ZEN",
			"USDT-BTC ($)",
			"USDT-ZEN ($)",
			"Received ($)",
			"Sent ($)",
			"Fees ($)",
			"After Fee ($)"
		])
	    for entry in zen_data.tx_history:
	    	wr.writerow(entry)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Usage: zen_tracker.py \"zen address\"")
	else:
		main(sys.argv[1])
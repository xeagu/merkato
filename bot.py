from merkato import merkato_config as config
from merkato.merkato import Merkato


def create_mutex_table():
    conn = sqlite3.connect('merkato.db')

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mutexes
                 (pair text, exchange text, owner text)''')

    conn.commit()
    conn.close()


def main():
    print("Merkato Alpha v0.1.1\n")

    configuration = config.get_config()

    if not configuration:
        raise Exception("Failed to get configuration.")

    print(configuration)
    merkato = Merkato(configuration)

    merkato.exchange.get_all_orders()

#        nonce = int(time.time()*1000)
#        response = exchange._sell_tux_nonce(nonce, float(1000), float(.00000450), 'PEPECASH')
#        print("-----------")
#        print(response)
#        response = exchange._sell_tux_nonce(nonce, float(1000), float(.00000450), 'PEPECASH')
#        print("-----------")
#        print(response)

    # Market making range specifications
#    polo_price     = input('What is the price on Poloniex? \n')
#    desired_spread = input('What spread would you like to use? (Recommended .0007-.0015) \n')
#    bid_ladder_min = input('What is the lowest the price could possibly go? (Recommend 0.005) \n') 
#    ask_ladder_max = input('What is the highest price to market make? (Recommend 0.025) \n')
#    total_btc      = input('How much BTC will you use for market making? \n')
#    total_xmr      = input('How much XMR will you use for market making? \n')

#    spread = float(desired_spread)

#    bid_ladder_max = str(float(polo_price) - spread/2)
#    print("Max: " + bid_ladder_max)

#    ask_ladder_min = str(float(polo_price) + spread/2)
#    print("Min: " + ask_ladder_min)

    # Cancel all existing orders
#    cancelrange(bid_ladder_min, ask_ladder_max)

    # Place a bid ladder
#    if float(total_btc) > 0:
#        bid_ladder("XMR", total_btc, bid_ladder_min, bid_ladder_max, '.00004')

    # Place an ask ladder
#    if float(total_xmr) > 0:
#        ask_ladder("XMR", total_xmr, ask_ladder_min, ask_ladder_max, '.00004')

    # Maintain the spread
#    print("Beginning spread maintainence.")
#    maintain_window(spread, "XMR")





if __name__ == '__main__':
    main()

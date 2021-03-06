#coding=utf-8

import trade_ut as trade
import sys

def left_side_method(pair, amount, buy_price, sell_price):
    buy_id = trade.trusted_buy(pair, amount, buy_price)
    print "buying~, id = "+buy_id
    if trade.test_order_closed(buy_id,0.1):
        print "bought~"
        sell_id = trade.trusted_sell(pair, amount, sell_price)
        print "selling~, id = "+sell_id
        if trade.test_order_closed(sell_id,3):
            return 'A great deal!'

def right_side_method(pair, amount, buy_price, sell_price):
    sell_id = trade.trusted_sell(pair, amount, sell_price)
    print "selling~, id = "+sell_id
    if trade.test_order_closed(sell_id,0.1):
        print "selled~"
        buy_id = trade.trusted_buy(pair, amount, buy_price)
        print "buying~, id = "+buy_id
        if trade.test_order_closed(buy_id,3):
            return 'A great deal!'

def simple_side():
    print "~~Usage:"
    print "~~$python strategy.py"
    print "~~or $python strategy.py left btc 1 8600 8700"
    print "~~Ctrl+C to quit!"
    try:
        side, pair, amount, buy_price, sell_price = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except IndexError:
        print "{left, right} {BTCUSDT, ETHUSDT, LTCUSDT} {amount} {price} {price}"
        order = raw_input("side pair amount buy_price sell_price:")
        side, pair, amount, buy_price, sell_price = order.split(" ")[0], order.split(" ")[1], order.split(" ")[2], order.split(" ")[3], order.split(" ")[4]

    while True:
        print "wait~"
        if side == 'left':
            print left_side_method(pair, amount, buy_price, sell_price)
        elif side == 'right':
            print right_side_method(pair, amount, buy_price, sell_price)
        else:
            print "error, running again~"

def stop_loss():
	pass

def auto_left_side(coin, amount, avg_price, earn_ratio, loss_ratio):
	pass

def auto_right_side(coin, amount, avg_price, earn_ratio, loss_ratio):
    sell_price = str(float(avg_price) * (1 + float(earn_ratio)))
    buy_price = str(float(avg_price) * (1 - float(earn_ratio)))

    sell_loss_price = str(float(avg_price) * (1 - float(loss_ratio)))
    # buy_loss_price = str(float(buy_price) * (1 + float(loss_ratio)))

    sell_id = trade.trusted_sell(coin, amount, sell_price)
    print "selling~, id = "+str(sell_id)
    while True:
    	if float(trade.get_last_price(coin.split('USDT')[0])) < float(sell_loss_price):
    		if trade.trusted_cancel_order(coin, sell_id):
    			sell_id = trade.trusted_sell(coin, amount, sell_loss_price)
    			print "stop loss, sell_id = "+str(sell_id)
    			return "stop loss"
    	elif trade.trusted_get_open_orders(coin, sell_id) == 'closed':
    		print "selled~"
    		break
    buy_id = trade.trusted_buy(coin, amount, buy_price)
    print "buying~, id = "+str(buy_id)
    while True:
    	if trade.trusted_get_open_orders(coin, buy_id) == 'closed':
    		print "bought"
    		break
    return 'A great deal!'

def auto_side():
    print "~~Usage:"
    print "~~$python strategy.py"
    print "~~or:"
    print "~~$python strategy.py right LTCUSDT 0.0001 0.001 0.05"
    print "~~Ctrl+C to quit!"
    try:
        side, coin, amount, earn_ratio, loss_ratio = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except IndexError:
        print "{left, right} {BTCUSDT, LTCUSDT} {amount} {earn_ratio} {loss_ratio}"
        order = raw_input("side coin amount earn_ratio loss_ratio:")
        side, coin, amount, earn_ratio, loss_ratio = order.split(" ")[0], order.split(" ")[1], order.split(" ")[2], order.split(" ")[3], order.split(" ")[4]

    avg_price = trade.get_last_price(coin.split('USDT')[0])
    #use neural network to predict the avg_price

    while True:
        print "wait~"
        if side == 'left':
            print auto_left_side(coin, amount, avg_price, earn_ratio, loss_ratio)
        elif side == 'right':
            print auto_right_side(coin, amount, avg_price, earn_ratio, loss_ratio)
        else:
            print "error, running again~"

def main():
    # simple_side()
    auto_side()

if __name__ == '__main__':
    main()

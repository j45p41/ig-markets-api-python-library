#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
IG Markets Stream API sample with Python
2015 FemtoTrader
"""

import datetime
import sys
import traceback
import logging

from trading_ig import (IGService, IGStreamService)
from trading_ig.config import config
from trading_ig.lightstreamer import Subscription

last = 0
lastopen = 0
lasthigh = 0
lastlow = 0
lastclose = 0


# A simple function acting as a Subscription listener
def on_prices_update(item_update):
    global last, lastopen, lasthigh,lastlow, lastclose



    # print("price: %s " % item_update)

    # if last != item_update['values']['UTM']:
    #
    #     stamp = int(last)/1000
    #     print(stamp)
    #     if stamp != 0: stamp = datetime.datetime.fromtimestamp(stamp).strftime('%c')
    #
    #     # print(stamp, '')

        # print('****************open: ', lastopen,'high: ', lasthigh,'low: ', lastlow,'close: ', lastclose,)
        # last = item_update['values']['UTM']
        # lastopen = item_update['values']['BID_OPEN']
        # lasthigh = item_update['values']['BID_HIGH']
        # lastlow = item_update['values']['BID_LOW']
        # lastclose = item_update['values']['BID_CLOSE']


    print('time', datetime.datetime.fromtimestamp(int(item_update['values']['UTM'])/1000).strftime('%c'),item_update['name'],  ' open: ', item_update['values']['BID_OPEN'], 'high: ', item_update['values']['BID_HIGH'], 'low: ', item_update['values']['BID_LOW'], 'close: ', item_update['values']['BID_CLOSE'], )








def on_account_update(balance_update):
    print("balance: %s " % balance_update)


def main():

    epics1 = ['CHART:CS.D.GBPEUR.MINI.IP:1MINUTE',
             'CHART:IR.D.10YEAR100.FWM2.IP:1MINUTE',
             'CHART:CC.D.LCO.UME.IP:1MINUTE',
             'CHART:CS.D.NZDUSD.MINI.IP:1MINUTE',
             'CHART:CS.D.USDCAD.MINI.IP:1MINUTE',
             'CHART:CS.D.USDJPY.MINI.IP:1MINUTE',
             'CHART:CO.D.RR.FWM1.IP:1MINUTE',
             'CHART:CO.D.O.FWM2.IP:1MINUTE',
             'CHART:IX.D.SPTRD.IFM.IP:1MINUTE',
             'CHART:IX.D.NASDAQ.IFE.IP:1MINUTE'
             ]

    epics2 = ['CHART:CS.D.GBPEUR.MINI.IP:1MINUTE']

    epics3 = ['CHART:IR.D.10YEAR100.FWM2.IP:1MINUTE']

    epics4 = ['CHART:CS.D.NZDUSD.MINI.IP:1MINUTE']



    epics2 = ['CHART:KA.D.ECHOGS.CASH.IP:1MINUTE']

    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    ig_service = IGService(
        config.username, config.password, config.api_key, config.acc_type
    )

    ig_stream_service = IGStreamService(ig_service)
    ig_session = ig_stream_service.create_session()
    # Ensure configured account is selected
    accounts = ig_session[u'accounts']
    for account in accounts:
        if account[u'accountId'] == config.acc_number:
            accountId = account[u'accountId']
            break
        else:
            print('Account not found: {0}'.format(config.acc_number))
            accountId = None
    ig_stream_service.connect(accountId)

    # Making a new Subscription in MERGE mode
    subscription_prices = Subscription(
        mode="MERGE",
        items=epics1,
        fields=["UTM", "BID_OPEN", "BID_HIGH", "BID_LOW", "BID_CLOSE"],
    )



    # adapter="QUOTE_ADAPTER")

    # Adding the "on_price_update" function to Subscription
    subscription_prices.addlistener(on_prices_update)

    # Registering the Subscription
    sub_key_prices = ig_stream_service.ls_client.subscribe(subscription_prices)

    # Making an other Subscription in MERGE mode
    subscription_account = Subscription(
        mode="MERGE",
        items=['ACCOUNT:'+accountId],
        fields=["AVAILABLE_CASH"],
    )
    #    #adapter="QUOTE_ADAPTER")



    # Registering the Subscription
    sub_key_account = ig_stream_service.ls_client.subscribe(subscription_account)

    input("{0:-^80}\n".format("HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
    LIGHTSTREAMER"))

    # Disconnecting
    ig_stream_service.disconnect()


if __name__ == '__main__':
    main()

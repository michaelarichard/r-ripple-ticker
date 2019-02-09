import locale
import praw
import re
import requests
import os
from datetime import datetime

def lambda_handler(event, context):

    # Settings
    #xrp_btc_url = 'http://www.cryptocoincharts.info/v2/api/tradingPair/xrp_btc'
    #xrp_usd_url = 'http://www.cryptocoincharts.info/v2/api/tradingPair/xrp_usd'
    #xrp_eur_url = 'http://www.cryptocoincharts.info/v2/api/tradingPair/xrp_eur'
    #btc_usd_url = 'http://www.cryptocoincharts.info/v2/api/tradingPair/btc_usd'

    ticker_url = 'https://api.coinmarketcap.com/v1/ticker/'
    ticker_url_eur = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR'

    subreddit_name = os.environ.get('REDDIT_SUBREDDIT')
    dryrun = False
    widget_shortName = 'Ripple Subreddit'
    up_symbol = '&#8679;'
    dn_symbol = '&#8681;'
    locale.setlocale(locale.LC_ALL, 'en_US')

    reddit = praw.Reddit(
        client_id = os.environ.get('REDDIT_CLIENT_ID'),
        client_secret = os.environ.get('REDDIT_CLIENT_SECRET'),
        password = os.environ.get('REDDIT_CLIENT_PASSWORD'),
        user_agent = 'rripple-bot-1.0',
        username = os.environ.get('REDDIT_CLIENT_USERNAME')
    )

    try: 
        # Get subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Get legacy sidebar (description) from subreddit
        sidebar = subreddit.mod.settings()['description']
        # Get ticker data
        usd_ticker_data = requests.get(ticker_url).json()
        eur_ticker_data = requests.get(ticker_url_eur).json()

        coins_usd = {}
        coins_eur = {}
        for coin in usd_ticker_data:
            coins_usd[coin['symbol']] = coin
        for coin in eur_ticker_data:
            coins_eur[coin['symbol']] = coin
            
        # XRP BTC
        xrp_btc_price = coins_usd['XRP']['price_btc']
        xrp_btc_change_pct = coins_usd['XRP']['percent_change_24h']
        xrp_btc_change_icon = up_symbol if float(xrp_btc_change_pct) > 0 else dn_symbol

        # XRP EUR
        xrp_eur_price = "{0:.3f}".format(float(coins_eur['XRP']['price_eur']))
        xrp_eur_change_pct = coins_eur['XRP']['percent_change_24h']
        xrp_eur_change_icon = up_symbol if float(xrp_eur_change_pct) > 0 else dn_symbol

        # XRP USD
        xrp_usd_price = "{0:.3f}".format(float(coins_usd['XRP']['price_usd']))
        xrp_usd_change_pct = coins_usd['XRP']['percent_change_24h']        
        xrp_usd_change_icon = up_symbol if float(xrp_usd_change_pct) > 0 else dn_symbol

        # BTC USD
        btc_usd_price = "{0:.2f}".format(float(coins_usd['BTC']['price_usd']))
        btc_usd_change_pct = coins_usd['BTC']['percent_change_24h']
        btc_usd_change_icon = up_symbol if float(btc_usd_change_pct) > 0 else dn_symbol


        updatetime = str(datetime.utcnow().strftime('%m-%d-%Y %H:%M'))

        # use a regex substitute replacement search for each currency

        # Text

        #> * BTC: Ƀ 0.00013851  -9.89%
        #* USD: $ 0.290467  -8.95%
        #* EUR: € 0.25658  -9.97%
        #* Updated: 05-23-2017 02:09:29 UTC

        sidebar = re.sub('> \* BTC: .*', '> * BTC: Ƀ {}  {}%'.format(xrp_btc_price, xrp_btc_change_pct), sidebar)
        sidebar = re.sub('\* USD: .*', '* USD: $ {}  {}%'.format(xrp_usd_price, xrp_usd_change_pct), sidebar)
        sidebar = re.sub('\* EUR: .*', '* EUR: € {}  {}%'.format(xrp_eur_price, xrp_eur_change_pct), sidebar)
        sidebar = re.sub('\* Updated: .*', '* Updated: {}'.format(updatetime), sidebar)
        
        # Ticker (h4)
        sidebar = re.sub('####\*\*.*',
            '####**&nbsp;&nbsp;&nbsp;XRP Values &#8680; BTC Ƀ {} {} {}%&nbsp;|&nbsp;'.format(xrp_btc_price, xrp_btc_change_icon, xrp_btc_change_pct) +
            'USD $ {} {} {}%&nbsp;|&nbsp;'.format(xrp_usd_price, xrp_usd_change_icon, xrp_usd_change_pct) +
            'EUR € {} {} {}%&nbsp;|&nbsp;'.format(xrp_eur_price, xrp_eur_change_icon, xrp_eur_change_pct) +
            'Updated {} UTC&emsp;**'.format(updatetime), sidebar)
            
        # Table
        
        # Symbol|Price|Change
        # :-:|:-:|:-:
        # Ƀ|0.000148|8.42%
        # $|0.338 |12.67%
        # €|0.292269|13.01%
        # Updated|05-23-2017 20:59:37|UTC
        # BTC|$ 3654.91|&#8679; 7.54%
        
        sidebar = re.sub('Ƀ\|.*', 'Ƀ|{}|{} {}%'.format(xrp_btc_price, xrp_btc_change_icon, xrp_btc_change_pct), sidebar)
        sidebar = re.sub('\$\|.*', '$|{}|{} {}%'.format(xrp_usd_price, xrp_usd_change_icon, xrp_usd_change_pct), sidebar)
        sidebar = re.sub('€\|.*', '€|{}|{} {}%'.format(xrp_eur_price, xrp_eur_change_icon, xrp_eur_change_pct), sidebar)
        sidebar = re.sub('Updated\|.*', 'Updated|{}|UTC'.format(updatetime), sidebar)
        # BTC_USD Price for baseline
        sidebar = re.sub('BTC\|.*', 'BTC|$ {}|{} {}%'.format(btc_usd_price, btc_usd_change_icon, btc_usd_change_pct), sidebar)
        if dryrun:
            print("\n######\n\n\nLEGACY_UPDATED:\n\n\n######\n\n{}".format(sidebar))
        else:
            # Actually update the legacy sidebar
            subreddit.mod.update(description=sidebar)

        # New Widget style
        text_area = None
        for widget in subreddit.widgets.sidebar:
            if isinstance(widget, praw.models.TextArea) and (widget.shortName == widget_shortName):
                text_area = widget
                break
        if dryrun:
            print("\n######\n\n\nWIDGET_OLD: '{}'\n\n\n######\n\n{}".format(text_area.shortName,text_area.text))

        new_sidebar = text_area.text

        # Widget style only has table format so far. Same as above.
        new_sidebar = re.sub('Ƀ\|.*', 'Ƀ|{}|{} {}%'.format(xrp_btc_price, xrp_btc_change_icon, xrp_btc_change_pct), new_sidebar)
        new_sidebar = re.sub('\$\|.*', '$|{}|{} {}%'.format(xrp_usd_price, xrp_usd_change_icon, xrp_usd_change_pct), new_sidebar)
        new_sidebar = re.sub('€\|.*', '€|{}|{} {}%'.format(xrp_eur_price, xrp_eur_change_icon, xrp_eur_change_pct), new_sidebar)
        new_sidebar = re.sub('Updated\|.*', 'Updated|{}|UTC'.format(updatetime), new_sidebar)
        new_sidebar = re.sub('BTC\|.*', 'BTC|$ {}|{} {}%'.format(btc_usd_price, btc_usd_change_icon, btc_usd_change_pct), new_sidebar)

        if dryrun:
            print("\n######\n\n\nWIDGET_UPDATED: '{}'\n\n\n######\n\n{}".format(text_area.shortName,new_sidebar))
        else:
            # Actually Update the ticker text area named widget_shortName
            text_area = text_area.mod.update(shortName=widget_shortName, text=new_sidebar)

    except:
        raise

    return 'Sidebar for {} updated at {}'.format(subreddit_name, updatetime)

lambda_handler(None,None)

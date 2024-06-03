import requests
from bs4 import BeautifulSoup


def data_extract():
    """
    gold price: {'24K Gold/gram': x}
    rate/USD: X
    bid: x
    ask: x
    :return:
    """

    try:
        r = requests.get('https://www.livepriceofgold.com/usa-gold-price.html#google_vignette')
    except Exception as e:
        print(e)
        return None

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')

        parent = soup.find('table', {'class': 'data-table-2'})

        # find change
        resultchange = parent.find('span', {'id': '22GXAUUSD_CHANGE'})
        change = resultchange.text

        # find rate/usd
        resultrate_usd = parent.find('td', {'data-price': 'GXAUUSD'})
        rate_usd = resultrate_usd.text

        # find bid
        resultbid = parent.find('td', {'data-price': 'GXAUUSD_BID'})
        bid = resultbid.text

        # find ask
        resultask = parent.find('td', {'data-price': 'GXAUUSD_ASK'})
        ask = resultask.text

        result = {
            '24k gold/gram': {
                'change': change,
                'rate/usd': rate_usd,
                'bid': bid,
                'ask': ask,
            }
        }

        return result

    else:
        return None


def show_data(result):
    if result is None:
        print('data not found')
        return None
    else:
        print('--Live Price of Gold in USA--')
        print('24k gold/gram')
        print('Change: ', result['24k gold/gram']['change'])
        print('Rate/USD: ', result['24k gold/gram']['rate/usd'])
        print('Bid: ', result['24k gold/gram']['bid'])
        print('Ask: ', result['24k gold/gram']['ask'])

if __name__ == '__main__':
    print('Aplikasi utama')
    result = data_extract()
    show_data(result)

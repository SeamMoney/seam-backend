import datetime
import requests

SWITCHBOARD_BASE="0x7d7e436f0b2aafde60774efb26ccc432cf881b677aca7faaf2a01879bd19fb8"

switchboard_pairs = [
    ("0x7b5f536d201280a10d33d8c2202a1892b1dd8247aecfef7762ea8e7565eac7b6",
    "ETH/USD"),
    ("0xdc7f6fbc4efe2995e1e37b9f73d113085e4ee3597d47210a2933ad3bf5b78774",
    "BTC/USD"),
    ("0x5af65afeeab555f8b742ce7fc2c539a5cb6a6fb2a6e6d96bc1b075fb28067808",
    "SOL/USD"),
    ("0xb8f20223af69dcbc33d29e8555e46d031915fc38cb1a4fff5d5167a1e08e8367",
    "APT/USD"),
    ("0xdc1045b4d9fd1f4221fc2f91b2090d88483ba9745f29cf2d96574611204659a5",
    "USDC/USD"),
    ("0x638b524fa794b1fba6cbe0e1af088d8dbbaaab48523ac9baab285587af318a8d",
    "tAPT/USD"),
]


class OracleClient():
    PYTH_BASE = 'https://xc-mainnet.pyth.network'
    APTOS_BASE = 'https://fullnode.mainnet.aptoslabs.com/v1'
    def __init__(self):
        self.connection = None
        self.cursor = None

    
    def get_price(self, account):
        res = requests.get(f'{self.PYTH_BASE}',
        params={
            "jsonrpc": "2.0",
            "method": "latest_price_feeds",
            "id" : 1
        }
        )
        print(res.json())
    def switchboard_price(self, oAccount,oPair):
        typef =f'{SWITCHBOARD_BASE}::aggregator::AggregatorHistoryData'
        typer =f'{SWITCHBOARD_BASE}::aggregator::AggregatorRound<{SWITCHBOARD_BASE}::aggregator::LatestConfirmedRound>'
        res = requests.get(f'{self.APTOS_BASE}/accounts/{oAccount}/resource/{typer}')
        data = res.json()['data']
        med = data['result']
        price = format_price(med['value'], med['dec'])
        # print(data.keys())
        timestamp = data['round_confirmed_timestamp']
        print("raw timestamp",float(timestamp))
        time = datetime.datetime.fromtimestamp(int(timestamp))
        print("time",time)
        
        # time = format_time(med['timestamp'])
        print(oPair,price)
        return [oPair,price,time]

    def update_switchboard(self):
        pairs = []
        for account, pair in switchboard_pairs:
            pairs.append(self.switchboard_price(account, pair))
        return pairs

def format_price(val,deg):
    return float(val) / 10 ** int(deg)


def format_time(val):
    return datetime.fromtimestamp(int(val) / 1000)

    
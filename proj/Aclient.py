import requests
NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"

class Aclient:

    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
    
    def get_user_txs(self, user_id):
        response = requests.post(self.rpc_url, )
        return

    def all_recent_txs(self):
        url = self.rpc_url+"/transactions"

        headers = {"Content-Type": "application/json"}

        response = requests.request("GET", url, headers=headers)
        try:
            json_response = response.json()
            print(json_response)
            for tx in json_response['data']:
                print(tx)
        except:
            print("No transactions found")
        return

    def get_account_transactions(self,address):
        user_dapps = {}
        response = requests.get(
            f"{NODE_URL}/accounts/{address}/transactions",
            params={"limit": 50}
            )
        try:
            resources = requests.get(
                f"{self.rpc_url}/accounts/{address}/resource/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
                )
            resources=resources.json()
            user_dapps["balance"] = int(dict(resources)['data']['coin']['value'])/100000000
        except:
            pass

        txs = response.json()
        txns_temp = []
        for tx in txs:
            try:
                txn = {}
                payload = tx['payload']
                to = payload['function'].split('::')[0]
                func = payload['function'].split('::')[2]
                mod = payload['function'].split('::')[1]
                txn['function'] = func
                txn['module'] = mod
                if to in dapp_dic.keys():
                    dapp_name = dapp_dic[to]
                    if dapp_name in user_dapps.keys():
                        user_dapps[dapp_name] = 1 + user_dapps[dapp_name]
                    else:
                        user_dapps[dapp_name] = 1
                txns_temp.append(txn)
            except:
                pass
        return txns_temp,user_dapps

        

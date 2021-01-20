import requests
import blockchain
import wallet

HACK_BLOCK_IDX = 2
HACKER_NODE_URL = 

miners_wallet = wallet.Wallet()
blockchain_address = miners_wallet.blockchain_address

def calculate_total_amount(chain,blockchain_address):
    total_amount = 0.0
    for block in chain:
        for transaction in block['transactions']:
            value = float(transaction['value'])
            if blockchain_address == \
                    transaction['recipient_blockchain_address']:
                total_amount += value
            if blockchain_address == \
                    transaction['sender_blockchain_address']:
                total_amount -= value
    return total_amount

def get_fifty_one_percentage_attack(valid_chain,hack_block_idx):

    # hacked_blockchain = blockchain.BlockChain(blockchain_address=blockchain_address)
    hacked_blockchain = blockchain.BlockChain(blockchain_address=blockchain_address,chain = valid_chain[:HACK_BLOCK_IDX])
    hacked_blockchain.add_transaction(sender_blockchain_address = "THE BLOCKCHAIN",recipient_blockchain_address="A HACKER",value=100.0)
    hacked_blockchain.mining()
    
    valid_chain_length = len(valid_chain)
    
    while valid_chain_length + 5 > len(hacked_blockchain.chain):
        hacked_blockchain.mining()
        if len(hacked_blockchain.chain) % 100 == 0:
            print("--------------------------------------")
            print("{} chain mined.(valid chain length:{})".format(len(hacked_blockchain.chain),valid_chain_length))
            print("--------------------------------------")

    return hacked_blockchain.chain


if __name__ == "__main__":
    response = requests.get(f'http://localhost:5000/chain')
    if response.status_code == 200:
        response_json = response.json()
        valid_chain = response_json['chain']

        # Validate Chain 
        print(blockchain.BlockChain().valid_chain(valid_chain)) # True
        print("Hacker's Coin:{} (Before 51% attack)".format(calculate_total_amount(valid_chain,"A HACKER")))

        hacked_chain = get_fifty_one_percentage_attack(valid_chain,HACK_BLOCK_IDX)
        print(blockchain.BlockChain().valid_chain(hacked_chain)) # True

        requests.put("{}/chain".format(HACKER_NODE_URL),json={"chain":hacked_chain})
        print("Hacker's Coin:{} (After 51% attack)".format(calculate_total_amount(hacked_chain,"A HACKER")))



        # 一つのノードに対してチェーンの上書きをするとき、本来なら,DBのデータを上書きするのだけど。。。
        # APIで代用する。


        # hacked_chain = valid_chain
        # fraudulent_transaction = {
        #   "recipient_blockchain_address": "A HACKER", 
        #   "sender_blockchain_address": "THE BLOCKCHAIN", 
        #   "value": 100.0
        # }
        # hacked_chain[HACK_BLOCK_IDX]["transactions"].append(fraudulent_transaction)
        # print(blockchain.BlockChain().valid_chain(hacked_chain)) # False

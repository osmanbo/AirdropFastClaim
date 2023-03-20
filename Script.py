from web3 import Web3
import requests
importimport time


your_private_key = "YOUR_PRIVATE_KEY"
your_address = "YOUR_ETH_ADDRESS"
claim_block_number = 16890400 #ARBITIMESTAMP


arbiscan_api_key = ""
arbiscan_url = f"https://api.arbiscan.io/api?module=proxy&action=eth_blockNumber&apikey={arbiscan_api_key}"
# Use ur own provider
w3 = Web3(Web3.HTTPProvider(
    f"https://speedy-nodes-nyc.moralis.io/{arbiscan_api_key}/arbitrum/mainnet"))

# FILL THIS WITH SMC ABI
contract_abi = [...]


contract_address = "0x912CE59144191C1204E64559FE8253a0e49E6548"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

your_account = w3.eth.account.privateKeyToAccount(your_private_key)


def claim_tokens():
    nonce = w3.eth.getTransactionCount(your_address)

    gas_price = w3.eth.gasPrice * 1.2

    # Replace 'claim_function_name' with the actual function name
    claim_txn = contract.functions.claim_function_name().buildTransaction({
        'from': your_address,
        'gas': 200000,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(claim_txn, your_private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Claim transaction sent: {txn_hash.hex()}")


while True:
    response = requests.get(arbiscan_url)
    if response.status_code == 200:
        current_block_number = int(response.json()['result'], 16)
        print(f"Current block number: {current_block_number}")

        if current_block_number >= claim_block_number:
            claim_tokens()
            break
    else:
        print("Error fetching block number")

    time.sleep(0.5)  

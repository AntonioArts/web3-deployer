import os
import json
from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider(os.getenv("NODE_PATH")))

chain_id = 42 # Kovan test net
deployer_address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create the contract
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
# Get account nonce
nonce = w3.eth.getTransactionCount(deployer_address)
# print(nonce)

transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": deployer_address, "nonce": nonce})
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)
# print(signed_txn)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# print(txn_hash)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
# print(txn_receipt)

simple_storage = w3.eth.contract(address = txn_receipt.contractAddress, abi = abi)

print(simple_storage.functions.retreive().call())

store_txn = simple_storage.functions.store(15).buildTransaction({"chainId": chain_id, "from": deployer_address, "nonce": nonce + 1})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key = private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print(store_txn_receipt)

print(simple_storage.functions.retreive().call())
import json
from substrateinterface import SubstrateInterface

# Step 1: Load ABI from file
with open("storage_contract.json", "r") as file:
    contract_data = json.load(file)

contract_abi = contract_data["abi"]
contract_address = contract_data["address"]

# Step 2: Connect to the Westend Asset Hub network
substrate = SubstrateInterface(
    url="https://westend-asset-hub-eth-rpc.polkadot.io",
    type_registry_preset="westend"
)

# Step 3: Initialize the contract
contract = Contract(
    substrate=substrate,
    address=contract_address,
    abi=contract_abi,
)

# Step 4: Call a view function like 'retrieve'
response = contract.query("retrieve", params=[], block_hash=None)
print("Stored value:", response.value)


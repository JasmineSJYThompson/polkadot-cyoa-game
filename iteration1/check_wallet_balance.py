from substrateinterface import SubstrateInterface

# Connect to the Substrate node (this is an example URL; replace with your node's URL)
substrate = SubstrateInterface(
    url="wss://rpc.polkadot.io",  # Use your node's WebSocket URL
    ss58_format=42,               # SS58 format for Polkadot (42 for Polkadot, 0 for Kusama, etc.)
    type_registry_preset='polkadot'
)

substrate = SubstrateInterface(
        url="wss://westend-asset-hub-rpc.polkadot.io",  # AssetHub-Westend RPC URL
        ss58_format=49,  # AssetHub-Westend ss58 format
        type_registry_preset="westend"  # Use the Westend type registry
)

# Specify the account address (replace with the wallet address you want to check)
address = "5DRrfL8JtBK6fVRKA8mSDW66GZPVQ8w6bN2yMKGZCqiDEBAc"

# Query the balance of the specified address
result = substrate.query(
    module='System',  # Module
    storage_function='Account',  # Storage function to retrieve the account balance
    params=[address]  # The address of the account
)

# Extract and print the free balance
free_balance = result['data']['free']  # Free balance (can also check reserved balance if needed)
print(f"Free Balance of address {address}: {free_balance} units")

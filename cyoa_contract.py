import json
from substrateinterface import SubstrateInterface, Keypair
from scalecodec.base import ScaleBytes

class CYOAContract:
    def __init__(self, mnemonic, contract_address, contract_metadata_path):
        self.substrate = SubstrateInterface(
            url="wss://westend-asset-hub-rpc.polkadot.io",
            ss58_format=42,
            type_registry_preset='westend'
        )
        self.keypair = Keypair.create_from_mnemonic(mnemonic)
        self.contract_address = contract_address

        # Load contract metadata
        with open(contract_metadata_path, 'r') as f:
            self.metadata = json.load(f)

        self.messages = {m['label']: m for m in self.metadata['V3']['spec']['messages']}

    def get_selector(self, method):
        return bytes.fromhex(self.messages[method]['selector'][2:])

    def call_contract(self, method, args=None, value=0):
        selector = self.get_selector(method)
        data = selector  # no args = selector only

        call = self.substrate.compose_call(
            call_module='Contracts',
            call_function='call',
            call_params={
                'dest': self.contract_address,
                'value': value,
                'gas_limit': 10_000_000_000,
                'storage_deposit_limit': None,
                'data': ScaleBytes(data)
            }
        )

        extrinsic = self.substrate.create_signed_extrinsic(call=call, keypair=self.keypair)
        receipt = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt

    def complete_game(self):
        return self.call_contract("complete_game")

    def has_player_completed(self, player_address):
        # Not supported in substrate-interface out of the box — needs off-chain query support
        raise NotImplementedError("For now, check manually in polkadot.js or add RPC extension")


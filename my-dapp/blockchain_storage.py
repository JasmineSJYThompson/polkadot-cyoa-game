# blockchain_storage.py

from substrateinterface import SubstrateInterface, Keypair
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blockchain.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlockchainStorage:
    def __init__(self, seed_phrase):
        # Initialize connection to Westend testnet
        self.substrate = SubstrateInterface(
            url="wss://westend-rpc.polkadot.io",
            ss58_format=42,
            type_registry_preset="westend"
        )
        self.mnemonic = seed_phrase
        logger.info("Blockchain storage initialized")

    def save_game(self, scene_key):
        """Save the current scene to the blockchain"""
        try:
            # Create keypair from mnemonic
            keypair = Keypair.create_from_mnemonic(self.mnemonic)
            
            # Create the remark with a consistent format
            remark = f"CYOA_SCENE:{scene_key}"
            logger.info(f"Preparing to save scene: {scene_key}")
            
            # Create the transaction
            call = self.substrate.compose_call(
                call_module='System',
                call_function='remark',
                call_params={
                    'remark': remark.encode()
                }
            )
            
            # Create and submit the transaction
            extrinsic = self.substrate.create_signed_extrinsic(
                call=call,
                keypair=keypair
            )
            
            # Wait for the transaction to be included in a block
            receipt = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
            block_hash = receipt.block_hash
            block_number = self.substrate.get_block_number(block_hash)
            
            logger.info(f"Scene {scene_key} saved in block {block_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save scene: {str(e)}")
            return False

    def load_game(self):
        """Load the last saved scene from the blockchain"""
        try:
            current_block = self.substrate.get_block_number(self.substrate.get_chain_head())
            logger.info(f"Searching for saved scene from block {current_block}")

            for block_number in range(current_block, max(0, current_block - 100), -1):
                block_hash = self.substrate.get_block_hash(block_number)
                block = self.substrate.get_block(block_hash)
                
                for extrinsic in block['extrinsics']:
                    extrinsic_str = str(extrinsic)
                    if 'remark' in extrinsic_str and 'CYOA_SCENE:' in extrinsic_str:
                        try:
                            scene_key = extrinsic_str.split('CYOA_SCENE:')[1].split("'")[0]
                            logger.info(f"Found saved scene {scene_key} in block {block_number}")
                            return scene_key
                        except Exception as e:
                            logger.error(f"Error parsing scene key: {e}")
                            continue
            
            logger.info("No saved scene found")
            return None
            
        except Exception as e:
            logger.error(f"Failed to load scene: {str(e)}")
            return None

    def check_balance(self):
        """Check the wallet balance"""
        try:
            keypair = Keypair.create_from_mnemonic(self.mnemonic)
            account_info = self.substrate.query('System', 'Account', [keypair.ss58_address])
            balance = account_info.value.get('data', {}).get('free', 0)
            balance_wnd = balance / 10**12  # Convert from planks to WND
            logger.info(f"Current balance: {balance_wnd} WND")
            return balance_wnd
        except Exception as e:
            logger.error(f"Failed to check balance: {str(e)}")
            return 0.0
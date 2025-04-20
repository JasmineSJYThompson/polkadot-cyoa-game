from substrateinterface import Keypair

seed_phrase = "farm act carpet risk until attitude ball payment evoke eight unlock rigid"

kp = Keypair.create_from_mnemonic()
print("Address:", kp.ss58_address)
print("Private key:", kp.private_key.hex())

# Address:5DRrfL8JtBK6fVRKA8mSDW66GZPVQ8w6bN2yMKGZCqiDEBAc
# Private key:8aa9519a0e94cde3eea598645b22be1bf8e033c9a2668a7f46300ec10c719b0e10b2805308f632e03af0886f35bbab7ba2f1f3e484af62caee6b365e8b034771
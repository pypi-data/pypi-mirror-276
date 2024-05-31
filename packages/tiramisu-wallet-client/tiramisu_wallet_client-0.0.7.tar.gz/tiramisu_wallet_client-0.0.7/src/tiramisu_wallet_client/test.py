# from tiramisu_wallet_client import TiramisuClient
from tiramisu_client import TiramisuClient
import random

# Please go to https://testnet.tarowallet.net/walletapp/ 
# and create an account then populate your credentials 
USER_NAME="username_here"
PASSWORD="password_here

# print("Register new user")
# client = TiramisuClient(username=USER_NAME, password=PASSWORD, network="mainnet",server_url="http://127.0.0.1:8000/walletapp/")

print("Create client object")
client = TiramisuClient(username=USER_NAME,password=PASSWORD, network='mainnet')

col =  client.nfts(collection_name="TaprootCans100")

res = client.transactions(offset=0, description="fee_user_1")


print("Asset detail")
asset_detail =  client.asset(id=2)
print(asset_detail)

print("List all wallet balances")
bal =  client.balances(offset=0)
print(bal)
bal =  client.balances_nft(offset=0)
print(bal)
col =  client.collections()
print(col)



col =  client.collections()
print(col)

print("Get info")
print(client.get_info())

print("Receive taproot assets")
res = client.transactions_receive_taproot_asset(amount=20,description="test",asset=16)
res = client.transaction(id=res['id'])
print(res)


# print("Buy taro")
# res = client.buy_taproot_asset_asset_wait_finished(asset=2,amount=1)
# print("Sell taro")
# res = client.sell_taproot_asset(asset=2,amount=1)

print("test send")
res = client.transactions_send_internal(destination_user=2181,asset=659,amount=100,description='test send')
print(res)

print("register asset")
res = client.asset_create(acronym='BLY', asset_id='53f795dc54c77403865a7d7ec71c1ed320b0203d5beef6dbe6cf060c5d52bb55')

print("Sell nft")
res = client.buy_nft_asset(1156)
print(res)



res = client.sell_taproot_asset

res = client.transactions_receive_btc(amount=20,description="test desc")
res = client.transaction(id=res['id'])
print(res)

res = client.transactions_receive_btc_lnd(amount=20,description="test desc")
res = client.transaction(id=res['id'])
print(res)

# res = client.transactions_send_internal(destination_user=123,asset=4,amount=1,description="test desc")
# res = client.transaction(id=res['id'])
# print(res)

# res = client.transactions_send_btc(
#     invoice_outbound="mvgYtgvYg8QkuZadQGk1xGaTyYVxwsNFzY",amount=30000
# )
# res = client.transaction(id=res['id'])
# print(res)


# res = client.transactions_send_btc_lnd(invoice_outbound="lntb100u1pnz2ahspp589czuqqdvap75acequtyl7msvwd49yrujrgz4txhc4zdzpz59xaqdqqcqzzsxqyz5vqsp5xur25umtgqxmwy26qn94ggmv838hmrh3cprs5ktc0hsh00s2tdms9qyyssqve0rk5yrn4vrp4zzgxesr20u4z8wlrkhtdvn4x8djlra4czvsgyk9wt3w2ez5fkylf735zpmrjpxyy6dkxzgwey4ady9vscttjt3kkcqcc473m")
# res = client.transaction(id=res['id'])
# print(res)
# aadasdas

print("List all notification")
print( client.notifications() )

print("List all collections")
print( client.collections() )

print("List all balances of NFTs in the wallet")
print( client.balances_nft() )

print("Get the BTC balance in wallet:")
print( client.get_btc_balance() )

print("List assets available")
assets=client.assets(offset=0)
print( assets )

print("List nfts available")
assets=client.nfts(offset=0)
print( assets )

print("Get first asset and print it")
asset=client.asset(4)
print( asset )

print("List wallet transactions")
print( client.transactions() )
print( client.transactions(offset=0) )

print(f"Buy asset '{asset['id']}'")
print( client.buy_taproot_asset_asset_wait_finished(asset=asset["id"], amount=1) )

print("Balances after purchase:")
print( client.balances() )

print("transactions_receive_btc")
transaction_inbound_btc = client.transactions_receive_btc_get_invoice(amount=10000, description='test BTC deposit')

print(f"send BTC to this address to top-up your BTC balance: {transaction_inbound_btc['invoice_inbound']}")

invoice_inbound_taproot_asset = client.transactions_receive_taproot_asset(amount=1, asset=asset['id'], description=f"receive asset {asset['id']}")

print(f"send Taproot asset {asset['name']} with ID {asset['id']} to this address to top-up your TAP balance: {invoice_inbound_taproot_asset}")

tn = random.randint(1, 1000)

print("Minting a new currency and waiting for minting to finish.")

new_asset = client.assets_mint_wait_finished(acronym=f'TC{tn}', name=f'Testasset{tn}', description=f'Test asset {tn}', supply=1234, file_path='test_image.jpg')

print("Newly created asset")
print(new_asset)

print("Listing the currency on an exchange...")
client.list_asset(asset=new_asset['id'])



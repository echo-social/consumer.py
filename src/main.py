import json, requests, logging, web3, os, time, datetime, first

from ocean_lib import aquarius, ocean
from ocean_lib.ocean.ocean import Ocean, OceanAssets
from ocean_lib.ocean.util import to_wei
from config import get_config_dict
from eth_account import Account
from ocean_lib.models.fixed_rate_exchange import (
  ExchangeArguments,
  FixedRateExchange,
  OneExchange
)
from ocean_lib.ocean.util import get_address_of_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

NETWORK_RPC = os.environ["NETWORK_RPC"]
AQUARIUS_URL = os.getenv("AQUARIUS_URL")
SUBGRAPH_URL = os.getenv("SUBGRAPH_URL")
MAX_GAS_PRICE = int(os.getenv("MAX_GAS_PRICE"))

DID = os.getenv("DID")

WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
consumer = Account.from_key(private_key=WALLET_PRIVATE_KEY)

config = get_config_dict(NETWORK_RPC)
ocean = Ocean(config)
OCEAN = ocean.OCEAN_token

aquarius = aquarius.Aquarius(AQUARIUS_URL)
asset = aquarius.get_ddo(DID)
datatoken_address = asset.datatokens[0]["address"]
logger.info({'asset': asset.as_dictionary()})

with open("erc20.json", "r") as fp:
  erc20_abi = json.loads(fp.read())
w3 = web3.Web3(web3.Web3.HTTPProvider(NETWORK_RPC))
token = w3.eth.contract(address=web3.Web3.to_checksum_address(datatoken_address.lower()), abi=erc20_abi)
balance = token.functions.balanceOf(web3.Web3.to_checksum_address(consumer.address.lower())).call()
decimals = token.functions.decimals().call()
logger.info({'balance': balance / 10 ** decimals})

# # Find the exchange id in order to swap base token to dataset token
# # TODO: use server filter
# query = """
# {
#   fixedRateExchanges(subgraphError:deny){
#     id
#     contract
#     exchangeId
#     owner{id}
#     datatoken{
#       id
#       name
#       symbol
#     }
#     price
#     datatokenBalance
#     active
#     totalSwapValue
#     swaps(skip:0, first:1){
#       tx
#       by {
#         id
#       }
#       baseTokenAmount
#       dataTokenAmount
#       createdTimestamp
#     }
#     updates(skip:0, first:1){
#       oldPrice
#       newPrice
#       newActive
#       createdTimestamp
#       tx
#     }
#   }
# }"""


# headers = {"Content-Type": "application/json"}
# payload = json.dumps({"query": query})
# response = requests.request("POST", SUBGRAPH_URL, headers=headers, data=payload)
# fre_infos = json.loads(response.text)

# one_exchange_info = first.first(
#   fre_infos["data"]["fixedRateExchanges"],
#   key=lambda fre_info: fre_info['datatoken']['id'].lower() == datatoken_address.lower())
# logger.info({'exchange_info': one_exchange_info})

# fre_addr = get_address_of_type(config, "FixedPrice")
# fre = FixedRateExchange(config, fre_addr)
# logger.info({'fixed_rate_exchange': fre})

# one_exchange = OneExchange(fre, exchange_id=one_exchange_info['exchangeId'])
# logger.info({'one_exchange': one_exchange})

# # Approve tokens
# tokens_needed = one_exchange.BT_needed(to_wei(1), consume_market_fee=0)
# ocean.OCEAN_token.approve(one_exchange.address, tokens_needed, {"from": consumer, "gasPrice": MAX_GAS_PRICE})

# # Buy data token
# one_exchange.buy_DT(to_wei(1), consume_market_fee=0, tx_dict={"from": consumer, "gasPrice": MAX_GAS_PRICE})

# Submit order
order_tx_id = ocean.assets.pay_for_access_service(asset, {"from": consumer, "gasPrice": MAX_GAS_PRICE})
logger.info({'order_tx_id': order_tx_id})

# Download the dataset
asset_dir = ocean.assets.download_asset(asset, consumer, './', order_tx_id.hex())

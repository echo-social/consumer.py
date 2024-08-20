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

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

# Load environment variables
NETWORK_RPC = os.getenv("NETWORK_RPC")
AQUARIUS_URL = os.getenv("AQUARIUS_URL")
SUBGRAPH_URL = os.getenv("SUBGRAPH_URL")
MAX_GAS_PRICE = os.getenv("MAX_GAS_PRICE")
DID = os.getenv("DID")
WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")

# Check if all required environment variables are set, exit if any are missing
if not all([NETWORK_RPC, AQUARIUS_URL, SUBGRAPH_URL, MAX_GAS_PRICE, DID, WALLET_PRIVATE_KEY]):
    logger.error("One or more required environment variables are not set")
    exit(1)

# Convert max gas price to integer
MAX_GAS_PRICE = int(MAX_GAS_PRICE)

# Initialize the Ethereum account from the provided private key
consumer = Account.from_key(private_key=WALLET_PRIVATE_KEY)

# Load the blockchain network configuration
config = get_config_dict(NETWORK_RPC)
ocean = Ocean(config)

# Get an instance of Aquarius which is part of Ocean Protocol's tools for assets metadata
aquarius_instance = aquarius.Aquarius(AQUARIUS_URL)
asset = aquarius_instance.get_ddo(DID)
if not asset:
    logger.error(f"Asset with DID {DID} not found")
    exit(1)

# Fetch the datatoken address associated with the asset
datatoken_address = asset.datatokens[0]["address"]
logger.info({'asset': asset.as_dictionary()})
logger.info(f"Datatoken address fetched: {datatoken_address}")

# Establish a Web3 connection
w3 = web3.Web3(web3.Web3.HTTPProvider(NETWORK_RPC))
with open("erc20.json", "r") as fp:
    erc20_abi = json.loads(fp.read())
token = w3.eth.contract(address=web3.Web3.to_checksum_address(datatoken_address.lower()), abi=erc20_abi)

# Construct a GraphQL query to fetch exchange information from the Ocean Protocol's subgraph
query = """
{
  fixedRateExchanges(subgraphError:deny, first: 1000, orderBy: createdTimestamp, orderDirection: desc){
    id
    contract
    exchangeId
    owner{id}
    createdTimestamp
    datatoken{
      id
      name
      symbol
    }
    price
    datatokenBalance
    active
    totalSwapValue
    swaps(skip:0, first:1){
      tx
      by {
        id
      }
      baseTokenAmount
      dataTokenAmount
      createdTimestamp
    }
    updates(skip:0, first:1){
      oldPrice
      newPrice
      newActive
      createdTimestamp
      tx
    }
  }
}"""
headers = {"Content-Type": "application/json"}
payload = json.dumps({"query": query})
response = requests.request("POST", SUBGRAPH_URL, headers=headers, data=payload)
fre_infos = json.loads(response.text)

# Handle errors in fetching exchange info
if "data" not in fre_infos or "fixedRateExchanges" not in fre_infos["data"]:
    logger.error("Error fetching exchange info from subgraph")
    exit(1)

# Fetch the first exchange info matching the datatoken
one_exchange_info = first.first(
    fre_infos["data"]["fixedRateExchanges"],
    key=lambda fre_info: fre_info['datatoken']['id'].lower() == datatoken_address.lower()
)
logger.info({'exchange_info': one_exchange_info})

# Get the address for fixed price exchanges
fre_addr = get_address_of_type(config, "FixedPrice")
fre = FixedRateExchange(config, fre_addr)
logger.info({'fixed_rate_exchange': fre})

# Initialize the fixed rate exchange with the fetched information
one_exchange = OneExchange(fre, exchange_id=one_exchange_info['exchangeId'])
logger.info({'one_exchange': one_exchange})

# Approve tokens for exchange
tokens_needed = one_exchange.BT_needed(to_wei(1), consume_market_fee=0)
ocean.OCEAN_token.approve(one_exchange.address, tokens_needed, {"from": consumer, "gasPrice": MAX_GAS_PRICE})

# Purchase the data token
one_exchange.buy_DT(to_wei(1), consume_market_fee=0, tx_dict={"from": consumer, "gasPrice": MAX_GAS_PRICE})

# Submit order to access the asset
order_tx_id = ocean.assets.pay_for_access_service(asset, {"from": consumer, "gasPrice": MAX_GAS_PRICE})
logger.info({'order_tx_id': order_tx_id})

# Download the dataset to the specified directory
asset_dir = ocean.assets.download_asset(asset, consumer, './', order_tx_id.hex())

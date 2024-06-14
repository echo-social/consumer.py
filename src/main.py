import json, requests, logging, web3, os, time, datetime

from ocean_lib import aquarius, ocean
from ocean_lib.ocean.ocean import Ocean, OceanAssets
from ocean_lib.ocean.util import to_wei
from config import get_config_dict
from eth_account import Account

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

NETWORK_RPC = os.environ["NETWORK_RPC"]
AQUARIUS_URL = os.getenv("AQUARIUS_URL")
SUBGRAPH_URL = os.getenv("SUBGRAPH_URL")
DID = os.getenv("DID")

WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
consumer = Account.from_key(private_key=WALLET_PRIVATE_KEY)

config = get_config_dict(NETWORK_RPC)
ocean = Ocean(config)
OCEAN = ocean.OCEAN_token

aquarius = aquarius.Aquarius(AQUARIUS_URL)
asset = aquarius.get_ddo(DID)
datatokenAddress = asset.datatokens[0]["address"]
logger.info(datatokenAddress)

logger.info("----")

query = """
{
  fixedRateExchanges(subgraphError:deny){
    id
    contract
    exchangeId
    owner{id}
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
fixedRateExchanges = json.loads(response.text)

exchangeDict = None
for fixedRateExchange in fixedRateExchanges["data"]["fixedRateExchanges"]:
    logger.info(fixedRateExchange['datatoken']['id'].lower())
    if fixedRateExchange['datatoken']['id'].lower() == datatokenAddress.lower():
        exchangeDict = fixedRateExchange
        break
logger.info(exchangeDict)

#OCEAN.approve(ocean.fixed_rate_exchange.address, 150, {"from": consumer})

# create exchange from exchange dict
# exchange.buy_DT(to_wei(1), consume_market_fee=0, tx_dict={"from": consumer})

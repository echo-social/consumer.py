# consumer.py

The main purpose of this repository is to provide an example of how to buy Oceanprotocol datasets published on [Taraxa](https://www.taraxa.io) using Python.
You can find the market UI for the [Oceanprotocol stack](https://oceanprotocol.com/) at [market.echo-social](https://market.echo-social.io/).

# Environment vars
This project uses the following environment variables:

| Name | Description | Default Value | Example |
| ---- | ----------- | ------------- | ------- |
| NETWORK_RPC            | Network RPC           | None      | https://rpc.mainnet.taraxa.io |
| AQUARIUS_URL           | Aquarius URL          | None      | https://aquarius.echo-social.io |
| SUBGRAPH_URL           | Subgraph URL          | None      | https://indexer.echo-social.io/subgraphs/name/oceanprotocol/ocean-subgraph |
| ADDRESS_FILE           | Oceanprotocol contract addresses          | None      | ./address.json |
| WALLET_PRIVATE_KEY     | Buyer wallet private key         | None      | 0x... |
| DID                    | Document ID to buy | None | did:op:... |

## Usage

1. Clone the repository
    ```
    git clone https://github.com/echo-social/consumer.py.git consumer.py
    ```

2. Create a Python virtual environment.

    ```
    cd consumer.py
    python -m venv .venv
    ```

3. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

5. Configure env vars

    For example,
    ```
    cp .env.testnet .env
    ```

    And then specify the wallet private key and the document id.    

6. Run the project

    ```
    dotenv ./.venv/bin/python src/main.py
    ```


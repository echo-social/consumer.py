# Getting Started Guide for Echo Data Marketplace App

Welcome to the Echo Data Marketplace App! This guide will walk you through the setup process and introduce you to the foundational concepts that power the application. This app utilizes the Ocean Protocol on the Taraxa blockchain to facilitate a marketplace for Telegram data.
You can find the market UI for the [Oceanprotocol stack](https://oceanprotocol.com/) at [market.echo-social](https://market.echo-social.io/).

# Prerequisites

- Python 3.6+
- Git
- Virtualenv (optional but recommended)

# Setup Instructions

# 1. Clone the Repository

Start by cloning the repository to your local environment using Git:

    git clone https://github.com/echo-social/consumer.py.git echo-consumer

# 2. Create a Python Virtual Environment
Navigate into the cloned directory and create a virtual environment:

    cd echo-consumer
    python -m venv .venv
    source .venv/bin/activate

# 3. Install Dependencies
Install the necessary Python packages:

    pip install -r requirements.txt

# Configuration
## Environment Variables

This project uses the following environment variables:

| Name | Description | Default Value | Example |
| ---- | ----------- | ------------- | ------- |
| NETWORK_RPC            | Network RPC           | None      | https://rpc.mainnet.taraxa.io |
| AQUARIUS_URL           | Aquarius URL          | None      | https://aquarius.echo-social.io |
| SUBGRAPH_URL           | Subgraph URL          | None      | https://indexer.echo-social.io/subgraphs/name/oceanprotocol/ocean-subgraph |
| ADDRESS_FILE           | Oceanprotocol contract addresses          | None      | ./address.json |
| WALLET_PRIVATE_KEY     | Buyer wallet private key         | None      | 0x... |
| DID                    | Document ID to buy | None | did:op:... |

Configure the necessary environment variables. Begin by copying the sample environment configuration file:

    cp .env.testnet .env


Edit the .env file with specifics, such as network RPC URL, Aquarius URL, Subgraph URL, wallet private key, and the DID of the dataset you wish to purchase.

## Obtaining the DID
To experiment with buying data, you'll need a unique identifier known as a Decentralized Identifier (DID). Here's how to obtain one:

- Visit the Echo Data Marketplace.
- Browse through the available datasets and select a specific hour of data that interests you.
- Click on the dataset to view its details.
- Find the DID associated with the dataset (usually listed prominently) and copy it.
- Paste this DID into the .env file under the DID variable.

This DID will link directly to the data you aim to download.

# Requesting ECHO Tokens
To buy the Data Tokens needed for accessing datasets, you will need ECHO tokens. You can request ECHO tokens by:

- Joining the [Taraxa Discord](https://discord.com/invite/WaXnwUb) and asking in the social-analytics channel.
- Alternatively, you can contact us through our [Taraxa Telegram](https://t.me/taraxa_project) channel.

# Running the Application
Execute the application with the configured environment variables:

    dotenv python src/main.py

Once the script runs successfully, it will download the dataset and save it in a zip file format in the root directory of the repository. You can then extract this zip file to access the individual files for chats, messages, and users for that specific hour of data.

# Understanding Key Terms

**Decentralized Identifier (DID):** A unique identifier for your data NFT in the Ocean Protocol, crucial for accessing specific datasets.

**Decentralized Identifier Document (DDO):** Contains metadata for your data NFT, including title, description, and pricing, which can be fetched using the DID.

**Data NFT:** Represents the actual dataset published on the Ocean market, including the downloadable file.

**Data Token:** Acts as a key granting access to the dataset associated with a Data NFT, purchasable on the Ocean market using ECHO tokens.

**ECHO Token:** Used within the app to buy Data Tokens, which are necessary to access and download datasets.

# Workflow Summary

Publishing an Asset: Data is published as a Data NFT on the Ocean Protocol.
Buying Access: Users purchase Data Tokens using ECHO Tokens to access datasets.
Using the Dataset: With the Data Token, users can download or utilize the data.
Additional Resources
For more detailed information about the technologies and protocols used in this app, visit the Ocean Protocol developers documentation.

# Troubleshooting

Ensure all environment variables are accurately set, check network connectivity, and confirm sufficient wallet funds for transactions (i.e., TARA).

# Conclusion

This guide provides the necessary steps to get started with the Echo Data Marketplace App, alongside key concepts to understand the underlying technologies. For further assistance, consider visiting our community forum or the GitHub issues page.
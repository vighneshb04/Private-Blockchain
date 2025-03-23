# Private Blockchain with Multi-Threading and Ganache

## Overview
This project implements a **private blockchain** using **Ganache** for Ethereum development, integrating **multi-threading** to optimize transaction processing and smart contract execution. The system supports peer-to-peer transaction broadcasting and local ledger storage.

## Features
- **Private Blockchain:** Uses **Ganache** for local blockchain simulation.
- **Multi-Threading:** Optimizes transaction validation and smart contract execution.
- **Peer-to-Peer Transaction Broadcasting:** Nodes communicate and share transactions.
- **Smart Contract Execution:** Uses **Solidity-based smart contracts**.
- **On-Chain Balance Tracking:** Fetches **ETH and token balances**.

## Technologies Used
- **Python** (Sockets, Multi-threading, Web3.py)
- **Solidity** (Smart Contract Development)
- **Ganache** (Ethereum Local Blockchain)
- **Node.js & Express** (Optional for API Handling)

## Setup Instructions
### 1. Install Dependencies
```sh
pip install web3 json socket threading
```

### 2. Run Ganache
Start **Ganache** and ensure it's running on `http://127.0.0.1:7545`.

### 3. Update Configurations
Modify the following variables in `server.py`:
```python
NODE_IP = "192.168.x.x"
NODE_PORT = 8000
PRIVATE_KEY = "your_private_key_here"
ADDRESS = web3.to_checksum_address("your_ethereum_address_here")
PEERS = [
    {"ip": "192.168.x.x", "port": 8001},  # Node A
    {"ip": "192.168.x.x", "port": 8002}   # Node C
]
```

### 4. Start the Blockchain Node
Run the following command to start the server:
```sh
python server.py
```

## Usage
### Sending Transactions
1. Start the blockchain node.
2. Select `1` from the menu to send a transaction.
3. Enter recipient address, ETH amount, and token amount.

### Viewing Transactions
- Select `2` to view locally stored transactions.

### Checking Balances
- Select `3` to view on-chain ETH and token balances.

### Exit
- Select `4` to exit the program.

## Challenges & Learnings
- **Thread Synchronization:** Managing multi-threaded transaction handling.
- **Efficient Transaction Processing:** Optimizing smart contract execution.
- **Data Consistency:** Ensuring peer-to-peer transaction integrity.

## Future Enhancements
- **Zero-Knowledge Proofs (ZKP):** Enhance privacy for transactions.
- **Layer 2 Integration:** Improve scalability using rollups.
- **Web Dashboard:** UI for transaction and balance monitoring.

---

### 🚀 **This private blockchain system leverages multi-threading and peer-to-peer communication for efficient and secure decentralized transactions!**


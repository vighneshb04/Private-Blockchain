import socket
import threading
import json
import time
from web3 import Web3

# Web3 and Ganache setup
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Node configuration
NODE_IP = "10.113.9.82"
NODE_PORT = 8001

PRIVATE_KEY = "0xbb87e52886e70ef14f333355163cd753acc354cb93de6905fee7abeca79f168f"
ADDRESS = web3.to_checksum_address("0x523C1432E254A19347A88e4cc709b4e0b4c77E75")

PEERS = [
    {"ip": "10.113.16.73", "port": 8000},  # Node A
    {"ip": "192.168.68.110", "port": 8002}   # Node C
]

transactions = []

CONTRACT_ADDRESS = "0xaE036c65C649172b43ef7156b009c6221B596B8b"

# ABI for TransactionLogger contract
CONTRACT_ABI = json.loads("""[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_initialSupply",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "TransferETH",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_tokenAmount",
				"type": "uint256"
			}
		],
		"name": "transferWithEth",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]""")  

# Create contract instance
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# ----------------------------------------------
# Broadcast TX to peers
def broadcast_transaction(tx_data):
    for peer in PEERS:
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer["ip"], peer["port"]))
            peer_socket.send(json.dumps(tx_data).encode('utf-8'))
            peer_socket.close()
            print(f"[{NODE_IP}] Broadcasted TX to {peer['ip']}:{peer['port']}")
        except Exception as e:
            print(f"[{NODE_IP}] Failed to send TX to {peer['ip']}: {str(e)}")

# ----------------------------------------------
# Handle incoming TX from peers
def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        tx = json.loads(data)
        transactions.append(tx)
        print(f"[{NODE_IP}] Received TX: {tx}")

        with open("transactions_log.txt", "a") as file:
            file.write(json.dumps(tx) + "\n")

    except Exception as e:
        print(f"[{NODE_IP}] Error receiving TX: {str(e)}")
    finally:
        client_socket.close()

# ----------------------------------------------
# Start socket server thread
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((NODE_IP, NODE_PORT))
    server_socket.listen(5)
    print(f"[{NODE_IP}] Listening on port {NODE_PORT}")

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# ----------------------------------------------
# Send Transaction (uses transferWithEth)
def send_transaction(to_address, eth_amount, token_amount):
    global web3, contract

    nonce = web3.eth.get_transaction_count(ADDRESS)

    # Convert recipient to checksum address
    to_address = web3.to_checksum_address(to_address)

    # Convert ETH amount to Wei
    eth_amount_wei = web3.to_wei(eth_amount, 'ether')

    try:
        # Call transferWithEth function (needs to be payable)
        txn = contract.functions.transferWithEth(
            to_address,
            int(token_amount)  # assuming tokenAmount is in basic units
        ).build_transaction({
            'from': ADDRESS,
            'value': eth_amount_wei,
            'gas': 300000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce
        })

        # Sign and send the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        print(f"[{NODE_IP}] Sent Contract TX Hash: {web3.to_hex(tx_hash)}")

        # Log and broadcast transaction data
        tx_data = {
            "from": ADDRESS,
            "to": to_address,
            "eth_amount": eth_amount,
            "token_amount": token_amount,
            "timestamp": time.time(),
            "tx_hash": web3.to_hex(tx_hash)
        }

        transactions.append(tx_data)
        broadcast_transaction(tx_data)

    except Exception as e:
        print(f"Error sending transaction: {str(e)}")


if __name__ == '__main__':
    threading.Thread(target=start_server).start()

    while True:
        print("\n1. Send Transaction (Smart Contract)")
        print("2. View Transactions (Local Ledger)")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            to_address = input("Enter recipient address: ")
            eth_amount = float(input("Enter ETH amount to send: "))
            token_amount = int(input("Enter token amount to transfer: "))
            send_transaction(to_address, eth_amount, token_amount)

        elif choice == "2":
            print("\n[Local Ledger Transactions]")
            for tx in transactions:
                print(tx)

        elif choice == "3":
            print("Exiting...")
            break







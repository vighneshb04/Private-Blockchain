// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BlockchainTransaction {
    struct Transaction {
        address sender;
        address receiver;
        uint amount;
        uint timestamp;
    }

    Transaction[] public transactions;

    event TransactionCreated(address indexed sender, address indexed receiver, uint amount, uint timestamp);

    function addTransaction(address _receiver) public payable {
        require(msg.value > 0, "Transaction amount must be greater than 0");

        transactions.push(Transaction(msg.sender, _receiver, msg.value, block.timestamp));
        emit TransactionCreated(msg.sender, _receiver, msg.value, block.timestamp);
    }

    function getTransaction(uint index) public view returns (address, address, uint, uint) {
        require(index < transactions.length, "Invalid index");
        Transaction memory txn = transactions[index];
        return (txn.sender, txn.receiver, txn.amount, txn.timestamp);
    }

    function getTotalTransactions() public view returns (uint) {
        return transactions.length;
    }
}
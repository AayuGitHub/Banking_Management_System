from Account import Account
from Transaction import Transaction
from Transfer import Transfer
from datetime import date, datetime
import json
import os

class BankManager:
    
    def __init__(self):
        self.accounts = []
        self.transactions = []
        self.transfers = []
        self.TRANSACTIONS_FILENAME = "transactions.json"
        self.TRANSFERS_FILENAME = "transfers.json"
        self.ACCOUNTS_FILENAME = "accounts.json"
    
    def create_account(self, customerName, customerPhone, customerEmail, accountType, currentBalance):

        for account in self.accounts:
            if (customerName == account.customerName and customerPhone == account.customerPhone):
                return False
        
        newAccount = Account(customerName, customerPhone, customerEmail, accountType, currentBalance)
        newAccount.accountStatus = "Active"
        self.accounts.append(newAccount)
        return True

    def view_all_accounts(self):
        return sorted(self.accounts, key=lambda acc:acc.customerName)

    def search_account(self, customerName: str= None, accountId: str = None):
        for account in self.accounts:
            if customerName and customerName.lower() == account.customerName.lower():
                return account
            if accountId and accountId.lower() == account.accountId.lower():
                return account
        return None
    
    def update_account(self, updatedName: str = None, updatedPhone: str = None, updatedEmail: str = None, accountId: str = None):
        account = self.search_account(accountId=accountId)
        if account:
            if updatedName:
                account.customerName = updatedName
            if updatedPhone:
                account.customerPhone = updatedPhone
            if updatedEmail:
                account.customerEmail = updatedEmail
            return True
        return False
    
    def close_account(self, accountId: str):
        account = self.search_account(accountId=accountId)
        if account:
            if (account.currentBalance == 0 and account.accountStatus == "Active"):
                account.accountStatus = "Closed"
                return True
        return False
    
    def deposit_money(self, accountId: str, depositAmount: int):
        account = self.search_account(accountId=accountId)
        if account:
            if depositAmount > 0:
                account.currentBalance += depositAmount
                transaction = Transaction(
                    transactionType="Deposit",
                    transactionAmount=depositAmount,
                    transactionDateTime=datetime.now(),
                    transactionDescription="Cash Deposit",
                    accountId=accountId
                )
                self.transactions.append(transaction)
                return True
        return False
    
    def withdraw_money(self, accountId: str, withdrawAmount: int):
        account = self.search_account(accountId=accountId)
        if account:
            if withdrawAmount > 0:
                if account.currentBalance > withdrawAmount:
                    account.currentBalance -= withdrawAmount
                    transaction = Transaction(
                        transactionType="Withdraw",
                        transactionAmount=withdrawAmount,
                        transactionDateTime=datetime.now(),
                        transactionDescription="Cash WithDraw",
                        accountId=accountId
                    )
                    self.transactions.append(transaction)
                    return True
        return False
    
    def get_transactions(self, accountId: str):
        transactions = []
        for transaction in self.transactions:
            if transaction.accountId == accountId:
                transactions.append(transaction)
        if transactions:
            return transactions
        return []    

    
    def transfer_money(self, senderAccountId: str, receiveAccountId: str, transferAmount: int):
        senderAccount = self.search_account(accountId=senderAccountId)
        receiveAccount = self.search_account(accountId=receiveAccountId)

        if senderAccount and receiveAccount:
            if senderAccount.currentBalance > transferAmount:
                senderAccount.currentBalance -= transferAmount
                receiveAccount.currentBalance += transferAmount
                transferRecord = Transfer(
                    fromAccountId=senderAccountId,
                    toAccountId=receiveAccountId,
                    transferAmount=transferAmount,
                    transferDate=datetime.now(),
                )
                senderTransaction = Transaction(
                    transactionType="Withdraw",
                    transactionAmount=transferAmount,
                    transactionDateTime=datetime.now(),
                    transactionDescription="Cash WithDraw",
                    accountId=senderAccountId                
                )
                recieverTransaction = Transaction(
                    transactionType="Deposit",
                    transactionAmount=transferAmount,
                    transactionDateTime=datetime.now(),
                    transactionDescription="Cash Deposit",
                    accountId=receiveAccountId
                )
                self.transactions.append(senderTransaction)
                self.transactions.append(recieverTransaction)
                self.transfers.append(transferRecord)
                return True
        return False

    def transaction_history(self):
        return sorted(self.transactions, key=lambda tran:tran.transactionDateTime)

    def account_statement(self, accountId: str):
        account = self.search_account(accountId=accountId)
        if not account:
            return None

        transactions = self.get_transactions(accountId) or []   # guard None

        total_credits = sum(t.transactionAmount for t in transactions if t.transactionType == "Deposit")
        total_debits  = sum(t.transactionAmount for t in transactions if t.transactionType == "Withdraw")

        closing_balance = account.currentBalance
        opening_balance = account.currentBalance - total_credits + total_debits

        return {
            "customer":        account,
            "current_balance": account.currentBalance,
            "transactions":    transactions,
            "opening_balance": opening_balance,
            "closing_balance": closing_balance
        }

    def save_data(self):
        data_mapping = {
            self.TRANSACTIONS_FILENAME: self.transactions,
            self.TRANSFERS_FILENAME: self.transfers,
            self.ACCOUNTS_FILENAME: self.accounts
        }

        try:
            for filename, list_data in data_mapping.items():
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump([item.to_dict() for item in list_data], json_file, indent=4)
            print("\n[System] Data saved successfully to file.")
        except Exception as e:
            print(f"\n[System] Error saving data: {e}")
    
    def load_data(self):

        file_mapping = [
            (self.TRANSACTIONS_FILENAME, Transaction, self.transactions),
            (self.TRANSFERS_FILENAME, Transfer, self.transfers),
            (self.ACCOUNTS_FILENAME, Account, self.accounts)
        ]
    
        any_loaded = False
        for filename, cls, target_lists in file_mapping:
            if not os.path.exists(filename):
                continue
            try:
                with open(filename, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                for d in data:
                    target_lists.append(cls.from_dict(d))
                any_loaded = True
            except Exception as e:
                print(f"\n[System] Error loading {filename}: {e}")
        
        if any_loaded:
            print(f"\n[System] data loaded successfully from disk.")
        else:
            print("\n[System] No previous database found. Starting Fresh.")



        


                




    
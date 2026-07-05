from BankManager import BankManager

bankManager = BankManager()
bankManager.load_data()

while True:

    print("\n================================")
    print("\nBanking Management System")
    print("\n================================")
    print("\n1.  Create Account")
    print("\n2.  View All Accounts")
    print("\n3.  Search Account")
    print("\n4.  Update Account")
    print("\n5.  Close Account")
    print("\n6.  Deposit Money")
    print("\n7.  Withdraw Money")
    print("\n8.  Transfer Money")
    print("\n9.  View Transaction History")
    print("\n10. View Account Statement")
    print("\n11. Exit")

    choice = input("Select the operation (1-11): ")

    if choice == "1":

        customerName = ""
        customerPhone = ""
        customerEmail = ""
        accountType = ""
        currentBalance = 0

        print("\nEnter below customer details to create customer account: ")
        
        while customerName == "":
            customerName = input("\nPlease enter the name of customer: ").strip()

        while customerPhone == "":
            customerPhone = input("\nPlease enter the phone number of customer: ").strip()
        
        while customerEmail == "":
            customerEmail = input("\nPlease enter the email of customer: ").strip()
        
        while accountType == "":
            accountType = input("\nPlease enter the type of account (Saving/Current): ").strip()
        
        while True:
            try:
                currentBalance = int(input("\nPlease enter the initial deposit: "))
                if currentBalance > 0:
                    break
                print("Initial deposit must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")

        account = bankManager.create_account(
            customerName, customerPhone, customerEmail, accountType, currentBalance
        )

        if account:
            print(f"\nAccount created successfully for {customerName}!")
        else:
            print(f"\nAccount couldn't be created for {customerName}, please try again!")

    elif choice == "2":
        print("\nAll Accounts and thier details...")
        accounts = bankManager.view_all_accounts()
        if not accounts:
            print("\nNo accounts created yet, start creatinga accounts using option 1!")
        else:
            for account in accounts:
                print("\n------------------------------------")
                print(f"\nAccount ID: {account.accountId}")
                print(f"\nCustomer: {account.customerName}")
                print(f"\nPhone: {account.customerPhone}")
                print(f"\nType: {account.accountType}")
                print(f"\nBalance: {account.currentBalance}")
                print(f"\nStatus: {account.accountStatus}")
                print("\n------------------------------------")
    
    elif choice == "3":
        print("\nSearch customer by entering their customer ID or name...")
        customerName = input("Enter the name of customer for which you want to search account: ").strip()

        accountId = input("Enter the ID of customer for which you want to search account: ")

        searchAccount = bankManager.search_account(customerName, accountId)

        if not searchAccount:
            print(f"Account doesn't exist; please add it first using option 1!")
        else:
            print("\nSearched Account Details: ")
            print("\n------------------------------------")
            print(f"\nAccount ID: {searchAccount.accountId}")
            print(f"\nCustomer: {searchAccount.customerName}")
            print(f"\nPhone: {searchAccount.customerPhone}")
            print(f"\nType: {searchAccount.accountType}")
            print(f"\nBalance: {searchAccount.currentBalance}")
            print(f"\nStatus: {searchAccount.accountStatus}")
            print("\n------------------------------------")

    elif choice == "4":
        print("\nUpdate customer by entering their customer ID...")

        accountId = input("\nEnter the ID of customer for which you want to update account: ").strip()

        updatedName = input(f"\nEnter the updated name which you want to have for your account {accountId} (keep it blank to skip): ").strip()

        updatedPhone = input(f"\nEnter the updated phone which you want to have for your account {accountId} (keep it blank to skip): ").strip()

        updatedEmail = input(f"\nEnter the updated email which you want to have for your account {accountId} (keep it blank to skip): ").strip()

        updateAccount = bankManager.update_account(updatedName, updatedPhone, updatedEmail, accountId)

        if not updateAccount:
            print(f"\nAccount doesn't exist; please add it first using option 1!")
        else:
            print(f"\nAccount details updated for your account {accountId}!")
        
    elif choice == "5":

        accountId = input(f"\nPlease provide your account Id for closing account.. ").strip()

        closeAccount = bankManager.close_account(accountId)
        if closeAccount:
            print(f"\nYour account with ({accountId}) closed successfully!")
        else:
            print(f"\nYour account couldn't be closed; please ensure your current balance is 0 before trying to close.")
    
    elif choice == "6":

        accountId = input("\nPlease enter your account ID to deposit moeny in it: ").strip()

        depositAmount = int(input("\nPlease enter the amount you want to deposit in your account: "))

        deposit = bankManager.deposit_money(accountId, depositAmount)

        if deposit:
            print(f"\nAmount {depositAmount} deposited in your account {accountId}!")
        else:
            print(f"\nAmount {depositAmount} couldn't be deposited in your account {accountId}! Your account doesn't exist!")
    
    elif choice == "7":

        accountId = input("\nPlease enter your account ID to withdraw moeny in it: ").strip()

        withdrawAmount = int(input("\nPlease enter the amount you want to withdraw from your account: "))

        withdraw = bankManager.withdraw_money(accountId, withdrawAmount)

        if withdraw:
            print(f"\nAmount {withdrawAmount} withdrawn from your account {accountId}!")
        else:
            print(f"\nAmount {withdrawAmount} couldn't be withdrawn from your account {accountId}! Your account doesn't exist!")

    elif choice == "8":

        senderAccountId = input(f"\nPlease enter the account Id from whome you want to send money: ").strip()

        receiveAccountId = input(f"\nPlease enter the account Id to whome you want to send money: ").strip()

        transferAmount = int(input(f"\nPlease enter the amount you want to transfer: "))

        transferMoney = bankManager.transfer_money(
            senderAccountId, receiveAccountId, transferAmount
        )

        if transferMoney:
            print(f"Amount ({transferAmount}) has been transferred from accountID {senderAccountId} to accountID {receiveAccountId}!")
        else:
            print(f"Money couldn't be transfterred!")
        
    elif choice == "9":

        print(f"Displaying Transaction History...")
        transactionHistory = bankManager.transaction_history()

        if not transactionHistory:
            print("\nNo transaction history yet, start making transactions!")
        else:
            for transaction in transactionHistory:
                print("\n------------------------------------")
                print(f"\nTransaction ID: {transaction.transactionId}")
                print(f"\nAccount: {transaction.accountId}")
                print(f"\nType: {transaction.transactionType}")
                print(f"\nAmount: {transaction.transactionAmount}")
                print(f"\nDate: {transaction.transactionDateTime}")
                print(f"\nDescription: {transaction.transactionDescription}")
                print("\n------------------------------------")

    elif choice == "10":
        accountId = input("\nPlease enter account ID for which you want the statement: ").strip()
        while accountId == "":
            accountId = input("Account ID can't be empty; please enter account ID: ").strip()

        statement = bankManager.account_statement(accountId)

        if not statement:
            print(f"\nAccount ({accountId}) doesn't exist. Please create it first using option 1.")
        else:
            customerInfo = statement["customer"]
            transactions  = statement["transactions"]

            print("\n====================================")
            print("         ACCOUNT STATEMENT          ")
            print("====================================")

            print(f"\nAccount ID     : {customerInfo.accountId}")
            print(f"Customer       : {customerInfo.customerName}")
            print(f"Phone          : {customerInfo.customerPhone}")
            print(f"Account Type   : {customerInfo.accountType}")
            print(f"Status         : {customerInfo.accountStatus}")

            print(f"\nOpening Balance : ₹{statement['opening_balance']}")
            print(f"Closing Balance : ₹{statement['closing_balance']}")
            print(f"Current Balance : ₹{statement['current_balance']}")

            print("\n--- Transaction History ---")
            if not transactions:
                print("\nNo transactions found for this account.")
            else:
                for txn in transactions:
                    print("\n------------------------------------")
                    print(f"Transaction ID : {txn.transactionId}")
                    print(f"Type           : {txn.transactionType}")
                    print(f"Amount         : ₹{txn.transactionAmount}")
                    print(f"Date & Time    : {txn.transactionDateTime}")
                    print(f"Description    : {txn.transactionDescription}")
                    print("------------------------------------")

            print("\n====================================")
    
    elif choice == "11":
        print("\nSaving database records before shutdown...")
        bankManager.save_data()
        print("\nExiting program. good bye!")
        break
    else:
        print("Invalid option; please select a number from (1-11): ")

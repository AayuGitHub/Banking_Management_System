from datetime import date, datetime
import uuid

class Transaction:
    
    def __init__(self, transactionType: str, transactionAmount: int, transactionDateTime: datetime, transactionDescription: str, accountId: str = None, transactionId: str = None):
        self.transactionType = transactionType
        self.transactionAmount = transactionAmount
        self.transactionDateTime = transactionDateTime
        self.transactionDescription = transactionDescription
        self.accountId = accountId
        self.transactionId = transactionId if transactionId else str(uuid.uuid4())

    def __str__(self):
        return f"Transaction ID: {self.transactionId} | Account ID: {self.accountId} | Transaction Type: {self.transactionType} | Transaction Amount: {self.transactionAmount} | Transaction Date&Time: {self.transactionDateTime} | Transaction Description: {self.transactionDescription}"
    
    def display_transaction(self):
        print(self)
        
    def to_dict(self):
        return {
            "transactionId": self.transactionId,
            "accountId": self.accountId,
            "transactionType": self.transactionType,
            "transactionAmount": self.transactionAmount,
            "transactionDateTime": self.transactionDateTime.isoformat(),
            "transactionDescription": self.transactionDescription
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["transactionType"], data["transactionAmount"], datetime.fromisoformat(data["transactionDateTime"]), data["transactionDescription"], data["accountId"], data["transactionId"])
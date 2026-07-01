from datetime import date, datetime

class Transfer:

    def __init__(self, fromAccountId: str, toAccountId: str, transferAmount: int, transferDate: datetime, transferID: str):
        self.fromAccountId = fromAccountId
        self.toAccountId = toAccountId
        self.transferAmount = transferAmount
        self.transferDate = transferDate
        self.transferId = transferID
    
    def __str__(self):
        return f"Transfer ID: {self.transferId} | From Account ID: {self.fromAccountId} | To Account ID: {self.toAccountId} | Transfer Amount: {self.transferAmount} | Transfer Date: {self.transferDate}"
    
    def display_transfer_record(self):
        print(self)
    
    def to_dict(self):
        return {
            "transferId" : self.transferId,
            "fromAccountId": self.fromAccountId,
            "toAccountId": self.toAccountId,
            "transferAmount": self.transferAmount,
            "transferDate": self.transferDate
        }
    
    def from_dict(cls, data):
        return cls(data["fromAccountId"], data["toAccountId"], data["transferAmount"], data["transferDate"], data["transferID"])

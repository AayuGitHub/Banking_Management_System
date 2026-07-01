import uuid

class Account:

    def __init__(self, customerName: str, customerPhone: str, customerEmail: str, accountType: str, currentBalance: int, accountStatus: str = False, accountId: str = None):
        self.accountId = accountId if accountId else str(uuid.uuid4())
        self.customerName = customerName
        self.customerPhone = customerPhone
        self.customerEmail = customerEmail
        self.accountType = accountType
        self.currentBalance = currentBalance
        self.accountStatus = accountStatus

    def __str__(self):
        return f"Account ID: {self.accountId} | Customer Name: {self.customerName} | Customer Phone: {self.customerPhone} | Customer Email: {self.customerEmail} | Account Type: {self.accountType} | Current Balance: {self.currentBalance} | Account Status: {self.accountStatus} "
    
    def to_dict(self):
        return {
            "accountId": self.accountId,
            "customerName": self.customerName,
            "customerPhone": self.customerPhone,
            "customerEmail": self.customerEmail,
            "accountType": self.accountType,
            "currentBalance": self.currentBalance,
            "accountStatus": self.accountStatus
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["customerName"], data["customerPhone"], data["customerEmail"], data["accountType"], data["currentBalance"], data["accountStatus"], data["accountId"])
    
        
        

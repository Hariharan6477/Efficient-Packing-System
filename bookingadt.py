class Booking:
    def __init__(self,cust):
        self.cust=cust
        self.status="Not sent!"
    def changestatus(self):
        if self.status=="Not sent!":
            self.status="In progress!!"
        elif self.status=="In progress!!":
            self.status="Delivered"
    def getstatus(self):
        return self.status
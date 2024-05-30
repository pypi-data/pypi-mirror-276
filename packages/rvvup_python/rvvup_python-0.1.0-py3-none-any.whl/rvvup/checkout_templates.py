class CheckoutTemplates:

    def __init__(self, client):
        self.client = client

    def create(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def find(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

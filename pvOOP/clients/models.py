import uuid

class Client:
    def __init__(self, name, company, email, position, uid=None):
        self.name = name
        self.company = company
        self.email = email
        self.position = position
        self.uid = uid or uuid.uuid4()

    def to_dict(self):
        # Nos permite acceder a una representación como dict de nuestro objeto
        return vars(self) # cheque lo que rgresa el método __dict__

    @staticmethod
    def schema():
        return ['name', 'company', 'email', 'position', 'uid']
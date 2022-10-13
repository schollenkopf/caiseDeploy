
class Trie(object):
    def __init__(self):
        self.child = {"#": 0}

    def insert(self, operations, new_id):
        print("Operations", operations)
        current = self.child
        for operation in operations:
            if operation not in current:
                current[operation] = {"#": new_id}
                break
            current = current[operation]

    def search(self, operations):
        current = self.child
        for operation in operations:
            if operation not in current:
                return False
            current = current[operation]
        return current["#"]

    def startsWith(self, prefix):
        current = self.child
        for l in prefix:
            if l not in current:
                return False
            current = current[l]
        return True

    def __repr__(self) -> str:
        return str(self.child)

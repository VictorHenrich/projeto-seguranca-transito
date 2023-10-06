import bcrypt



class BCryptUtils:
    @classmethod
    def generate_hash(cls, data: str) -> str:
        data_in_bytes: bytes = data.encode("utf-8")

        new_hash: bytes = bcrypt.hashpw(data_in_bytes, bcrypt.gensalt())

        return new_hash.decode()
    
    @classmethod
    def compare_hash(cls, data: str, hash: str) -> bool:
        data_in_bytes: bytes = data.encode("utf-8")

        hash_in_bytes: bytes = hash.encode("utf-8")

        return bcrypt.checkpw(data_in_bytes, hash_in_bytes)


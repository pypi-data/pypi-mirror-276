import random


class Base62:
    BASE = 62
    CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encode(self, b: bytes) -> str:
        encoded: list[str] = []
        for byte in b:
            i = byte % self.BASE
            encoded.append(self.CHARSET[i])

        return "".join(reversed(encoded))


base62 = Base62()


def gen_id_suffix() -> str:
    b = random.randbytes(24)
    return base62.encode(b)


def gen_id(prefix: str, *, sep: str = "_") -> str:
    return prefix + sep + gen_id_suffix()

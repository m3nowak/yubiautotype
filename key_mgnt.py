import typing as ty

import gnupg

_GPG = gnupg.GPG()
_GPG.encoding = 'utf-8'


def available_pub_keys() -> ty.List[str]:
    return [ d['keyid'] for d in _GPG.list_keys()]


def encrypt(value: str, key: str) -> str:
    if key not in available_pub_keys():
        msg = 'Bad key id!'
        print(msg)
        raise ValueError(msg)
    encypted = _GPG.encrypt(value, key)
    return str(encypted)


def decrypt(value: str) -> str:
    return str(_GPG.decrypt(value))

import os
import typing as ty
import getpass

import models
import key_mgnt

_DEFAULT_FILENAME = ".yubiautotype.json"
_ENV_KEY_CFG_PATH = "YUBIAUTOTYPECFG"


def _default_path() -> str:
    fromenv = os.getenv(_ENV_KEY_CFG_PATH)
    if fromenv is None:
        return os.path.join(os.path.expanduser("~"), _DEFAULT_FILENAME)
    else:
        return fromenv


def _get_ucfg(path: ty.Optional[str] = None) -> models.UserConfig:
    if path is None:
        path = _default_path()
    return models.UserConfig.parse_file(path)


def _set_ucfg(ucfg: models.UserConfig, path: ty.Optional[str] = None):
    if path is None:
        path = _default_path()
    fle = open(path, 'w')
    fle.write(ucfg.json(indent=2))
    fle.close()


def create_config(keyid: str, overwrite: bool = False, path: ty.Optional[str] = None):
    if path is None:
        path = _default_path()
    if os.path.exists(path):
        if overwrite:
            msg = "Config already exists"
            print(msg)
            raise ValueError(msg)
        else:
            print("Overwriting config")
    if keyid not in key_mgnt.available_pub_keys():
        msg = "Unknown key"
        print(msg)
        raise ValueError(msg)
    ucfg = models.UserConfig(keyid=keyid, secrets={})
    _set_ucfg(ucfg, path)


def add_secret(label: str, value: ty.Optional[str] = None,  overwrite: bool = False, path: ty.Optional[str] = None):
    ucfg = _get_ucfg(path)
    if label in ucfg.secrets:
        if overwrite:
            print("Overwriting secret")
        else:
            msg = "Secret already exists"
            print(msg)
            raise ValueError(msg)

    if not value:
        value = getpass.getpass("Secret value (no-echo):")
    value = value.strip()
    if not value:
        msg = "Value cannot be empty"
        print(msg)
        raise ValueError(msg)
    ucfg.secrets[label] = key_mgnt.encrypt(value, ucfg.keyid)
    _set_ucfg(ucfg, path)


def read_secret(label: str, path: ty.Optional[str] = None) -> str:
    ucfg = _get_ucfg(path)
    if label not in ucfg.secrets:
        msg = "Secret does exist"
        print(msg)
        raise ValueError(msg)
    return key_mgnt.decrypt(ucfg.secrets[label])

import argparse

import config_mgnt
import windowselect

import time
import pyautogui


def create(args: argparse.Namespace):
    config_mgnt.create_config(args.key, args.force, args.config)


def add(args: argparse.Namespace):
    config_mgnt.add_secret(args.label, overwrite=args.force, path=args.config)


def type(args: argparse.Namespace):
    secret =config_mgnt.read_secret(args.label, args.config)
    time.sleep(args.delay)
    if args.window:
        windowselect.focus_window(args.window.strip())
    pyautogui.typewrite(secret)
    pyautogui.typewrite("\n")

def write(args: argparse.Namespace):
    secret =config_mgnt.read_secret(args.label, args.config)
    print(secret)


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='YubiAutoType',
        description='Perform autotype of secrets encryped by gpg',
        epilog='===')
    parser.add_argument('-c', '--config', help="Config file path")
    parser.add_argument('-f', '--force', action='store_true',
                        help="Force specified action")
    subparsers = parser.add_subparsers(help='Subcommands', required=True)

    sub_create = subparsers.add_parser('c', help='Create config file')
    sub_create.add_argument('key', help="Config key")
    sub_create.set_defaults(func=create)

    sub_add = subparsers.add_parser('a', help='Add secret to config')
    sub_add.add_argument('label', help="Secret label")
    sub_add.set_defaults(func=add)

    sub_type = subparsers.add_parser('t', help='Perform auto-type of a secret')
    sub_type.add_argument('label', help="Secret label")
    sub_type.add_argument('-w', '--window', help="Window title (part)")
    sub_type.add_argument('-d', '--delay', type=int,
                          help="Auto-type delay", default=0)
    sub_type.set_defaults(func=type)

    sub_write = subparsers.add_parser('w', help='Write secret to stdout')
    sub_write.add_argument('label', help="Secret label")
    sub_write.set_defaults(func=write)

    return parser

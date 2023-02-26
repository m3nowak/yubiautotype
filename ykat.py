import cli


def main():
    args = cli.parser().parse_args()
    args.func(args)
    


if __name__ == '__main__':
    main()

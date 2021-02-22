from discord_bot import discord_bot
from other import get_symbols


def main():
    try:
        symbols = get_symbols()
        discord_bot(symbols)
    except Exception as e:
        with open("main_error.log", "a") as fp:
            fp.write(repr(e))


if __name__ == '__main__':
    main()





# A very simple HTTP client

import argparse

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    r = requests.get(args.url)
    r.raise_for_status()

    print(r.text)


if __name__ == '__main__':
    main()

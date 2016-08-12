#!/usr/bin/env python3

import argparse


def parse_args():
    p = argparse.ArgumentParser(description='''
        A tool for measuring Python class cohesion.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    args = p.parse_args()

    return args


def main():
    args = parse_args()

    pass

if __name__ == "__main__":
    main()

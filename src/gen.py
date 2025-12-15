import argparse
from builder import build_site

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    build_site(args.output)
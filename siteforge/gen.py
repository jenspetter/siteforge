import argparse
from siteforge.builder import build_site

parser = argparse.ArgumentParser()
parser.add_argument('--content_path', type=str, required=True)
parser.add_argument('--build_registry_path', type=str, required=True)
parser.add_argument('--asset_registry_path', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    build_site(args.content_path, args.build_registry_path, args.asset_registry_path, args.output)
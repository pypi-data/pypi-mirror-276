import argparse


def cli():
    parser = argparse.ArgumentParser(description='Download and read weather forecast data from DWD')
    parser.add_argument("--lat", type=float, nargs="+", help="Latitude of the location(s)")
    parser.add_argument("--lon", type=float, nargs="+", help="Longitude of the location(s)")

    args = parser.parse_args()
    print("=== ===\t=== ===\t=== ===")
    print("=== ===\tDWD4Cast\t=== ===")
    print("=== ===\t=== ===\t=== ===")
    print(f"Latitude: {args.lat}")
    print(f"Longitude: {args.lon}")

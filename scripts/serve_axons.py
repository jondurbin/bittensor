import os
import argparse
import bittensor as bt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--wallet-path",
        type=str,
        default=os.path.expanduser("~/.bittensor/wallets"),
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default="wss://entrypoint-finney.opentensor.ai:443",
    )
    parser.add_argument(
        "--wallet-name",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--hotkeys",
        required=True,
        help="List of hotkeys to serve/advertise.",
        nargs="+",
    )
    parser.add_argument(
        "--ip",
        default=bt.utils.networking.get_external_ip(),
        help="IP address to serve the axon on.",
    )
    parser.add_argument(
        "--port",
        default=2000,
        help="Port to serve the axon on.",
    )
    parser.add_argument(
        "--netuid",
        required=True,
        type=int,
        help="Subnet to serve axon on.",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    bt.logging.info(f"Initializing subtensor with chain endpoint {args.endpoint}")
    subtensor = bt.subtensor(chain_endpoint=args.endpoint)
    ip = args.ip
    port = args.port
    for hotkey in args.hotkeys:
        bt.logging.info(f"Initializing wallet with {hotkey=}")
        wallet = bt.wallet(
            path=args.wallet_path,
            name=args.wallet_name,
            hotkey=hotkey
        )
        bt.logging.info(f"Serving axon {hotkey} on {ip}:{port}")
        success = subtensor.serve(
            wallet=wallet,
            ip=ip,
            port=port,
            netuid=args.netuid,
            protocol=4,
            wait_for_inclusion=True,
            wait_for_finalization=True,
        )
        if success:
            bt.logging.success(f"Successfully served axon {hotkey} on {ip}:{port}")

if __name__ == "__main__":
    main()

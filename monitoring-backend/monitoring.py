import argparse
import os

import uvicorn

VALID_LOG_LEVELS = ["INFO", "WARNING", "ERROR"]


def main():
    parser = argparse.ArgumentParser(description="Script that accepts four optional arguments.")
    parser.add_argument("--host", default="0.0.0.0", help="Application running host")
    parser.add_argument("--port", default="5487", help="Application running port")
    parser.add_argument("--refresh-hz", default="10", help="Refresh frequency in HZ")
    parser.add_argument("--log-level", default="INFO", help="Application log level")

    args = parser.parse_args()

    if not args.refresh_hz.isdigit():
        raise ValueError("Refresh frequency must be an integer.")

    if int(args.refresh_hz) <= 0:
        raise ValueError("Refresh frequency must be greater than 0.")

    if args.log_level not in VALID_LOG_LEVELS:
        raise ValueError(f"Provided LOG LEVEL does not exist. Choices are: {VALID_LOG_LEVELS}.")

    os.environ["REFRESH_FREQUENCY_HZ"] = str(args.refresh_hz)
    os.environ["LOG_LEVEL"] = args.log_level

    uvicorn.run("main:app", host=args.host, port=int(args.port))


if __name__ == "__main__":
    main()

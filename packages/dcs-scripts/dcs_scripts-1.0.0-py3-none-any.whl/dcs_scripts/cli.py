import argparse
from .utils import (
    read_yaml_file,
    submit_inference_tasks,
    generate_summarize_metrics_csv,
    submit_terminate_tasks,
)


def main():
    parser = argparse.ArgumentParser(
        description="Draycon Cell Segmentation (DCS) utility scripts"
    )
    subparsers = parser.add_subparsers(dest="command")

    inference_parser = subparsers.add_parser(
        "inference",
        help="Submit a series of inference jobs based on input config file.",
    )
    inference_parser.add_argument(
        "-c", "--config", required=True, help="Path to the configuration file"
    )

    terminate_parser = subparsers.add_parser(
        "terminate", help="Terminate active or running jobs based on input config file."
    )
    terminate_parser.add_argument(
        "-c", "--config", required=True, help="Path to the configuration file"
    )

    summary_metrics_parser = subparsers.add_parser(
        "summary_metrics",
        help="Create a summary_metrics.csv based on input config file.",
    )
    summary_metrics_parser.add_argument(
        "-c", "--config", required=True, help="Path to the configuration file"
    )

    args = parser.parse_args()

    if args.command == "inference":
        config = read_yaml_file(args.config)
        submit_inference_tasks(config=config)
    elif args.command == "terminate":
        config = read_yaml_file(args.config)
        submit_terminate_tasks(config=config)
    elif args.command == "summary_metrics":
        config = read_yaml_file(args.config)
        generate_summarize_metrics_csv(config=config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

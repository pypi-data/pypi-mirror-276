import argparse
import pandas as pd
from io import BytesIO
import yaml
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

ZERO_DAY_MIN_AREA = 2
CSV_COLUMNS = [
    "Study name",
    "Porcine ID",
    "Wound site location",
    "Days",
    "Product type",
    "Wounded area (cm^2)",
]


def read_yaml_file(yaml_path: str) -> dict:
    """Read yaml file as dictionary

    :param yaml_path: String for full path of yaml file
    :return: dictionary of parsed config yaml
    """
    with open(yaml_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


def preprocess_analysis_dataframe(input_df):
    df = input_df[input_df["valid_area"]].copy(deep=True)

    # Preprocess filename into specific columns
    df["Study name"] = df["filename"].str.split("_").str[0]
    df["Porcine ID"] = df["filename"].str.split("_").str[1]
    df["Wound site location"] = df["filename"].str.split("_").str[2]
    df["Days"] = df["filename"].str.split("_").str[3]
    df["Days"] = df["Days"].str[1:].astype(int)
    df["Product type"] = df["filename"].str.split("_").str[4]
    df = df.rename(columns={"wounded_area (cm^2)": "Wounded area (cm^2)"})

    # Filter out edge cases
    filter_mask = (df["Days"] == 0) & (df["Wounded area (cm^2)"] < ZERO_DAY_MIN_AREA)
    df = df[~filter_mask]
    df = df[CSV_COLUMNS]
    df = df.sort_values("Days")

    # Create baseline measurements for normalization
    df_deduped = df.drop_duplicates(
        ["Study name", "Porcine ID", "Wound site location", "Product type"],
        keep="first",
    )
    df_deduped = df_deduped.rename(
        columns={"Wounded area (cm^2)": "Wounded area baseline"}
    )
    _ = df_deduped.pop("Days")

    df = df.merge(
        df_deduped,
        on=["Study name", "Porcine ID", "Wound site location", "Product type"],
        how="inner",
    )
    df["Percent reduction\nfrom baseline"] = (
        100
        * (df["Wounded area (cm^2)"] - df["Wounded area baseline"])
        / df["Wounded area baseline"]
    )

    return df


def generate_wound_healing_plots(config_path: str) -> None:

    # Extract config parameters into dictionary
    config = read_yaml_file(config_path)

    # Authenticate key vault keys for Storage account and Batch API
    credential = AzureCliCredential()
    keyvault_secret_client = SecretClient(
        vault_url=config["key_vault_url"], credential=credential
    )
    storage_api_secret = keyvault_secret_client.get_secret(config["storage_secret"])
    print(storage_api_secret.name)
    print(storage_api_secret.value)
    print("")
    print("Key vault authenticated")

    # Connect to Storage account
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_api_secret.value
    )
    # load file from blob
    blob_name = f"{config['output_folder'] + 'morphometrics/study_summary_metrics.csv'}"
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_api_secret.value
    )
    container_client = blob_service_client.get_container_client(
        config["storage_container"]
    )
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()
    df = pd.read_csv(BytesIO(blob_data))

    df = preprocess_analysis_dataframe(input_df=df)

    # load to RAM, eg. jupyter notebook
    # df = pd.read_csv(blob_client.download_blob())

    # print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path to config file for submissions")
    parser.add_argument(
        "--yaml_file_path",
        "-c",
        help="Path to config file",
        type=str,
    )
    args = parser.parse_args()
    generate_wound_healing_plots(args.yaml_file_path)

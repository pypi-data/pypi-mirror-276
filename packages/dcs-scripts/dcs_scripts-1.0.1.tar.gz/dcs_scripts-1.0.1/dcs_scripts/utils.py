from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
import azure.batch._batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
from io import BytesIO
from itertools import compress
import pandas as pd
import uuid
import yaml


def read_yaml_file(yaml_path: str):
    """Read yaml file as dictionary

    :param yaml_path: String for full path of yaml file
    :return: dictionary of parsed config yaml
    """
    with open(yaml_path, "r") as stream:
        config = yaml.safe_load(stream)
    return config


def create_keyvault_client(config: dict):
    """Get the secret value for an input key_name string via Azure authentication

    :param config: configuration dictionary
    :return: Azure keyvault client object
    """

    # Authenticate key vault keys for Storage account and Batch API
    credential = AzureCliCredential()
    keyvault_secret_client = SecretClient(
        vault_url=config["key_vault_url"], credential=credential
    )
    print("\nKey vault authenticated.\n")
    return keyvault_secret_client


def submit_inference_tasks(config: dict):
    """Function to automatically scale inference jobs based on # of files in storage container

    :param config: configuration dictionary
    :return: None. Submits POST requests to Batch API for autoscaling jobs
    """

    # Define blobfuse mount directory
    storage_mount_dir = config["storage_container"].replace("-", "")

    # Get Azure API keys
    keyvault_secret_client = create_keyvault_client(config=config)
    storage_api_secret = keyvault_secret_client.get_secret(config["storage_secret"])
    batch_api_secret = keyvault_secret_client.get_secret(config["batch_account_secret"])

    # Connect to Storage account
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_api_secret.value
    )
    container_client = blob_service_client.get_container_client(
        config["storage_container"]
    )

    # Connect to Batch account
    batch_credentials = batchauth.SharedKeyCredentials(
        config["batch_account"], batch_api_secret.value
    )
    batch_client = batch.BatchServiceClient(
        batch_credentials, config["batch_account_url"]
    )

    # Recursively find the image file names in specified directory
    blob_list = container_client.list_blobs(
        name_starts_with=config["raw_inference_folder"]
    )
    raw_file_list = [blob.name.split("/")[-1] for blob in blob_list]
    extensionsToCheck = (".jpg", ".png", ".tif", ".JPG", ".PNG", ".TIF")
    image_file_list = [
        image_file
        for image_file in raw_file_list
        if image_file.endswith(extensionsToCheck)
    ]
    for image_file in image_file_list:
        assert " " not in image_file, (
            f"{image_file} has a space in the name. "
            f"Please remove any spaces in filenames in {config['storage_container']}/{config['raw_inference_folder']}"
        )

    print(
        f"\nIdentified {len(image_file_list)} images in {config['storage_container']}:{config['raw_inference_folder']}"
    )

    custom_container_settings = batchmodels.TaskContainerSettings(
        image_name=config["docker_image"],
        container_run_options="--privileged --cap-add=SYS_ADMIN -w /home/worker/",
    )

    # Recursively submit each inference job based for each individual image file
    for image_file in image_file_list:
        job_name_prefix = image_file.split(".")[0]
        command_line = (
            '/bin/bash -c "python3 scripts/predict.py'
            f' --raw_inference_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["raw_inference_folder"]}'
            f' --output_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["output_folder"]}'
            f" --filename {image_file}"
            f' --morphometrics {config.get("morphometrics")}'
            f' --model_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["model_folder"]}'
            f' --calibration_model_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["calibration_model_folder"]}'
            f' --calibration_diam_in_cm {config.get("calibration_diam_in_cm")}'
            f' --patch_size {config["patch_size"]}'
            f' --n_classes {config["n_classes"]}'
            f' --pixel_calibration {config.get("pixel_calibration")}'
            f' --rescaling_factor {config.get("rescaling_factor")};'
            " mkdir -p /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/;"
            'cp -R $AZ_BATCH_TASK_DIR/*.txt /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/"'
        )
        task = batchmodels.TaskAddParameter(
            id=f"{job_name_prefix}-{str(uuid.uuid4())}"[:64],
            command_line=command_line,
            container_settings=custom_container_settings,
        )

        batch_client.task.add(job_id=config["job_queue_name"], task=task)

    print(
        f"Submitted {len(image_file_list)} jobs on {config['batch_account']}:{config['job_queue_name']} queue"
    )


def generate_summarize_metrics_csv(config: dict) -> None:
    """Aggragate all relevent CSV in a given input Azure blob folder and generate the study summary metrics CSV

    :param config: configuration dictionary
    :return: None. Submits POST requests to Batch API for autoscaling jobs
    """

    # Authenticate key vault keys for Storage account API
    keyvault_secret_client = create_keyvault_client(config=config)
    storage_api_secret = keyvault_secret_client.get_secret(config["storage_secret"])

    # Connect to Storage account
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_api_secret.value
    )
    container_client = blob_service_client.get_container_client(
        config["storage_container"]
    )
    # Recursively find the image file names in specified directory
    blob_list = list(
        container_client.list_blobs(
            name_starts_with=config["output_folder"] + "morphometrics"
        )
    )

    # Exclude study summary CSV if it exists
    blob_list = [
        blob
        for blob in blob_list
        if "study_summary" not in blob.name and blob.name.endswith(".csv")
    ]
    if len(blob_list) == 0:
        raise ValueError(
            f"No CSVs in directory: {config['output_folder'] + 'morphometrics'}"
        )

    # Initialize an empty list to store the dataframes
    summary_metrics_df = pd.DataFrame()

    # Loop through the blobs and read CSV files
    print(
        f"Aggregating {len(blob_list)} CSVs into a single `study_summary_metrics` CSV."
    )
    for blob in blob_list:
        blob_client = container_client.get_blob_client(blob)
        blob_data = blob_client.download_blob().readall()
        df = pd.read_csv(BytesIO(blob_data))
        summary_metrics_df = pd.concat((summary_metrics_df, df), ignore_index=True)

    # Save the final dataframe to a CSV file
    output_file_name = (
        f"{config['output_folder'] + 'morphometrics/study_summary_metrics.csv'}"
    )
    print(
        f"Saving summary CSV to Azure storage: {config['storage_container']}/{output_file_name}"
    )
    output = BytesIO()
    summary_metrics_df.to_csv(output, index=False)
    output.seek(0)

    # Upload the CSV file to the same container
    blob_client = container_client.get_blob_client(output_file_name)
    blob_client.upload_blob(output, overwrite=True)


def submit_terminate_tasks(config: dict):
    """Function to automatically terminate all jobs that are NOT "Completed" stage

    :param config: configuration dictionary
    :return: None. Submits POST requests to Batch API
    """

    # Authenticate key vault keys for Batch account API
    keyvault_secret_client = create_keyvault_client(config=config)
    batch_api_secret = keyvault_secret_client.get_secret(config["batch_account_secret"])

    # Connect to Batch account
    batch_credentials = batchauth.SharedKeyCredentials(
        config["batch_account"], batch_api_secret.value
    )
    batch_client = batch.BatchServiceClient(
        batch_credentials, config["batch_account_url"]
    )

    # Find all task_ids that are NOT equal to "Completed". This should only return "Active" or "Running"
    task_filter = batchmodels.TaskListOptions(filter="state ne 'Completed'")
    task_list = [
        task.id
        for task in batch_client.task.list(
            job_id=config["job_queue_name"], task_list_options=task_filter
        )
    ]

    # Systematically terminate all tasks that are part of the filtered task list
    if len(task_list) < 1:
        print(
            f"No 'Active' or 'Running' tasks for termination in queue: "
            f"{config['batch_account']}:{config['job_queue_name']}"
        )
    else:
        print(
            f"Terminating tasks in {config['batch_account']}:{config['job_queue_name']} queue: "
        )
        for task_id in task_list:
            batch_client.task.delete(job_id=config["job_queue_name"], task_id=task_id)
            print(f"    Terminated {task_id}")


def submit_training_task(config: dict):
    """Function to automatically submit a single training job

    :param config: configuration dictionary
    :return: None. Submits POST requests to Batch API for autoscaling jobs
    """

    # Handle augmentation flags
    augment_keys = [f"--{key}" for key, _ in config.items() if "augment" in key]
    augment_values = [value for key, value in config.items() if "augment" in key]
    augment_params = " ".join(list(compress(augment_keys, augment_values)))

    # Handle encoder freezing and pretrained weights params
    freeze_encoder_param = "--freeze_encoder" if config.get("freeze_encoder") else ""
    pretrained_weights_param = (
        "--pretrained_weights" if config.get("pretrained_weights") else ""
    )
    # Define blobfuse mount directory
    storage_mount_dir = config["storage_container"].replace("-", "")

    # Determine if scoring params exist or not
    if all(
        [
            config.get("scoring_folder"),
            config.get("scoring_mask"),
            config.get("scoring_raw_file"),
        ]
    ):
        config["ground_truth_path"] = (
            f'/mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["scoring_folder"]}{config["scoring_mask"]}'  # noqa
        )
        config["ground_pred_path"] = (
            f'/mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["scoring_folder"]}{config["scoring_raw_file"]}'
        )
    else:
        config["ground_truth_path"] = None
        config["ground_pred_path"] = None

    # Get Azure API keys
    keyvault_secret_client = create_keyvault_client(config=config)
    batch_api_secret = keyvault_secret_client.get_secret(config["batch_account_secret"])

    # Connect to Batch account
    batch_credentials = batchauth.SharedKeyCredentials(
        config["batch_account"], batch_api_secret.value
    )
    batch_client = batch.BatchServiceClient(
        batch_credentials, config["batch_account_url"]
    )

    custom_container_settings = batchmodels.TaskContainerSettings(
        image_name=config["docker_image"],
        container_run_options="--privileged --cap-add=SYS_ADMIN -w /home/worker/",
    )

    # Define training job command for Batch syntax
    command_line = (
        '/bin/bash -c "python3 scripts/train.py'
        f' --train_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["train_folder"]}'
        f' --val_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["val_folder"]}'
        f' --model_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["model_folder"]}'
        f' --eval_ground_truth_file {config["ground_truth_path"]}'
        f' --eval_pred_file {config["ground_pred_path"]}'
        f' --patch_size {config["patch_size"]}'
        f' --n_classes {config["n_classes"]}'
        f' --thresholds {config["thresholds"]}'
        f' --pixel_calibration {config["pixel_calibration"]}'
        f' --rescaling_factor {config["rescaling_factor"]}'
        f' --epochs {config["epochs"]}'
        f' --learning_rate {config["learning_rate"]}'
        f' --batch_size {config["batch_size"]}'
        f" {augment_params}"
        f" {freeze_encoder_param}"
        f" {pretrained_weights_param}"
        f' --sm_backbone {config["sm_backbone"]}'
        f' --seed {config["seed"]};'
        " mkdir -p /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/;"
        'cp -R $AZ_BATCH_TASK_DIR/*.txt /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/"'
    )
    task = batchmodels.TaskAddParameter(
        id=f"{config['job_name_prefix']}-training-{str(uuid.uuid4())}",
        command_line=command_line,
        container_settings=custom_container_settings,
    )

    batch_client.task.add(job_id=config["job_queue_name"], task=task)

    print(
        f"Submitted training job on {config['batch_account']}:{config['job_queue_name']} queue"
    )


def submit_create_dataset_task(config: dict):
    """Function to automatically submit a single training job

    :param config: configuration dictionary
    :return: None. Submits POST requests to Batch API for autoscaling jobs
    """

    # Define blobfuse mount directory
    storage_mount_dir = config["storage_container"].replace("-", "")

    # Get Azure API keys
    keyvault_secret_client = create_keyvault_client(config=config)
    batch_api_secret = keyvault_secret_client.get_secret(config["batch_account_secret"])

    # Connect to Batch account
    batch_credentials = batchauth.SharedKeyCredentials(
        config["batch_account"], batch_api_secret.value
    )
    batch_client = batch.BatchServiceClient(
        batch_credentials, config["batch_account_url"]
    )

    custom_container_settings = batchmodels.TaskContainerSettings(
        image_name=config["docker_image"],
        container_run_options="--privileged --cap-add=SYS_ADMIN -w /home/worker/",
    )

    # Define training job command for Batch syntax
    command_line = (
        '/bin/bash -c "python3 scripts/generate_dataset.py'
        f' --raw_train_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["raw_train_folder"]}'
        f' --raw_val_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["raw_val_folder"]}'
        f' --train_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["train_folder"]}'
        f' --val_folder /mnt/batch/tasks/shared/{storage_mount_dir}/{config["project_folder"]}{config["val_folder"]}'
        f' --patch_size {config["patch_size"]}'
        f' --pixel_calibration {config["pixel_calibration"]}'
        f' --thresholds {config["thresholds"]}'
        f' --n_classes {config["n_classes"]}'
        f' --rescaling_factor {config["rescaling_factor"]}'
        f' --seed {config["seed"]};'
        " mkdir -p /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/;"
        'cp -R $AZ_BATCH_TASK_DIR/*.txt /mnt/batch/tasks/shared/logs/$AZ_BATCH_TASK_ID/\\$TaskLog/"'
    )
    task = batchmodels.TaskAddParameter(
        id=f"{config['job_name_prefix']}-dataset-{str(uuid.uuid4())}",
        command_line=command_line,
        container_settings=custom_container_settings,
    )

    batch_client.task.add(job_id=config["job_queue_name"], task=task)

    print(
        f"Submitted dataset creation job on {config['batch_account']}:{config['job_queue_name']} queue"
    )

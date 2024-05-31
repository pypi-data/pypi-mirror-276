import base64
import json
import os
import re
import pkg_resources

from functools import wraps

from py4j.java_gateway import java_import

from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.config.constants import DEPOT_SECRETS_KV_REGEX, DATAOS_DEFAULT_SECRET_DIRECTORY, S3_ACCESS_KEY_ID, \
    S3_ACCESS_SECRET_KEY, S3_SPARK_CONFS, GCS_AUTH_ACCOUNT_ENABLED, GCS_ACCOUNT_EMAIL, GCS_PROJECT_ID, \
    GCS_ACCOUNT_PRIVATE_KEY, GCS_ACCOUNT_PRIVATE_KEY_ID, AZURE_ACCOUNT_KEY_PREFIX, AZURE_ACCOUNT_KEY, \
    DATAOS_ADDRESS_RESOLVER_REGEX

# import builtins
#
#
# def my_print(*args, **kwargs):
#     # Do something with the arguments
#     # Replace sensitive strings with a placeholder value
#     redacted_text = re.sub('(?i)secret|password|key|abfss|dfs|apikey', '*****', " ".join(str(arg) for arg in args))
#     # Print the redacted text
#     builtins.print(redacted_text)
from pyflare.sdk.utils.pyflare_exceptions import MissingEnvironmentVariable


def decorate_logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = pyflare_logger.get_pyflare_logger(name=__name__)
        log.debug('About to run %s' % fn.__name__)

        out = fn(*args, **kwargs)

        log.debug('Done running %s' % fn.__name__)
        return out

    return wrapper


def append_properties(dict1: dict, dict2: dict) -> dict:
    for key, value in dict2.items():
        dict1[key] = value
    return dict1


def safe_assignment(val1, val2):
    """
    Returns val1 if val2 is None, else return val2
    """
    if val2:
        return val2
    return val1


def get_jars_path():
    flare_sdk_jar_path = pkg_resources.resource_filename('pyflare.jars', 'flare_2.12-3.3.1-0.0.14.1-javadoc.jar')
    heimdall_jar_path = pkg_resources.resource_filename('pyflare.jars', 'heimdall-0.1.9.jar')
    commons_jar_path = pkg_resources.resource_filename('pyflare.jars', 'commons-0.1.9.jar')
    spark_jar_path = pkg_resources.resource_filename('pyflare.jars', 'spark-authz-0.1.9.jar')
    josn4s_jar_path = pkg_resources.resource_filename('pyflare.jars', 'json4s-jackson_2.12-3.6.12.jar')
    josn4s_jar_path = pkg_resources.resource_filename('pyflare.jars', 'json4s-jackson_2.12-4.0.6.jar')
    flare_jar_path = pkg_resources.resource_filename('pyflare.jars', 'flare_4.jar')
    return f"{commons_jar_path},{heimdall_jar_path}, {flare_sdk_jar_path}, {josn4s_jar_path}, {spark_jar_path}"


def get_abfss_spark_conf(rw_config: ReadConfig):
    dataset_absolute_path = rw_config.dataset_absolute_path()
    dataset_auth_token = get_secret_token(rw_config.depot_details)
    account = rw_config.depot_details.get("connection", {}).get("account", "")
    endpoint_suffix = dataset_absolute_path.split(account)[1].split("/")[0].strip(". ")
    dataset_auth_key = "{}.{}.{}".format(AZURE_ACCOUNT_KEY_PREFIX, account, endpoint_suffix)
    return [(dataset_auth_key, dataset_auth_token)]


def get_s3_spark_conf(rw_config: ReadConfig):
    access_key_id = rw_config.depot_details.get("secrets", {}).get("accesskeyid", "")
    access_key_secret = rw_config.depot_details.get("secrets", {}).get("awssecretaccesskey", "")
    aws_access_key_id = (S3_ACCESS_KEY_ID, access_key_id)
    aws_access_key_secret = (S3_ACCESS_SECRET_KEY, access_key_secret)
    spark_conf = [aws_access_key_id, aws_access_key_secret]
    spark_conf.extend(S3_SPARK_CONFS)
    return spark_conf


def get_gcs_spark_conf(rw_config: ReadConfig):
    client_email = rw_config.depot_details.get("secrets", {}).get("client_email", "")
    project_id = rw_config.depot_details.get("secrets", {}).get("project_id", "")
    private_key = rw_config.depot_details.get("secrets", {}).get("private_key", "")
    private_key_id = rw_config.depot_details.get("secrets", {}).get("private_key_id", "")
    private_key_file_path = rw_config.depot_details.get("secrets", {}).get(
        f"{rw_config.depot_name()}_secrets_file_path", "")
    return [
        # ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/etc/dataos/secret/depot.*.json"),
        (GCS_AUTH_ACCOUNT_ENABLED, "true"),
        (GCS_ACCOUNT_EMAIL, client_email),
        (GCS_PROJECT_ID, project_id),
        (GCS_ACCOUNT_PRIVATE_KEY, private_key_file_path),
        (GCS_ACCOUNT_PRIVATE_KEY_ID, private_key_id),
    ]


def get_secret_token(depot_details) -> str:
    return depot_details.get("secrets", {}).get(AZURE_ACCOUNT_KEY, "")


def get_dataset_path(depot_config) -> str:
    return "{}.{}.{}".format(depot_config.depot_name(), depot_config.collection(),
                             depot_config.dataset_name())


def encode_base64_string(json_string: str) -> str:
    encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def decode_base64_string(encoded_string: str, type: str) -> dict:
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    if type.casefold() == "json":
        key_value_pairs = json.loads(decoded_string)
    else:
        key_value_pairs = re.findall(DEPOT_SECRETS_KV_REGEX, decoded_string)
    return dict(key_value_pairs)


def get_secret_file_path() -> str:
    return DATAOS_DEFAULT_SECRET_DIRECTORY if os.getenv("DATAOS_SECRET_DIR") is None else \
        os.getenv("DATAOS_SECRET_DIR").rstrip('/')


def write_string_to_file(file_path: str, string_data: str, overwrite: bool = True) -> None:
    log = pyflare_logger.get_pyflare_logger()
    if not overwrite and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        log.info("File exists and is not empty")
    else:
        log.info("Creating file at path: %s", file_path)
        try:
            with open(file_path, "w") as file:
                file.write(string_data)
            log.info(f"Data written successfully to: {file_path}")
        except Exception as e:
            log.error(f"Error writing data to the file: {str(e)}")


def write_dict_to_file(file_path: str, data_dict: dict, overwrite: bool = True) -> None:
    log = pyflare_logger.get_pyflare_logger()
    if not overwrite and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        log.info("File exists and is not empty")
    else:
        log.info("Creating file at path: %s", file_path)
        try:
            with open(file_path, "w") as file:
                json.dump(data_dict, file)
            log.info(f"Dictionary Data written successfully to: {file_path}")
        except Exception as e:
            log.error(f"Error writing data dictionary to the file: {str(e)}")


def resolve_dataos_address(dataos_address: str) -> dict:
    matches = re.match(DATAOS_ADDRESS_RESOLVER_REGEX, dataos_address)
    parsed_address = {}
    if matches:
        parsed_address["depot"] = matches.groups()[0]
        parsed_address["collection"] = matches.groups()[2]
        parsed_address["dataset"] = matches.groups()[4]
    return parsed_address


def get_env_variable(env_variable: str) -> str:
    value = os.environ.get(env_variable, "")
    if len(value) < 1:
        raise MissingEnvironmentVariable(f"{env_variable} is not set")
    return value


def enhance_connection_url(connection_url: str, collection: str, dataset: str) -> str:
    if collection and collection.casefold() != "none":
        connection_url += f"/{collection}"
    if dataset:
        connection_url += f"/{dataset}"
    return connection_url


def authorize_user(spark, heimdallClient, apikey):
    log = pyflare_logger.get_pyflare_logger()
    response = heimdallClient.getAuthorizeApi().authorize(apikey).execute()
    if response.isSuccessful():
        json_response = response.body()
        user_id = json_response.getResult().getId()
        return user_id
    else:
        log.error(f"Error: {response.code()}, {response.message()}")
        return None

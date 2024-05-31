import re

import requests
from pyflare.sdk.config import constants
from pyflare.sdk import pyflare_logger
from pyflare.sdk.config.constants import DEPOT_NAME_JSON_FILE_REGEX
from pyflare.sdk.utils.generic_utils import decode_base64_string, write_dict_to_file, get_secret_file_path


class DepotClientAPI:

    def __init__(self, api_token: str):
        self.api_token: str = api_token
        self.log = pyflare_logger.get_pyflare_logger(__name__)

    def get_depot_details(self, depot_name: str, acl: str = "r", with_secrets: bool = True) -> dict:
        depot_metadata = self.__get_depot_metadata(depot_name)
        depot_name = depot_metadata.get("depot", "")

        if with_secrets:
            depot_metadata["secrets"] = self.__get_depot_secrets(depot_name, acl)
        return depot_metadata

    def __get_depot_metadata(self, depot_name: str):
        url, headers = self.__get_depot_metadata_url_and_headers(depot_name)
        response = requests.request(constants.HTTP_GET, url=url, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Something went wrong in depot metadata API for depot: {depot_name} "
                                                f"with status code: {response.status_code}")
        data = response.json()
        self.log.info(f"data: {data}, status: {response.status_code}")
        return data

    def __get_depot_secrets(self, depot_name: str, acl: str):
        url, headers = self.__get_depot_secrets_url_and_headers(depot_name, acl)
        response = requests.request(constants.HTTP_GET, url=url, headers=headers)
        data = {}
        if response.status_code != 200 and response.status_code != 404:
            raise requests.exceptions.HTTPError(f"Something went wrong in depot secrets API for depot: {depot_name} "
                                                f"with status code: {response.status_code}")
        elif response.status_code == 200:
            data = response.json()
        self.log.info(f"Secrets API status: {response.status_code}")
        if data and data.get('data'):
            data = self.__extract_secret(depot_name, data.get('data'), acl)
        return data

    def __get_depot_metadata_url_and_headers(self, depot_name: str):
        url = constants.DEPOT_RESOLVE_ENDPOINT_CUSTOM.format(constants.HTTP_PROTOCOL, constants.DATAOS_BASE_URL,
                                                             depot_name)
        headers = {constants.DEPOT_METADETA_HEADER_KEY: self.api_token}
        return url, headers

    def __get_depot_secrets_url_and_headers(self, depot_name: str, acl: str):
        url = constants.DEPOT_SECRETS_ENDPOINT.format(constants.HTTP_PROTOCOL, constants.DATAOS_BASE_URL,
                                                      depot_name, acl)
        headers = {constants.DEPOT_METADETA_HEADER_KEY: self.api_token}
        return url, headers

    def __extract_secret(self, depot_name, secrets_list, acl: str):
        decoded_secrets = {}
        if len(secrets_list) == 1:
            decoded_secrets = decode_base64_string(secrets_list[0].get("base64Value", {}), "kv")
        else:
            secrets_dict = {item["key"]: item for item in secrets_list}
            inner_dict = decode_base64_string(secrets_dict.get(f"{depot_name}-{acl}", {}).get("base64Value", {}), "kv")
            result_value = next((secrets_dict[key] for key in secrets_dict if key in inner_dict.values()), None)
            encoded_secrets = result_value.get("base64Value", {})
            decoded_secrets = decode_base64_string(encoded_secrets, "json")
            secrets_file_path = f"{get_secret_file_path()}/{result_value.get('key', {})}"
            write_dict_to_file(secrets_file_path, decoded_secrets)
            decoded_secrets[f"{depot_name}_secrets_file_path"] = secrets_file_path
        return decoded_secrets

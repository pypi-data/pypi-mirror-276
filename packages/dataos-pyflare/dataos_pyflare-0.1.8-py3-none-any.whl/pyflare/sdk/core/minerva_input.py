# from __future__ import annotations
from pyflare.sdk import pyflare_logger
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.depots import client
from pyflare.sdk.readers.minerva_reader import MinervaInputReader
from pyflare.sdk.readers.reader import Reader
from pyflare.sdk.utils.generic_utils import safe_assignment, resolve_dataos_address, append_properties
from pyspark.sql import SparkSession, DataFrame

from pyflare.sdk.utils.pyflare_exceptions import InvalidInputException, PyflareReadException


class MinervaInput:
    def __init__(self, name, parsed_inputs, spark, apikey, cluster_name,
                 source_format="jdbc", driver="io.trino.jdbc.TrinoDriver", query=None, options=None):
        self.input_name: str = name
        self.parsed_inputs: dict[str: Reader] = parsed_inputs
        self.spark: SparkSession = spark
        self.api_token = apikey
        self.source_format: str = source_format
        self.driver = driver
        self.query = query
        self.cluster_name = cluster_name
        self.options: dict = options if options else {}

    def process_inputs(self) -> DataFrame:
        """

        Run query on minerva and the result is stored as a temp view
        with the name passed in the dataos_source decorator.
        """
        try:
            log = pyflare_logger.get_pyflare_logger(name=__name__)
            log.debug(f"minerva_read_input, input: {self.parsed_inputs}")
            resolved_address = resolve_dataos_address(self.input_name)

            if not self.parsed_inputs.get(resolved_address.get("depot", "")):
                raise InvalidInputException(f"Depot not loaded in current session: {self.input_name}")
            reader_instance: Reader = self.parsed_inputs.get(resolved_address.get("depot", "")).get('reader_instance')
            read_conf: ReadConfig = reader_instance.read_config
            read_conf.io_format = safe_assignment(read_conf.io_format, self.source_format)
            fresh_depot_details = client.DepotClientAPI(self.api_token).get_depot_details(self.input_name, "r", False)
            fresh_depot_details["secrets"] = read_conf.depot_details.get("secrets")
            read_conf.depot_details = fresh_depot_details
            minerva_reader: MinervaInputReader = MinervaInputReader(reader_instance.read_config)
            minerva_reader.read_config.driver = self.driver
            minerva_reader.read_config.query = self.query
            minerva_reader.read_config.cluster_name = self.cluster_name
            minerva_reader.spark = safe_assignment(minerva_reader.spark, self.spark)
            minerva_reader.read_config.io_format = safe_assignment(minerva_reader.read_config.io_format,
                                                                   self.source_format)
            minerva_reader.read_config.extra_options = append_properties(minerva_reader.read_config.extra_options,
                                                                         self.options.pop(
                                                                             minerva_reader.read_config.io_format, {}))
            minerva_reader.read_config.spark_options = safe_assignment(minerva_reader.read_config.spark_options,
                                                                       self.options)
            df = minerva_reader.read()
            # df.createOrReplaceTempView(self.input_name)
            return df, resolved_address.get("depot", "")
        except AttributeError as e:
            raise InvalidInputException(
                f"Check if read format {self.source_format} is valid for depot {self.input_name}. Msg: {str(e)}")
        except Exception as e:
            raise PyflareReadException(
                f"Check if dataset {self.input_name} exists and you have read access. Msg: {str(e)}")

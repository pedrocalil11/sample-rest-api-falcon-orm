import os
from constants              import ENV_VARS
from jsonschema             import Draft7Validator
from json                   import JSONDecodeError
import json
import logging

class SchemaCache:
    schemas = {}
    @staticmethod
    def getSchema(schema_file_name):
        logger = logging.getLogger(__name__)
        schema_path = ENV_VARS['SERVICE_ROOT'] + "/schemas/" + schema_file_name
        
        if schema_path in SchemaCache.schemas:
            logger.info("JsonSchema retrieved from cache: " + schema_path)
            return SchemaCache.schemas[schema_path]

        if not os.path.isfile(schema_path):
            logger.fatal('JsonSchema file "' + schema_path + '" not found.')
            raise Exception('Internal Error', 'There was an internal error loading JSON Schema - ' + schema_file_name)
        
        try:
            SchemaCache.schemas[schema_path] = json.loads(open(schema_path, "r").read())
            logger.info("JsonSchema retrieved from file: " + schema_path)
            return SchemaCache.schemas[schema_path]
            
        except JSONDecodeError:
            logging.fatal('Schema file "' + schema_path + '" is not a valid JSON file')
            raise Exception('Internal Error', 'There was an internal error validating JSON Schema')
        except IOError:
            logging.fatal('Schema file "' + schema_path + '" is not accessible')
            raise Exception('Internal Error', 'There was an internal error validating JSON Schema')

        return SchemaCache.schemas[schema_path]
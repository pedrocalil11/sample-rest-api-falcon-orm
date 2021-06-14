import os
import logging
ENV_VARS_NAMES = {
    'APP_ENV': {
        'type': 'string',
        'required': True
    },
    'DB_HOSTNAME': {
        'type': 'string',
        'required': True
    },
    'DB_PORT': {
        'type': 'integer',
        'required': True
    },
    'DB_USERNAME': {
        'type': 'string',
        'required': True
    },
    'DB_PASSWORD': {
        'type': 'string',
        'required': True
    },
    'DB_NAME': {
        'type': 'string',
        'required': True
    },
    'AWS_DEFAULT_REGION': {
        'type': 'string',
        'required': True
    },
    'MASTER_ADMIN_KEY': {
        'type': 'string',
        'required': True
    },
}

ENV_VARS = dict()
for var_name in ENV_VARS_NAMES:
    if ENV_VARS_NAMES[var_name].get('required', True) and os.environ.get(var_name) is None:
        raise Exception('Environment Variable "' + var_name + '" not found')

    if os.environ.get(var_name) is None and 'default' in ENV_VARS_NAMES[var_name]:
        default_value = ENV_VARS_NAMES[var_name].get('default')
        logging.getLogger(__name__).info(('Loading Environment Var: "'
                                                + var_name + '" with default value: "'
                                                + default_value + '"'))
        ENV_VARS[var_name] = default_value

    if os.environ.get(var_name) is not None:
        value = os.environ.get(var_name)
        logging.getLogger(__name__).info(('Loading Environment Var: "'
                                                + var_name + '" with value: "'
                                                + value + '"'))
        ENV_VARS[var_name] = value

ENV_VARS['GIT_COMMIT'] = "$$GIT_COMMIT"
ENV_VARS['GIT_BRANCH'] = "$$GIT_BRANCH"
ENV_VARS['SERVICE_ROOT'] = os.path.abspath(os.path.dirname(__file__))
ENV_VARS['SCHEMA_PATH'] = os.path.join(ENV_VARS['SERVICE_ROOT'] + "/schemas/")

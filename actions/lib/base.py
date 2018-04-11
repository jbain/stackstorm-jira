from jira import JIRA

#  from st2common.runners.base_action import Action
__all__ = [
    'BaseJiraAction'
]


class Action(object):
    def __init__(self, config):
        self.config = config


class BaseJiraAction(Action):
    def __init__(self, config):
        super(BaseJiraAction, self).__init__(config=config)
        self._client = self._get_client()

    def _get_client(self):
        config = self.config

        options = {'server': config['url'], 'verify': config['verify']}

        rsa_cert_file = config['rsa_cert_file']
        rsa_key_content = self._get_file_content(file_path=rsa_cert_file)

        oauth_creds = {
            'access_token': config['oauth_token'],
            'access_token_secret': config['oauth_secret'],
            'consumer_key': config['consumer_key'],
            'key_cert': rsa_key_content
        }

        if config['basic_auth']:
            client = JIRA(options=options, basic_auth=(config['basic_auth_username'],
                                                       config['basic_auth_password']))
            return client

        client = JIRA(options=options, oauth=oauth_creds)
        return client

    def _get_file_content(self, file_path):
        with open(file_path, 'r') as fp:
            content = fp.read()

        return content

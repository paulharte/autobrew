



class AwsConfig(object):
    BASE_URLS = {'uat': 'https://brew-uat.paulspetprojects.net/', 'prod': 'https://brew.paulspetprojects.net/'}

    TOKEN_ENDPOINTS = {'uat': 'https://autobrew-uat.auth.eu-west-1.amazoncognito.com/token',
                       'prod': 'https://autobrew-prod.auth.eu-west-1.amazoncognito.com/token'}


    def __init__(self, env: str):
        self.env = env

    def get_base_url(self):
        return self.BASE_URLS[self.env]

    def get_token_endpoint(self):
        return self.TOKEN_ENDPOINTS[self.env]


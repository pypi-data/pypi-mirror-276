# -*- coding: utf-8 -*-

"""
Cherwell API Client Class
"""

import inspect
import os


class CherwellAPIClientError(Exception):
    pass


class CherwellAPIClientAuthenticationError(Exception):
    pass


def strtobool(_string):
    """Converts a string to a boolean, replaces distutils.utils.strtobool (deprecated per PEP 632)"""
    if _string in ['y', 'yes', 't', 'true', 'on', '1', 1]:
        return True
    elif _string in ['n', 'no', 'f', 'false', 'off', '0', 0]:
        return False
    else:
        raise CherwellAPIClientError(f"Invalid boolean value: {_string}")


class Client(object):
    """Client class to access the Cherwell API"""

    def __init__(self, host=None, user=None, password=None, client_id=None, ssl_verify=None):
        """
        Create the client object to communicate with Cherwell. The authentication
        and ssl parameters can be pulled from the environment so that they
        don't have to be passed in from code or command line args.

        Arguments:
            host (str): FQDN used to access the cherwell server
            user (str): Cherwell username
            password (str): Cherwell user's password
            client_id (str): API client ID
            ssl_verify (bool): Whether to verify the SSL certificate or not.
                Set to false when using servers with self-signed certs.
        """
        if not host:
            if 'CHERWELL_HOST' in os.environ:
                host = os.environ['CHERWELL_HOST']

        if not user:
            if 'CHERWELL_USER' in os.environ:
                user = os.environ['CHERWELL_USER']

        if not password:
            if 'CHERWELL_PASSWD' in os.environ:
                password = os.environ['CHERWELL_PASSWD']

        if not client_id:
            if 'CHERWELL_CLIENT_ID' in os.environ:
                client_id = os.environ['CHERWELL_CLIENT_ID']

        if ssl_verify is None:
            if 'CHERWELL_SSL_VERIFY' in os.environ:
                ssl_verify = os.environ['CHERWELL_SSL_VERIFY']
            else:
                ssl_verify = True

        if isinstance(ssl_verify, str):
            ssl_verify = bool(strtobool(ssl_verify))

        self.api_url = host
        self.ssl_verify = ssl_verify
        self.api_headers = {"Content-Type": "application/json"}
        self.routers = dict()
        self.api_user = user
        self.api_password = password
        self.api_client_id = client_id

        for router in self.get_routers():
            self.routers[router] = __import__(
                'cherwellapi.routers.{0}'.format(router),
                fromlist=[router])

    def get_routers(self):
        """
        Gets the list of availble Cherwell API routers

        Returns:
            list:
        """
        router_list = []
        routers_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'routers')
        file_list = os.listdir(routers_path)
        file_list = [filename for filename in file_list if '.py' in filename]
        for fname in file_list:
            name, ext = fname.split('.')
            if name == "__init__":
                continue
            if ext == "py":
                router_list.append(name)

        return router_list

    def get_router(self, router):
        """
        Instantiates and returns a Cherwell router object

        Arguments:
            router (str): The API router to use
        """
        router_class = getattr(
            self.routers[router],
            '__router__',
            '{0}Router'.format(router.capitalize())
        )

        api_router = getattr(
            self.routers[router],
            router_class,
        )(
            self.api_url,
            self.api_headers,
            self.api_user,
            self.api_password,
            self.api_client_id,
            self.ssl_verify
        )
        return api_router

    def get_router_methods(self, router):
        """
        List all available methods for an API router

        Arguments:
            router (str): The router to get methods from

        Returns:
            list:
        """
        router_methods = []
        router_class = getattr(
            self.routers[router],
            '__router__',
            '{0}Router'.format(router.capitalize())
        )

        for method in inspect.getmembers(
                getattr(self.routers[router],
                        router_class),
                predicate=inspect.isroutine
        ):
            if method[0].startswith('__'):
                continue
            router_methods.append(method[0])

        return router_methods

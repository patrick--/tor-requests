import json
import socket
import requests
import socks
import stem.process

SOCKS_PORT = 7000

class TorRequests(object):
    """
    Class used to issue HTTP requests through a Tor Proxy

    Args:
        socks_port(int,optional):
            SOCKS port proxy is running on, defaults to 7000

        exit_nodes(string,optional):
         Sets exit node for certain country using ISO 3166-1 format, defaults to russia
         see: http://en.wikipedia.org/wiki/ISO_3166-1
    """

    def __init__(self, socks_port=7000, exit_nodes='{ru}'):
        self.socks_port = socks_port
        self.exit_nodes = exit_nodes
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', self.socks_port)
        socket.socket = socks.socksocket

        self.tor_process = stem.process.launch_tor_with_config(
        config = {
            'SocksPort': str(self.socks_port),
            'ExitNodes': self.exit_nodes,
          },
        )


    def post(self,url,data, content_type="application/json"):
        """
        Method for POSTing data to an endpoint

        Args:
            url(string):
                URL endpoint that data will be posted to

            data(dictionary):
                Requests style dictionary with POST payload data

            content_type(string,optional):
                Sets content header for request, defaults to json


        Returns:
            Response object if successful otherwise None
        """
        try:
            headers = {'content-type': content_type}
            response = requests.post(url,data=json.dumps(data),headers=headers)
        except requests.exception.RequestException:
            response = None
        return response


    def get(self,url):
        """
        Method for GETing data from an endpoint

        Args:
            url(string):
                Endpoint to request data from

        Returns:
            Response object if successful otherwise None
        """
        try:
            response = requests.get(url,verify=False)
        except:
            response = None
        return response


    def exit(self):
        """
        Method that exits Tor process

        """
        self.tor_process.kill()

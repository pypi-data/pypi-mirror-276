"""Pretty simple Python module that makes interacting with a Pufferpanel Server Daemon easy."""

import requests
import json
from time import time, sleep


class ServerError(Exception):
    pass


class Panel:
    """
    A Panel object must get assigned 3 values: serverURL, clientID, and clientSecret.
    These can be obtained by creating an oauth2 client in PufferPanel.

    The user can also (optionally) define serverID, which is useful if the scope of your token doesn't cover multiple servers.
    When serverID is defined, the serverID parameter can be skipped in methods where it is required, so

    object.logs('a1b236')

    becomes

    object.logs()
    """

    def __init__(self, serverUrl: str, clientId: str, clientSecret: str, serverId=None):

        self.URL = serverUrl
        self.ID = clientId
        self.SECRET = clientSecret
        self.SERVER_ID = serverId

        if self.SERVER_ID:
            try:
                self.name = self.api_server()["server"]["name"]
            except KeyError:
                self.name = "Unknown"

            try:
                self.type = self.api_server()["server"]["type"]
            except KeyError:
                self.type = "generic-type"
        else:
            if not (self.getToken()):
                raise ValueError(
                    "Could not obtain a token from the server. Are your credentials correct?"
                )

    def __str__(self):
        return (
            f'URL: {self.URL}, Client ID: {self.ID}, using "{self.name}" ({self.SERVER_ID}) running a {self.type} server'
            if self.SERVER_ID
            else f"URL: {self.URL}, Client ID: {self.ID}"
        )
        # What this might look like:
        # "URL: https://panel.domain.com, Client ID: randomClientId, using YourServer (randomSecretKey) running a type-of server"
        #
        # or
        #
        # "URL: https://panel.domain.com, Client ID: randomClientId"

    def __repr__(self):
        return (
            f"Panel('{self.URL}', '{self.ID}', '{self.SECRET}', '{self.SERVER_ID}')"
            if self.SERVER_ID
            else f"Panel('{self.URL}', '{self.ID}', '{self.SECRET}')"
        )
        # What this might look like:
        # Panel('https://panel.domain.com', 'randomClientId', 'randomSecretKey', 'a1b236')
        #
        # or
        #
        # Panel('https://panel.domain.com', 'randomClientId', 'randomSecretKey')

    def invalidCode(self, given: object, override=False) -> bool:
        validCodes = []
        for i in range(200, 300):
            validCodes.append(i)
        isInvalidCode = not (given.status_code in validCodes)

        isServerOfflineMsg = given.json() == {
            "error": {"msg": "server offline", "code": "ErrServerOffline"}
        }
        return (
            isInvalidCode or isServerOfflineMsg if not (override) else isInvalidCode
        )  # Valid codes are 200-299.

    # The server can also return an 'error' as written here, even if the request was successful.
    # I've just made it so that it behaves exactly as if it had gotten an invalid response code, but added a manual override so that creating an object while this special error is returned is still possible.
    # If the response message changes or if there is a better way to handle this I'll change it

    def getToken(self) -> str:
        """
        Obtains a token from the server with the provided client ID and secret.
        Returns the token if succesful, error if not.

        This function is called anytime there is any contact with the daemon,
        because the token expires after a certain amount of time.
        """
        GET_TOKEN_HEADER = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            f"{self.URL}/oauth2/token",
            data=f"grant_type=client_credentials&client_id={self.ID}&client_secret={self.SECRET}",
            headers=GET_TOKEN_HEADER,
        )

        if self.invalidCode(response):
            print(self.invalidCode(response))
            raise ValueError(
                "Could not obtain a token from the server. Are your credentials corret?"
            )

        accessToken = response.json()["access_token"]

        return accessToken

    def tokenIt(self, serverID) -> tuple:
        token = self.getToken()
        serverID = serverID or self.SERVER_ID
        if not (serverID):
            raise TypeError("Missing 1 required argument: 'serverID'")
        AUTH_HEADER = {"Authorization": f"Bearer {token}"}

        return (
            serverID,
            AUTH_HEADER,
        )  # tuple[0] is the server ID and tuple[1] is the HTTP header

    # All GET methods

    def api_server(self, serverID=None) -> dict:
        """
        Gets the data of a given server from the API, not the config.

        Returns the physical data of the server.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/api/servers/{data[0]}"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        return response.json()

    # In it's current state this method was only implemented to get the server name, not much else.

    def daemon(self) -> bool:
        """
        Check if the API is active.
        Different from status(), which checks if the given server is running, not the actual API.

        Returns True if running, False if not.
        """
        data = {"Authorization": f"Bearer {self.getToken()}"}
        fullURL = f"{self.URL}/daemon"

        response = requests.get(fullURL, headers=data)

        if self.invalidCode(response):
            return False

        isRunning = response.json()["message"] == "daemon is running"
        # Returns True if the server is running ASSUMING that the running message is "daemon is running". If this message changes I'll fix it

        return isRunning

    def data_admin(self, serverID=None) -> dict:
        """
        Gets the full data of a server given a server ID as admin.

        Returns the data of the server.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        if response.json() == {"data": {}}:
            raise ServerError(
                f"Server returned an empty dataset: {response.json()}\nAre you using a client that inherits permissions for all servers?"
            )

        return response.json()["data"]
        # All server data is within one key: 'data'. If this is a bad idea I'll change it

    def logs(self, serverID=None) -> str:
        """
        Gets the server log given a server ID with the process described at
        https://hosting.povario.com/swagger/index.html#/default/get_daemon_server__id__console

        This is different from the client ID, which is only used when obtaining a token with getToken().
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/console"  # Todo: Implement selecting a timestamp

        response = requests.get(fullURL, headers=data[1])
        response.raise_for_status()

        if self.invalidCode(response, override=True):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        logs = response.json()["logs"]

        return logs

    def data(self, serverID=None) -> dict:
        """
        Gets the full data of a server given a server ID with the process described at
        https://hosting.povario.com/swagger/index.html#/default/get_daemon_server__id_

        Returns the data of the server.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/data"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        if response.json() == {"data": {}}:
            raise ServerError(
                f"Server returned an empty dataset: {response.json()}\nAre you using a client that inherits permissions for all servers?"
            )

        return response.json()["data"]  # Same as data_admin().

    def extract(self, filename: str, serverID=None) -> int:
        """
        Extracts a given file on the given server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/extract/{filename}"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        return response.status_code

    # def get_file(self,filename,serverID=None):
    #     """
    #     Lists a file or directory on the given server.
    #
    #     Returns either a dictonary with the file properties or a dictionary with individual files in a directory.
    #     """
    #
    #     data=self.tokenIt(serverID)
    #     fullURL=f'{self.URL}/proxy/daemon/server/{data[0]}/file/{filename}'
    #
    #     response=requests.get(f'{fullURL}',
    #         headers=data[1])
    #
    #     if self.invalidCode(response):
    #         raise ServerError(f'Server returned an invalid response: {response.json()}')
    #
    #     return response.json()
    #
    # Kinda broken. Don't use please thank you

    def stats(self, serverID=None, precise=False) -> dict:
        """
        Gets the server stats given a server ID with the process described at
        https://hosting.povario.com/swagger/index.html#/default/get_daemon_server__id__stats

        Returns a dictonary with the following values rounded to two decimal places:

        CPU Usage (float)
        RAM Usage in MB (float)

        Unless precise=True, in which case the values will not be rounded.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/stats"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            return response.json()

        cpu = response.json()["cpu"]
        ram = (response.json()["memory"] / 1000) / 1000

        formattedUsage = (
            {"cpu_usage": round(cpu, 2), "ram_usage": round(ram, 2)}
            if not (precise)
            else {"cpu_usage": cpu, "ram_usage": ram}
        )

        return formattedUsage

    def status(self, serverID=None) -> str:
        """
        Checks if the server is running.

        Returns True if running, False if not.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/status"

        response = requests.get(fullURL, headers=data[1])

        if self.invalidCode(response):
            raise ServerError(f"Server returned an invalid response: {response.json()}")

        return response.json()["running"]

    # All POST methods

    def update(self, serverID=None) -> int:
        """
        Updates a server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def archive(self, filename, serverID=None) -> int:
        """
        Archives a given file on the server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/archive/{filename}"

        response = requests.post(fullURL, data=f"{filename}", headers=data[1])

        return response.status_code

    def exec(self, command, serverID=None) -> int:
        """
        Executes a command on a given server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/console"

        response = requests.post(fullURL, data=command, headers=data[1])

        # previousLogs = self.logs(serverID)
        # reply=self.logs(serverID)
        # return reply.replace(previousLogs,'')
        #
        # Todo: return the logs instead of just the status code.

        return response.status_code

    def edit_data(self, key, value, serverID=None) -> int:
        """
        Edits the server config.

        Only returns the HTTP Response code.
        """

        data = self.tokenIt(serverID)
        reply = self.data(serverID)
        options = []
        for option in reply:
            options.append(option)
        optionExists = key in options
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/data"

        if optionExists:
            nonMatchingValue = type(reply[key]["value"]) != type(value)
            if nonMatchingValue:
                raise ValueError(
                    f"Value must match type for key '{key}'\n{type(value)} does not match {type(reply[key]['value'])}"
                )
        else:
            raise ValueError(
                f"'{key}' does not match any in the options list:\n{options}"
            )

        response = requests.post(
            fullURL, data=json.dumps({"data": reply}), headers=data[1]
        )

        return response.status_code

    def install(self, serverID=None) -> int:
        """
        Queues an installation for the given server.
        Potentially destructive action. (Can overwrite needed data such as config files)

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/install"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def kill(self, serverID=None) -> int:
        """
        Force quits a server without warning.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/kill"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def reload(self, serverID=None) -> int:
        """
        Reloads a server from disk.
        Potentially destructive action. (May overwrite server data)
        This method is NOT the same as restart(), which stops then starts a server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/reload"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def start(self, serverID=None):
        """
        Starts the given server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/start"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def stop(self, serverID=None):
        """
        Stops the given server.

        Only returns the HTTP response code.
        """

        data = self.tokenIt(serverID)
        fullURL = f"{self.URL}/proxy/daemon/server/{data[0]}/stop"

        response = requests.post(fullURL, headers=data[1])

        return response.status_code

    def restart(self, serverID=None) -> int:
        """
        Stops, then starts a given server.

        Only returns the HTTP status code from the start() method.
        """

        self.stop(serverID)
        sleep(1.5)
        response = self.start(serverID)

        return response

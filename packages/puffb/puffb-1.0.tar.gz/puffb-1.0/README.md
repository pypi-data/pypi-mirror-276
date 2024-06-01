# puffb

puffb is a small Python module for interacting with a Pufferpanel daemon.

Made this in my spare time because I needed it.

## Usage

### Prerequisites

First make sure you have Pufferpanel set up, and a deploy a server you intend to interact with it.
Create an OAuth2 application for this server. Like it says, **write down the secret key in a safe place. It is only ever displayed once.**

Now you have Pufferpanel, a server, it's server ID (randomly generated 8 character string, usually displayed in the URL in the browser), client ID and secret ID.

Make sure you have the requests and json modules available.

### Usage

```python
import puffb

...
```

Now you are ready to create a puffb!
Using the information you gathered before, create an object:

```python
server = puffb.Panel('your-server-url', 'your-client-id', 'your-secret-key', 'your-server-id')
```

Or, alternatively, if you want to use a client that has access to multiple servers at once:

```python
admin = puffb.Panel('your-server-url', 'your-client-id', 'your-secret-key')
```

Keep in mind that with this method, you will have to specify the server ID for most commands. Instead of

```python
admin.stop()
```
you must now type
```python
admin.stop(serverID = 'a1b2c3d4')
```

Now you can run various methods that return useful information about your server, or interact with it.

Examples:

```python
server.logs()
# Returns logs as a string

server.stats()
# {'cpu_usage': 5, 'ram_usage': 135.50}

server.status()
# True
# (Returns True if running, False if not)

server.stop()
# 204

server.edit_data(key = 'server-name', value = 'new and better name!')
# 204
```

Most of the `/daemon` endpoints specified in the Pufferpanel API docs are available for use through this module.

# ActionCable Client - A Python 3 client for Rails' Action Cable

[![pipeline status](https://gitlab.com/liant-sasu/actioncable-client/badges/main/pipeline.svg?ignore_skipped=true)](https://gitlab.com/liant-sasu/actioncable-client/-/commits/main)
[![coverage report](https://gitlab.com/liant-sasu/actioncable-client/badges/main/coverage.svg)](https://gitlab.com/liant-sasu/actioncable-client/-/commits/main)
[![Latest Release](https://gitlab.com/liant-sasu/actioncable-client/-/badges/release.svg)](https://gitlab.com/liant-sasu/actioncable-client/-/releases)

This library handles the connections and subscriptions and monitors the connection. It removes the underlaying websocket layer.

Currently authentication is not managed by this library.

## Credits

The project originate [this](https://github.com/tobiasfeistmantl/python-actioncable-zwei) that was
stalled for more than 5 years.

## ROADMAP

See [Roadmap file](ROADMAP.md)

## Get started

```
$ sudo pip3 install actioncable_client
```

## Example usage

### Setup the connection
Setup the connection to your Action Cable server.

```python
from actioncable.connection import Connection

connection = Connection(url='wss://url_to_your_cable_server/cable', origin='https://url_to_your_cable_server')
connection.connect()
```

### Subscribe to a channel

```python
from actioncable.subscription import Subscription

subscription = Subscription(connection, identifier={'channel': 'YourChannelCLassName'})

def on_receive(message: dict):
  print('New message arrived!')
  print('Action: {} | Data: {}'.format(message['action'], message['data']))

subscription.on_receive(callback=on_receive)
subscription.create()
```

### Send data

```python
from actioncable.message import Message

message = Message(action='update_something', data={'something': 'important'})

subscription.send(message)
```

### Unsubscribe

```python
subscription.remove()
```

### Close connection

```python
connection.disconnect()
```

## Development

Pull it up!

## You need help?

Ask a question on [StackOverflow](https://stackoverflow.com/) with the tag 'actioncable-client'.

## Contribution

Create pull requests on GitLab and help us to improve this package. There are some guidelines to follow:

 * Follow the conventions
 * Test all your implementations
 * Document methods which aren't self-explaining
 * try to follow the [Roadmap](ROADMAP.md)

Copyright (c) 2024 Liant SASU, MIT license

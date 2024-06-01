import actioncable_client.connection as conn

def test_instantiation():
  assert conn.Connection('http://example.com/cable') != None
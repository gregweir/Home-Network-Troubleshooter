from unittest.mock import patch, MagicMock

from homenet.checks import upnp


def _sock(recv_data=None, raises=None):
    sock = MagicMock()
    if raises:
        sock.recvfrom.side_effect = raises
    elif recv_data is not None:
        sock.recvfrom.return_value = (recv_data, ("1.2.3.4", 1900))
    else:
        sock.recvfrom.side_effect = upnp.socket.timeout("nope")
    return sock


def test_upnp_found(monkeypatch):
    monkeypatch.setattr(upnp.socket, "socket", lambda *a, **k: _sock(recv_data=b"HTTP/1.1 200 OK\r\nST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n"))
    assert upnp.run()[0].status == "ok"


def test_upnp_not_found_info(monkeypatch):
    monkeypatch.setattr(upnp.socket, "socket", lambda *a, **k: _sock(recv_data=None))
    assert upnp.run()[0].status == "info"


def test_upnp_socket_error(monkeypatch):
    def boom(*a, **k):
        raise OSError("no socket")
    monkeypatch.setattr(upnp.socket, "socket", boom)
    assert upnp.run()[0].status == "error"
from consistent_hash import ConsistentHash


def test_consistent_hashing():
    ch = ConsistentHash()
    ch.add_server(1)
    ch.add_server(2)
    ch.add_server(3)

    # Test request routing
    request_id = 123456
    server = ch.get_server(request_id)
    print(f"Request {request_id} routed to Server {server}")


if __name__ == "__main__":
    test_consistent_hashing()
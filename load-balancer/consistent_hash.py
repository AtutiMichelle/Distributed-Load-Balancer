class ConsistentHash:
    def __init__(self, slots=512, virtual_servers=9):
        self.slots = slots
        self.virtual_servers = virtual_servers
        self.ring = [None] * slots  # Maps slots to server IDs
        self.servers = set()  # Physical server IDs

    def _request_hash(self, request_id):
        return (request_id**2 + 2*request_id**2 + 17) % self.slots

    def _virtual_server_hash(self, server_id, replica_id):
        return (server_id**2 + replica_id + 2*replica_id + 25) % self.slots

    def add_server(self, server_id):
        self.servers.add(server_id)
        for j in range(self.virtual_servers):
            slot = self._virtual_server_hash(server_id, j)
            # Quadratic probing for collision resolution
            for k in range(self.slots):
                probe_slot = (slot + k*k) % self.slots
                if self.ring[probe_slot] is None:
                    self.ring[probe_slot] = server_id
                    break

    def remove_server(self, server_id):
        self.servers.discard(server_id)
        for j in range(self.virtual_servers):
            slot = self._virtual_server_hash(server_id, j)
            for k in range(self.slots):
                probe_slot = (slot + k*k) % self.slots
                if self.ring[probe_slot] == server_id:
                    self.ring[probe_slot] = None

    def get_server(self, request_id):
        slot = self._request_hash(request_id)
        for i in range(slot, slot + self.slots):
            probe_slot = i % self.slots
            if self.ring[probe_slot] is not None:
                return self.ring[probe_slot]
        return None
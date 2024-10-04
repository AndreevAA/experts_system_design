import Statuses

class Graph:
    def __init__(self, name=None, nodes=None, nodes_cnt=None):
        self.name = name
        if nodes is None:
            self.nodes = []
            self.nodes_cnt = 0

    def add_node(self, node):
        node_exist_state = self._is_node_number_exists(node.number)
        if node_exist_state[0]:
            return Statuses.error_status
        self.nodes.append(node)
        self.nodes_cnt += 1
        return Statuses.success_status

    def delete_node(self, node_number):
        node_exist_state = self._is_node_number_exists(node_number)
        if node_exist_state[0]:
            self.nodes.pop(node_exist_state[1])
            self.nodes_cnt -= 1
            return Statuses.success_status
        return Statuses.error_status

    def _is_node_number_exists(self, node_number):
        for _ in range(self.nodes_cnt):
            if self.nodes[_].number == node_number:
                return [True, _]
        return [False, None]
import typing
from .state import State
from cellworld_game import Point
from cellworld_game.torch.device import default_device
import torch


class GraphNode(object):

    def __init__(self, state: State, label: int):
        self.state = state
        self.label = label


class Graph(object):
    def __init__(self, nodes: typing.Dict[int, State]):
        self.nodes: typing.Dict[int, GraphNode] = dict()
        self.edges: typing.Dict[int, typing.Dict[int, typing.List[int]]] = dict()
        self.costs: typing.Dict[int, typing.Dict[int, float]] = dict()
        self.next_label = 0
        self._nodes_tensor = None
        self._nodes_labels_tensor = None
        if nodes:
            for label, state in nodes.items():
                self.add_node(state=state, label=label)

    @property
    def nodes_tensor(self):
        if self._nodes_tensor is None:
            self._nodes_tensor = torch.tensor([node.state.point
                                               for label, node
                                               in self.nodes.items()],
                                              dtype=torch.float32,
                                              device=default_device)
        return self._nodes_tensor

    @property
    def nodes_labels_tensor(self):
        if self._nodes_labels_tensor is None:
            self._nodes_labels_tensor = torch.tensor([label
                                                      for label
                                                      in self.nodes],
                                                     dtype=torch.int,
                                                     device=default_device)
        return self._nodes_labels_tensor

    def add_node(self, state: State, label: int = None) -> GraphNode:
        if label is None:
            label = self.next_label
            self.next_label += 1
        else:
            if label in self.nodes:
                raise ValueError(f"label '{label}' already exists")
            self.next_label = label + 1
        node = GraphNode(state=state, label=label)
        self.nodes[label] = node
        self.edges[label] = dict()
        self.costs[label] = dict()
        self._nodes_tensor = None
        self._nodes_labels_tensor = None
        return node

    def __getitem__(self, label: int) -> GraphNode:
        return self.nodes[label]

    def connect(self, src_label: int, dst_label: int, path: typing.List[int] = None):
        if src_label not in self.nodes:
            raise KeyError('source label does not exist')
        if dst_label not in self.nodes:
            raise KeyError('destination label does not exist')
        if dst_label not in self.edges[src_label]:
            if path is None:
                path = [src_label, dst_label]
            cost = 0
            prev_step = path[0]
            for step in path[1:]:
                cost += Point.distance(self.nodes[prev_step].state.point, self.nodes[step].state.point)
                prev_step = step
            self.costs[src_label][dst_label] = cost
            self.edges[src_label][dst_label] = path
            self.edges[dst_label][src_label] = [i for i in path[::-1]]
            self.costs[dst_label][src_label] = cost

    def get_centrality(self, depth: int = 3) -> typing.Dict[int, float]:
        max_iter = depth
        if len(self.nodes) == 0:
            raise ValueError('Graph has no nodes')
        x = {label: 1.00 for label in self.nodes}
        for _ in range(max_iter):
            x_last = x
            x = x_last.copy()
            for label in x:
                connections = self.edges[label]
                for conn_label in connections:
                    x[label] += x_last[conn_label]
        norm = sum(x.values())
        x = {label: centrality / norm for label, centrality in x.items()}
        return x

    def get_lppo(self, n: int, depth: int = 3) -> typing.List[int]:
        centrality = self.get_centrality(depth=depth)
        planning_index: typing.Dict[int, float] = dict()
        for label, connections in self.edges.items():
            max_diff = 0
            for conn_label in connections:
                diff = abs(centrality[conn_label]-centrality[label])
                if diff > max_diff:
                    max_diff = diff
            planning_index[label] = max_diff / centrality[label]
        return sorted(planning_index, key=planning_index.get, reverse=True)[:n]

    def get_subgraph(self, nodes: typing.List[int]) -> "Graph":
        tlppo_graph = Graph()
        for label, node in self.nodes.items():
            tlppo_graph.add_node(state=node.state, label=label)
        for src in nodes:
            for dst in nodes:
                if src == dst:
                    continue
                s_path = self.get_shortest_path(src=src, dst=dst)
                if s_path:
                    for label in s_path[1:-1]:
                        if label in nodes:
                            break
                    else:
                        tlppo_graph.connect(src_label=src, dst_label=dst, path=s_path)
        return tlppo_graph

    def get_shortest_path(self, src: int, dst: int) -> typing.List[int]:
        def heuristic(node, goal):
            return Point.distance(self.nodes[node].state.point,
                                  self.nodes[goal].state.point)

        import heapq
        if src == 90 and dst == 3:
            print("stop")

        # Priority queue
        frontier = []
        heapq.heappush(frontier, (0.0, src))

        # Stores the cost to reach each node
        cost_so_far = {src: 0.0}

        # Stores the path
        came_from = {src: None}

        current_node = None
        is_connected = False
        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            # Check if the goal is reached
            if current_node == dst:
                is_connected = True
                break

            for next_node in self.edges[current_node]:
                new_cost = cost_so_far[current_node] + self.costs[current_node][next_node] + heuristic(next_node, dst)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    heapq.heappush(frontier, (new_cost, next_node))
                    came_from[next_node] = current_node

        if not is_connected:
            return []

        # Reconstruct path
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = came_from[current_node]
        path.reverse()
        return path

    def get_nearest(self, point: Point.type) -> GraphNode:
        labels = self.nodes_labels_tensor
        nodes = self.nodes_tensor
        point_tensor = torch.tensor(point,
                                    dtype=torch.float32,
                                    device=default_device)
        distances = torch.norm(nodes - point_tensor, dim=1)
        closest_index = torch.argmin(distances)
        closest_id = labels[closest_index].item()
        return self.nodes[closest_id]

from dataclasses import dataclass
from itertools import combinations

from solutions.solution import Solution
from utils.files import FileUtils

class Node:
    id: str
    conns: set["Node"]

    def __init__(self, id: str):
        self.id = id
        self.conns = set()

class Connection:
    node1: Node
    node2: Node
    score: int = -1

    def __init__(self, n1: Node, n2: Node, score: int = -1):
        self.node1 = n1
        self.node2 = n2
        self.score = score

    def key(self) -> str:
        return "|".join(sorted([self.node1.id, self.node2.id]))

NodeMap = dict[str, Node]

class Day25Pt1Solution(Solution):

    def run(self) -> None:
        lines = FileUtils.read_lines('resources/day25/input.txt')
        node_map: NodeMap = self.parse_nodes(lines)

        for node in node_map.values():
            print(f"{node.id} -> {" & ".join(map(lambda n: n.id, node.conns))}")
        print(f"Total nodes: {len(node_map.keys())}")

        # Compute the #steps to the further nodes for each node in the web.
        longest: dict[str, int] = {}
        for node_id, node in node_map.items():
            longest[node_id] = self.longest_route(node_map, node)

        unique_longest = list(set(longest.values()))
        print(f"Unique longest: {unique_longest}")

        total_groups = self.gather_groups(node_map, [])
        print(f"Total groups to start: {len(total_groups)}")

        # My theory was the nodes with the lowest step count to reach any one node are most central
        # to the web. Therefore probably good candidates for points to cleanly cut the web.
        # I planned to make combinations of these low-scoring candidates/connections until I got the answer.
        # 
        # I tried various methods of scoring ndoes, connections, combinations of connections, etc.
        # The problem was always too big to reasonably tackle. I was doubting my scoring methods gave enough
        # disturction. Then I decided to count the number of connections that have the same score (population
        # per score), and testing against the input because the example is too small a sample to be meaingful. 
        # 
        # This is when something special jumped out. 
        # 
        # There are exactly 3 connections with the connection score. More than a little suspcious. Decided to
        # take these exact 3 (and if not those, combinations with the other small slices). It turns out 
        # those are the exact 3 connections you need of course to get 2 groups. Puzzle solved!
        conns: dict[str, Connection] = {}
        for node in node_map.values():
            for conn in node.conns:
                conn_key = "|".join(sorted([node.id, conn.id]))
                if not conn_key in conns:
                    score = longest[node.id] * longest[conn.id]
                    # Note: I'm keepting the assignment of n1/n2 arbitrary instead of matching
                    # the key order, which sorts alphabetically. Need ot pay attention to this just in case.
                    conns[conn_key] = Connection(node, conn, score)

        # map: score -> population
        unique_scores: dict[int, int] = {}
        for conn in conns.values():
            pop = unique_scores.get(conn.score, 0)
            unique_scores[conn.score] = pop+1

        # This shows somewhat of a correlation between low scores and which connections to cut.
        # Not smoking gun, but the ones we want are in the upper third/half.
        print("\nConn scores:")
        sorted_keys = sorted(list(unique_scores.keys()))
        for key in sorted_keys:
            print(f"{key}: {unique_scores[key]}")

        lowest_conns = sorted(conns.keys(), key=lambda key: conns[key].score)
        conn_slice = lowest_conns[:3]
        # conn_slice = lowest_conns

        print("3 lowest conns:")
        for conn in conn_slice:
            print(f"{conn}: {conns[conn].score}")

        groups = self.gather_groups(node_map, map(lambda id: conns[id], conn_slice))
        print(f"New total groups: {len(groups)}")
        print(f"Total nodes: {len(node_map)}")
        print(f"Group sizes: {", ".join(map(str, map(len, groups)))}")

        if len(groups) != 2:
            print(f"Solution not found :(")
        else:
            soln = len(groups[0]) * len(groups[1])
            print(f"Solution: {soln}")

    
    def parse_nodes(self, lines: list[str]) -> NodeMap:
        """Parse lines from file into a map"""
        node_map: NodeMap = {}

        for line in lines:
            tokens = line.split(": ")
            node_id = tokens[0]
            conn_ids = tokens[1].split(" ")

            node = node_map.get(node_id, Node(node_id))
            for conn_id in conn_ids:
                conn = node_map.get(conn_id, Node(conn_id))
                conn.conns.add(node)
                node.conns.add(conn)
                node_map[conn.id] = conn
            node_map[node.id] = node

        return node_map

    def longest_route(self, node_map: NodeMap, start: Node) -> int:
        routes = self.shortest_routes(node_map, start)
        return max(routes.values())

    def shortest_routes(self, node_map: NodeMap, start: Node) -> dict[str, int]:
        queue: list[tuple[str, int]] = [(start.id, 0)]
        visited: dict[str, int] = {}

        while len(queue) > 0:
            (node_id, steps) = queue.pop(0)

            # if this node was already visited in the current step num or less
            # this ignore this route.
            if node_id in visited and visited[node_id] <= steps:
                continue

            visited[node_id] = steps

            node = node_map[node_id]
            for conn in node.conns:
                queue.append((conn.id, steps+1))

        return visited

    def gather_groups(self, node_map: NodeMap, cuts: list[Connection]) -> list[list[str]]:
        # Apply the cuts (undone at end of func)
        for cut in cuts:
            cut.node1.conns.remove(cut.node2)
            cut.node2.conns.remove(cut.node1)

        unvisited = set(node_map.keys())
        distinct_groups: list[list[str]] = []

        while len(unvisited) > 0:
            group: list[str] = []

            # Grab any unvisited node, then step to any nodes it connects to, draining the set.
            # Rinse and repeat to count groups.
            queue = [next(iter(unvisited))]
            while len(queue) > 0:
                node_id = queue.pop(0)

                # e.g. if visited... skip
                if not node_id in unvisited:
                    continue

                unvisited.remove(node_id)
                group.append(node_id)

                for conn in node_map[node_id].conns:
                    queue.append(conn.id)

            distinct_groups.append(group)

        # Undo the cuts
        for cut in cuts:
            cut.node1.conns.add(cut.node2)
            cut.node2.conns.add(cut.node1)

        return distinct_groups
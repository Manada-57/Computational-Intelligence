from collections import deque
import heapq

class Graph:
        def __init__(self):
        # adjacency list: node -> [(neighbor, cost)]
                self.graph = {}

        def add_node(self, node):
                if node not in self.graph:
                        self.graph[node] = []

        def add_edge(self, u, v, cost):
                if u not in self.graph:
                        self.add_node(u)
                if v not in self.graph:
                        self.add_node(v)
                self.graph[u].append((v, cost))
                self.graph[v].append((u, cost))

        def delete_node(self, node):
                if node in self.graph:
                        del self.graph[node]
                for n in self.graph:
                        self.graph[n] = [(v, c) for v, c in self.graph[n] if v != node]

        def delete_edge(self, u, v):
                if u in self.graph:
                        self.graph[u] = [(x, c) for x, c in self.graph[u] if x != v]
                if v in self.graph:
                        self.graph[v] = [(x, c) for x, c in self.graph[v] if x != u]

        def display_adjacency_list(self):
                print("\nAdjacency List:")
                for node in self.graph:
                        print(f"{node} -> {self.graph[node]}")

        def bfs_search(self, start, goal):
                fringe = deque([start])
                visited = set([start])
                search_path = []
                print("\nBFS Search:")
                while fringe:
                        #print("Search Order:", " -> ".join(search_path))
                        print("Fringe:", list(fringe))
                        current = fringe.popleft()
                        search_path.append(current)
                        print("Expanding:", current)
                        if current in goal:
                                return search_path
                                break
                        else:
                                for neighbor, _ in self.graph.get(current, []):
                                        if neighbor not in visited:
                                                visited.add(neighbor)
                                                #search_path.append(neighbor)
                                                fringe.append(neighbor)
                                        if neighbor in goal:
                                                break
                return None

        def dfs_search(self, start, goal):
                fringe = [start]
                visited = set([start])
                path_tracker = {start: [start]}
                print("\nDFS Search:")
                while fringe:
                        print("Fringe:", fringe)
                        current = fringe.pop()
                        print("Expanding:", current)
                        if current in goal:
                                return path_tracker[current]
                        for neighbor, _ in reversed(self.graph.get(current, [])):
                                if neighbor not in visited:
                                        visited.add(neighbor)
                                        path_tracker[neighbor] = path_tracker[current] + [neighbor]
                                        fringe.append(neighbor)
                return None

        def ucs_search(self, start, goal):
                fringe = [(0, start)]
                cost_so_far = {start: 0}
                path_tracker = {start: [start]}
                print("\nUCS Search:")
                while fringe:
                        print("Fringe:", fringe)
                        current_cost, current = heapq.heappop(fringe)
                        print(f"Expanding: {current} (cost={current_cost})")
                        if current in goal:
                                return path_tracker[current], current_cost
                        for neighbor, weight in self.graph.get(current, []):
                                new_cost = current_cost + weight
                                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                                        cost_so_far[neighbor] = new_cost
                                        path_tracker[neighbor] = path_tracker[current] + [neighbor]
                                        heapq.heappush(fringe, (new_cost, neighbor))
                return None, None

        def construct_path(self, parent, goal):
                path = []
                while goal is not None:
                        path.append(goal)
                        goal = parent[goal]
                return path[::-1]

g = Graph()
n = int(input("Enter number of nodes: "))
print("Enter nodes:")
for i in range(n):
        g.add_node(input())
e = int(input("Enter number of edges: "))
print("Enter edges (u v ):")
for i in range(e):
        u, v= input().split()
        g.add_edge(u, v,1)
while True:
        print("\n----- MENU -----")
        print("1. BFS Search")
        print("2. DFS Search")
        print("3. UCS Search")
        print("4. Add Node")
        print("5. Add Edge")
        print("6. Delete Node")
        print("7. Delete Edge")
        print("8. Display Adjacency List")
        print("9. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
                start_node = input("Enter start node: ")
                num_goals = int(input("Enter number of goal nodes: "))
                goal_nodes = []
                print("Enter goal nodes:")
                for i in range(num_goals):
                        goal_nodes.append(input())
                search_path = g.bfs_search(start_node, goal_nodes)
                if search_path:
                        print("Search Order:", " -> ".join(search_path))
                else:
                        print("Failed")
        elif choice == "2":
                start_node = input("Enter start node: ")
                num_goals = int(input("Enter number of goal nodes: "))
                goal_nodes = []
                print("Enter goal nodes:")
                for i in range(num_goals):
                        goal_nodes.append(input())
                path = g.dfs_search(start_node, goal_nodes)
                if path:
                        print("Path:", " -> ".join(path))
                else:
                        print("Goal not reachable")
        elif choice == "3":
                print("Enter edges with cost (u v c):")
                for i in range(e):
                        u, v, cost=input().split()
                        g.delete_edge(u,v)
                        cost=int(cost)
                        g.add_edge(u,v,cost)
                start_node = input("Enter start node: ")
                num_goals = int(input("Enter number of goal nodes: "))
                goal_nodes = []
                print("Enter goal nodes:")
                for i in range(num_goals):
                        goal_nodes.append(input())
                path, cost = g.ucs_search(start_node, goal_nodes)
                if path:
                        print("Path:", " -> ".join(path))
                        print("Cost:", cost)
                else:
                        print("Goal not reachable")
        elif choice == "4":
                node = input("Enter node to add: ")
                g.add_node(node)
                print(f"Node '{node}' added successfully.")
        elif choice == "5":
                u = input("Enter first node: ")
                v = input("Enter second node: ")
                '''cost = input("Enter cost (default 1): ")
                if cost == "":
                        cost = 1
                else:
                        cost = int(cost)'''
                g.add_edge(u, v)
                print(f"Edge '{u}' - '{v}' with added successfully.")
        elif choice == "6":
                node = input("Enter node to delete: ")
                g.delete_node(node)
                print(f"Node '{node}' deleted successfully.")
        elif choice == "7":
                u = input("Enter first node: ")
                v = input("Enter second node: ")
                g.delete_edge(u, v)
                print(f"Edge '{u}' - '{v}' deleted successfully.")
        elif choice == "8":
                g.display_adjacency_list()
        elif choice == "9":
                break
        else:
                print("Invalid choice")

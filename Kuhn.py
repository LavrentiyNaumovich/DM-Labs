def read_graph(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        if not lines:
            print("Input file is empty.")
            return None, 0, 0
        n, m = map(int, lines[0].strip().split())
        adj = [[] for _ in range(n + 1)]  
        for line in lines[1:]:
            parts = list(map(int, line.strip().split()))
            if not parts:
                continue
            u = parts[0]
            # Sort neighbors for predictability
            adj[u].extend(sorted(parts[1:]))
        return adj, n, m
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, 0, 0

def write_matching(pair_u, output_path):
    try:
        with open(output_path, 'w') as f:
            for u in range(1, len(pair_u)):
                v = pair_u[u]
                if v != 0:
                    f.write(f"{u} {v}\n")
    except Exception as e:
        print(f"Error writing file: {e}")

def kuhn(adj, n, m):
    pair_u = [0] * (n + 1)
    pair_v = [0] * (m + 1)
    result = 0

    for u in range(1, n + 1):
        if pair_u[u] == 0:
            stack = [u]
            parent = [-1] * (n + 1)  
            visited = [False] * (n + 1)
            visited[u] = True
            path_found = False

            while stack and not path_found:
                current = stack.pop()
                for v in adj[current]:
                    if pair_v[v] == 0:

                        pair_u[current] = v
                        pair_v[v] = current
                        result += 1

                        prev_u = parent[current]
                        while prev_u != -1:
                            prev_v = pair_u[prev_u]
                            pair_u[prev_u] = pair_v[prev_v]
                            pair_v[prev_v] = prev_u
                            current = prev_u
                            prev_u = parent[prev_u]
                        path_found = True
                        break
                    elif not visited[pair_v[v]]:
                        visited[pair_v[v]] = True
                        parent[pair_v[v]] = current
                        stack.append(pair_v[v])
    return pair_u, result

def main():
    print("Program to find the maximum matching in a bipartite graph")

    input_file = input("Enter the path to the input file: ").strip()

    adj, n, m = read_graph(input_file)
    if adj is None or n == 0 or m == 0:
        print("Failed to read the graph from the input file.")
        return

    print(f"Graph successfully read: {n} vertices in the left partition and {m} vertices in the right partition.")

    pair_u, matching = kuhn(adj, n, m)

    print(f"The maximum matching contains {matching} pairs.")

    output_file = input("Enter the path to the output file to write the matching: ").strip()

    write_matching(pair_u, output_file)
    print(f"Matching has been written to the file {output_file}.")

if __name__ == "__main__":
    main()

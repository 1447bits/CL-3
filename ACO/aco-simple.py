import random
import math

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        distances: 2D matrix of distances between cities
        n_ants: number of ants per iteration
        n_best: number of best ants who deposit pheromone
        n_iterations: number of iterations
        decay: rate at which pheromone decays
        alpha: influence of pheromone
        beta: influence of distance
        """
        self.distances = distances
        self.pheromone = [[1 / len(distances) for j in range(len(distances))] for i in range(len(distances))]
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", math.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            
            # Print iteration result
            path_str = ' -> '.join([str(move[0]) for move in shortest_path[0]] + [str(shortest_path[0][-1][1])])
            print(f"Iteration {i+1:3d}: Best path = {path_str} | Distance = {shortest_path[1]:.2f}")
            
            self.pheromone = [[col * self.decay for col in row] for row in self.pheromone]

        print("\nAll-time shortest path found:")
        final_path_str = ' -> '.join([str(move[0]) for move in all_time_shortest_path[0]] + [str(all_time_shortest_path[0][-1][1])])
        print(f"Path = {final_path_str}")
        print(f"Distance = {all_time_shortest_path[1]:.2f}")
        return all_time_shortest_path

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move[0]][move[1]] += 1.0 / self.distances[move[0]][move[1]]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele[0]][ele[1]]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # return to starting city
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = [p ** self.alpha for p in pheromone]
        heuristic = [(1 / d) ** self.beta if d > 0 else 0 for d in dist]
        prob = []
        for p, h, i in zip(pheromone, heuristic, self.all_inds):
            prob.append(0 if i in visited else p * h)
        norm = sum(prob)
        if norm == 0:
            return random.choice(list(set(self.all_inds) - visited))
        prob = [p / norm for p in prob]
        move = random.choices(self.all_inds, weights=prob)[0]
        return move


# Example usage with sample distance matrix
if __name__ == "__main__":
    # Distance matrix between 5 cities
    distances = [
        [0, 2, 2, 5, 7],
        [2, 0, 4, 8, 2],
        [2, 4, 0, 1, 3],
        [5, 8, 1, 0, 2],
        [7, 2, 3, 2, 0]
    ]

    colony = AntColony(distances, n_ants=10, n_best=3, n_iterations=100, decay=0.95, alpha=1, beta=2)
    shortest_path = colony.run()
    
    print("\nShortest path found:")
    print(shortest_path[0])
    print("Path length:", shortest_path[1])

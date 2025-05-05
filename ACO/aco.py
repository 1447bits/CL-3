import numpy as np
import matplotlib.pyplot as plt
import random
import time

class AntColonyOptimizer:
    def __init__(self, distances, n_ants=10, decay=0.95, alpha=1.0, beta=2.0):
        """
        Initialize the ACO solver.
        
        Parameters:
        - distances: matrix of distances between cities
        - n_ants: number of ants to use
        - decay: pheromone decay rate
        - alpha: pheromone importance
        - beta: distance importance
        """
        self.distances = distances
        self.n_cities = len(distances)
        self.n_ants = n_ants
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromones = np.ones((self.n_cities, self.n_cities))
        self.all_inds = range(self.n_cities)
        
    def run(self, n_iterations):
        """Run the ACO algorithm for n_iterations."""
        best_path = None
        best_path_length = float('inf')
        all_best_path_lengths = []
        
        for i in range(n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromones(all_paths)
            
            # Find iteration's best path
            current_best_path, current_best_path_length = self.find_best_path(all_paths)
            
            # Update overall best path
            if current_best_path_length < best_path_length:
                best_path = current_best_path
                best_path_length = current_best_path_length
            
            all_best_path_lengths.append(best_path_length)
            
            # Print progress
            if i % 10 == 0:
                print(f"Iteration {i}: Best path length = {best_path_length:.2f}")
            
        return best_path, best_path_length, all_best_path_lengths
        
    def gen_all_paths(self):
        """Generate paths for all ants."""
        all_paths = []
        for ant in range(self.n_ants):
            path = self.gen_path(0)  # Start from city 0
            all_paths.append((path, self.path_length(path)))
        return all_paths
    
    def gen_path(self, start):
        """Generate a path for a single ant starting from a given city."""
        path = [start]
        visited = {start}
        
        while len(path) < self.n_cities:
            current = path[-1]
            unvisited = list(set(self.all_inds) - visited)
            
            # Calculate probabilities
            probabilities = self.calculate_probabilities(current, unvisited)
            
            # Choose next city
            next_city = random.choices(unvisited, weights=probabilities)[0]
            
            path.append(next_city)
            visited.add(next_city)
            
        return path
    
    def calculate_probabilities(self, current, unvisited):
        """Calculate transition probabilities."""
        probabilities = []
        
        for city in unvisited:
            # Get pheromone and distance values
            pheromone = self.pheromones[current, city]
            distance = self.distances[current, city]
            
            if distance == 0:  # Avoid division by zero
                distance = 1e-10
                
            # Apply formula: (pheromone^alpha) * (1/distance^beta)
            probability = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
            probabilities.append(probability)
            
        # Normalize probabilities
        sum_probabilities = sum(probabilities)
        if sum_probabilities == 0:  # Avoid division by zero
            return [1.0 / len(unvisited)] * len(unvisited)
        
        return [p / sum_probabilities for p in probabilities]
    
    def spread_pheromones(self, all_paths):
        """Update pheromone levels based on ant paths."""
        # Decay existing pheromones
        self.pheromones *= self.decay
        
        # Add new pheromones based on path quality
        for path, path_length in all_paths:
            # Amount of pheromone to deposit
            pheromone_amount = 1.0 / path_length
            
            # Deposit pheromones on the path
            for i in range(self.n_cities):
                city_from = path[i]
                city_to = path[(i + 1) % self.n_cities]  # Wrap around for the return
                self.pheromones[city_from, city_to] += pheromone_amount
                self.pheromones[city_to, city_from] += pheromone_amount  # Symmetric
    
    def path_length(self, path):
        """Calculate the total length of a path."""
        total_length = 0
        for i in range(self.n_cities):
            city_from = path[i]
            city_to = path[(i + 1) % self.n_cities]  # Return to start
            total_length += self.distances[city_from, city_to]
        return total_length
    
    def find_best_path(self, all_paths):
        """Find the best path from all_paths."""
        best_path, best_path_length = min(all_paths, key=lambda x: x[1])
        return best_path, best_path_length
            

def generate_random_cities(n_cities, seed=None):
    """Generate random city coordinates."""
    if seed is not None:
        np.random.seed(seed)
    
    # Generate in a 2D grid
    x_coords = np.random.rand(n_cities) * 100
    y_coords = np.random.rand(n_cities) * 100
    
    # Calculate distance matrix
    distances = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                # Euclidean distance
                distances[i, j] = np.sqrt((x_coords[i] - x_coords[j])**2 + 
                                         (y_coords[i] - y_coords[j])**2)
    
    return distances, x_coords, y_coords

def plot_path(x_coords, y_coords, path, title):
    """Plot the path on a 2D grid."""
    plt.figure(figsize=(10, 8))
    
    # Plot cities
    plt.scatter(x_coords, y_coords, s=100, c='red')
    
    # Plot path
    for i in range(len(path)):
        city_from = path[i]
        city_to = path[(i + 1) % len(path)]  # Return to start
        plt.plot([x_coords[city_from], x_coords[city_to]], 
                 [y_coords[city_from], y_coords[city_to]], 'b-', alpha=0.7)
    
    # Add city labels
    for i, (x, y) in enumerate(zip(x_coords, y_coords)):
        plt.annotate(str(i), (x, y), fontsize=12)
    
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_convergence(all_best_path_lengths):
    """Plot the convergence of the algorithm."""
    plt.figure(figsize=(10, 6))
    plt.plot(all_best_path_lengths)
    plt.title('ACO Algorithm Convergence')
    plt.xlabel('Iteration')
    plt.ylabel('Best Path Length')
    plt.grid(True)
    plt.show()


def main():
    # Problem parameters
    n_cities = 20
    n_ants = 20
    n_iterations = 100
    
    # Generate random cities
    distances, x_coords, y_coords = generate_random_cities(n_cities, seed=42)
    
    # Print distance matrix
    print("Distance Matrix:")
    print(distances)
    
    # Initialize and run ACO
    print("\nStarting Ant Colony Optimization...")
    start_time = time.time()
    
    aco = AntColonyOptimizer(
        distances=distances,
        n_ants=n_ants,
        decay=0.95,
        alpha=1.0,
        beta=2.0
    )
    
    best_path, best_path_length, all_best_path_lengths = aco.run(n_iterations)
    
    end_time = time.time()
    run_time = end_time - start_time
    
    # Print results
    print("\nResults:")
    print(f"Best path: {best_path}")
    print(f"Best path length: {best_path_length:.2f}")
    print(f"Algorithm run time: {run_time:.2f} seconds")
    
    # Plot the best path
    plot_path(x_coords, y_coords, best_path, f'Best TSP Path (Length: {best_path_length:.2f})')
    
    # Plot convergence
    plot_convergence(all_best_path_lengths)


if __name__ == "__main__":
    main()

import random
import csv

class Individual:
    def __init__(self, genes=None, size=16):
        self.size = size
        self.genes = genes if genes else self.generate_random()
        self.fitness = self.calculate_fitness()

    def generate_random(self):
        """Generate a random gene sequence."""
        return [random.randint(0, self.size - 1) for _ in range(self.size)]

    def calculate_fitness(self):
        """Calculate the number of non-attacking queen pairs."""
        total_pairs = (self.size * (self.size - 1)) // 2
        attacking_pairs = 0

        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.genes[i] == self.genes[j] or abs(self.genes[i] - self.genes[j]) == abs(i - j):
                    attacking_pairs += 1

        return total_pairs - attacking_pairs

    def mutate(self, mutation_rate=0.1):
        """Mutate a gene with a probability defined by mutation_rate."""
        if random.random() < mutation_rate:
            col = random.randint(0, self.size - 1)
            new_row = random.randint(0, self.size - 1)
            self.genes[col] = new_row
            self.fitness = self.calculate_fitness()


class Problem:
    def __init__(self, population_size=100, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [Individual() for _ in range(population_size)]

    def fitness_function(self, individual):
        return individual.fitness
    
    def is_solution_found(self):
        return any(ind.fitness == 120 for ind in self.population)


class GeneticAlgorithm:
    def __init__(self, problem, max_generations=1000, elitism_k=1):
        self.problem = problem
        self.max_generations = max_generations
        self.elitism_k = elitism_k
        self.log_file = open("run_log.csv", "w", newline="")  # Open CSV file
        self.csv_writer = csv.writer(self.log_file)
        self.csv_writer.writerow(["Generation", "Best Fitness", "Genes"])  # Write header

    def log(self, generation, best_individual):
        """Write generation number, best fitness, and best genes to the CSV file."""
        log_message = f"Generation {generation}: Best Fitness = {best_individual.fitness}, Genes = {best_individual.genes}"
        print(log_message)  # Print to console
        self.csv_writer.writerow([generation, best_individual.fitness, ",".join(map(str, best_individual.genes))])

    def selection(self):
        """Select an individual using roulette selection."""
        total_fitness = sum(self.problem.fitness_function(ind) for ind in self.problem.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for ind in self.problem.population:
            current += self.problem.fitness_function(ind)
            if current > pick:
                return ind
        return self.problem.population[0]

    def crossover(self, parent1, parent2):
        """Perform crossover at two random points."""
        point1, point2 = sorted(random.sample(range(parent1.size), 2))
        new_genes = parent1.genes[:point1] + parent2.genes[point1:point2] + parent1.genes[point2:]
        return Individual(new_genes)

    def run(self):
        for generation in range(1, self.max_generations + 1):
            new_population = sorted(self.problem.population, key=lambda x: x.fitness, reverse=True)[:self.elitism_k]
            
            while len(new_population) < self.problem.population_size:
                parent1 = self.selection()
                parent2 = self.selection()
                child = self.crossover(parent1, parent2)
                child.mutate(self.problem.mutation_rate)
                new_population.append(child)
            
            self.problem.population = new_population
            best_individual = max(new_population, key=lambda x: x.fitness)
            self.log(generation, best_individual)
            
            if self.problem.is_solution_found():
                break

        self.log_file.close()  # Close the CSV file
        return best_individual


# Run the algorithm and save logs
problem = Problem(population_size=100, mutation_rate=0.1)
ga = GeneticAlgorithm(problem, max_generations=1000, elitism_k=1)
best_solution = ga.run()

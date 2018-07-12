from random import randrange, random, uniform, randint
import copy

CONDITION_LENGTH = 8;
POPULATION_SIZE = 10;
MUTATION_RATE = 0.025;

TOTAL_GENERATION = 20;
TOTAL_FITNESS = 65025;

class PopulationSet(object):
  def __init__(self):
    self.binaryString = 0;
    self.fitness = 0;

populationSet = [PopulationSet() for _ in range(POPULATION_SIZE)];
BESTINDIVIDUAL = PopulationSet();

def binToNumber(binary):
  return int(binary, 2);
  #Converts binary to Integer.

def evaluate(individual):
  global BESTINDIVIDUAL

  number = binToNumber(individual.binaryString);
  individual.fitness = (number ** 2);
  #X squared fitness function
	
  if (individual.fitness > BESTINDIVIDUAL.fitness):
    BESTINDIVIDUAL = copy.copy(individual);
	#Finds and sets best individual.

def printAverage():
  total = 0;
  grandTotal = 0;

  for population in populationSet[:]:
    grandTotal += population.fitness;
    total += 1;

  print(grandTotal / total);
  #Calculates the average.

def createPopulation():
  global populationSet
  for population in populationSet[:]:
    population.binaryString = "";
    for i in range(CONDITION_LENGTH):
      population.binaryString += str(randrange(2))
    evaluate(population);
	#Creates and evalutates the population.

def tournamentSelection(numberOfTimes):
    children = [None, None];

    for child in range(len(children)):
      for i in range(numberOfTimes):
        individual = populationSet[randrange(POPULATION_SIZE)];
        if (children[child] is None) or individual.fitness > children[child].fitness:
          children[child] = copy.copy(individual);
    return children;
	#Tournament selection that favours high fitness.

def onePointCrossover(parents):
  children = [PopulationSet(), PopulationSet()];

  parent1 = parents[0].binaryString;
  parent2 = parents[1].binaryString;
  crossoverNum = randint(1, (CONDITION_LENGTH - 1));
  #Initialises and sets the crossover point

  children[0].binaryString = parent1[:crossoverNum] + parent2[crossoverNum:];
  children[1].binaryString = parent2[:crossoverNum] + parent1[crossoverNum:];
  #Finishes crossover of both children
	
  return children;

def mutation(parents):
  children = [PopulationSet(), PopulationSet()];

  children[0].binaryString = parents[0].binaryString;
  children[1].binaryString = parents[1].binaryString;
  #Initialises mutation.

  for child in range(len(children)):
    concatString = "";
    for binary in children[child].binaryString[:]:
      if 0.1 < random() < (0.1 + MUTATION_RATE):
        concatString += str(1 - int(binary));
      else:
        concatString += binary
    children[child].binaryString = concatString;
	#Bitwise mutation.
	
  return children;


def main():
  global populationSet;

  createPopulation();
  generation = 1;

  print("Generation: " + str(generation));
  print("Highest Solution is: " + BESTINDIVIDUAL.binaryString);
  print("Highest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");

  while (generation < TOTAL_GENERATION):
    generation += 1;

    # Create child Population
    child_population = [];
    while len(child_population) < POPULATION_SIZE:
      selectParents = tournamentSelection(2);

      newChildren = onePointCrossover(selectParents);
      newChildren = mutation(newChildren);

      evaluate(newChildren[0]);
      evaluate(newChildren[1]);

      child_population.append(newChildren[0]);
      child_population.append(newChildren[1]);

    populationSet = populationSet + child_population
    populationSet.sort(key=lambda x: x.fitness, reverse=True)
	#Adds together previous and child population, then sorts them.
	
    for i in range(POPULATION_SIZE):
      populationSet.pop();
	#Pops the bottom half of the stack.

    #Print after generation
    print("Generation: " + str(generation));
    print("Highest Solution is: " + BESTINDIVIDUAL.binaryString);
    print("Highest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");
	
	
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print "Didn't find the best solution"

from random import randrange, random, uniform, randint
import copy

CONDITION_LENGTH = 5;
POPULATION_SIZE = 20;
MUTATION_RATE = 0.025;
TOTAL_GENERATION = 20;
TOTAL_FITNESS = 0;

class PopulationSet(object):
  def __init__(self):
    self.binaryString = ['', ''];
    #Changed to a pair to allow for x and y.
    self.fitness = None;

populationSet = [PopulationSet() for _ in range(POPULATION_SIZE)];
BESTINDIVIDUAL = PopulationSet();

def binToSignedNumber(binary):
  if (binary[0] == "1"):
    return int(binary[1:], 2);
  else:
    return int("-" + binary[1:], 2);
  #Converts binary to signed Integer.

def evaluate(individual):
  global BESTINDIVIDUAL

  x = binToSignedNumber(individual.binaryString[0]);
  y = binToSignedNumber(individual.binaryString[1]);

  individual.fitness = (0.26 * ((x**2)+(y**2))) - (0.48 * x * y);
  #New fitness function.

  if ((BESTINDIVIDUAL.fitness is None) or individual.fitness < BESTINDIVIDUAL.fitness):
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
    for key in range(len(population.binaryString)):
      population.binaryString[key] = "";
      for i in range(CONDITION_LENGTH):
        population.binaryString[key] += str(randrange(2));
    evaluate(population);
    #Creates and evalutates the population.

def tournamentSelection(numberOfTimes):
    children = [None, None];

    for child in range(len(children)):
      for i in range(numberOfTimes):
        individual = populationSet[randrange(POPULATION_SIZE)];
        if (children[child] is None) or individual.fitness < children[child].fitness:
          children[child] = copy.copy(individual);
    return children;
    #Tournament selection changed to favour low fitness.

def onePointCrossover(parents):
  children = [PopulationSet(), PopulationSet()];

  children[0].binaryString = parents[0].binaryString;
  children[1].binaryString = parents[1].binaryString;
  crossoverNum = randint(1, ((CONDITION_LENGTH * len(children)) - 1));
  #Crossover point now between 1 and total length of children.

  childCrossover0 = children[0].binaryString[0] + children[0].binaryString[1];
  childCrossover1 = children[0].binaryString[1] + children[0].binaryString[1];
  #Adds together both binary strings in the pair.

  childCrossoverDone0 = childCrossover0[:crossoverNum] + childCrossover1[crossoverNum:];
  childCrossoverDone1 = childCrossover1[:crossoverNum] + childCrossover0[crossoverNum:];
  #Initialises crossover.

  children[0].binaryString[0] = childCrossoverDone0[:CONDITION_LENGTH];
  children[0].binaryString[1] = childCrossoverDone0[CONDITION_LENGTH:];
  #Finishes crossover of first child.

  children[1].binaryString[0] = childCrossoverDone1[:CONDITION_LENGTH];
  children[1].binaryString[1] = childCrossoverDone1[CONDITION_LENGTH:];
  #Finishes crossover of second child.

  return children;

def mutation(parents):
  children = [PopulationSet(), PopulationSet()];

  children[0].binaryString = parents[0].binaryString;
  children[1].binaryString = parents[1].binaryString;
  #Initialises mutation.

  for child in range(len(children)):
    concatString = "";
    for binaryPair in children[child].binaryString[:]:
      for binary in binaryPair[:]:
        if 0.1 < random() < (0.1 + MUTATION_RATE):
          concatString += str(1 - int(binary));
        else:
          concatString += binary
      binary = concatString;
      #Bitwise mutation.
  return children;


def main():
  global populationSet;

  createPopulation();
  generation = 1;

  print("Generation: " + str(generation));
  print("Best Solution is: " + str(BESTINDIVIDUAL.binaryString[0]) + ", " + str(BESTINDIVIDUAL.binaryString[1]));
  print("Lowest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");

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
    populationSet.sort(key=lambda x: x.fitness)
	#Adds together previous and child population, then sorts them.

    for i in range(POPULATION_SIZE):
      populationSet.pop();
	#Pops the bottom half of the stack.

    for i in populationSet[:]:
      print(i.fitness);

    #Print after generation
    print("Generation: " + str(generation));
    print("Best Solution is: " + str(BESTINDIVIDUAL.binaryString[0]) + ", " + str(BESTINDIVIDUAL.binaryString[1]));
    print("Lowest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");
	
	
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print "Didn't find the best solution"
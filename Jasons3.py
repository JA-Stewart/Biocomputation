import random
import copy

POPULATION_SIZE = 10;
MUTATION_RATE = 0.025;
HIGHEST_VALUE = 5.12;

TOTAL_GENERATION = 20;

class PopulationSet(object):
  def __init__(self):
    self.realNumber = 0.0;
    self.fitness = None;

populationSet = [PopulationSet() for _ in range(POPULATION_SIZE)];
BESTINDIVIDUAL = PopulationSet();

def evaluate(individual):
  global BESTINDIVIDUAL

  individual.fitness = (individual.realNumber ** 2);
  print(individual.fitness)
  #X squared fitness function
  
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
    population.realNumber = round(random.uniform(-HIGHEST_VALUE, HIGHEST_VALUE), 2);
    evaluate(population);
  #Creates and evalutates the population.

def tournamentSelection(numberOfTimes):
    children = [None, None];

    for child in range(len(children)):
      for i in range(numberOfTimes):
        individual = populationSet[random.randrange(POPULATION_SIZE)];
        if (children[child] is None) or individual.fitness < children[child].fitness:
          children[child] = copy.copy(individual);
    return children;
  #Tournament selection that favours low fitness.

def crossoverBlend(parents):
  children = [PopulationSet(), PopulationSet()];

  parent1 = parents[0].realNumber;
  parent2 = parents[1].realNumber;
  #Initialises crossover
  
  for child in range (len(children)):
    childrenInvalid = True
    while childrenInvalid:
      gamma = random.uniform(0, 0.25)
      children[0].realNumber = parent1 - gamma *(parent1 - parent2)
      children[1].realNumber = parent2 + gamma *(parent1 - parent2)
      #Checks if number is within limits or repeats process.
      if (children[0].realNumber < 5.12 and children[0].realNumber >-5.12
      and children[1].realNumber < 5.12 and children[1].realNumber >-5.12):
        childrenInvalid = False
    
  return children;

def mutation(parents):
  children = [PopulationSet(), PopulationSet()];

  children[0].realNumber = parents[0].realNumber;
  children[1].realNumber = parents[1].realNumber;
  #Initialises mutation.

  for child in range(len(children)):    
    if 0.1 < random.random() < (0.1 + MUTATION_RATE):
      #Performs mutation within smaller boundaries
      if (children[child].realNumber > 5.02):
        children[child].realNumber +=round(random.uniform(-0.1, 0.0), 2)
      
      elif (children[child].realNumber < -5.02):
        children[child].realNumber +=round(random.uniform(0.0, 0.1), 2)
      #Performs mutation without boundaries
      else:
        children[child].realNumber +=round(random.uniform(-0.1, 0.1), 2)
        
  #Random stepwise mutation.
  
  return children;


def main():
  global populationSet;

  createPopulation();
  generation = 1;

  for i in populationSet[:]:
    print(i.realNumber);

  print("Generation: " + str(generation));
  print("Best Solution is: " + str(BESTINDIVIDUAL.realNumber));
  print("Lowest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");

  while (generation < TOTAL_GENERATION):
    generation += 1;

    #Create child Population
    child_population = [];
    while len(child_population) < POPULATION_SIZE:
      selectParents = tournamentSelection(2);
      newChildren = crossoverBlend(selectParents);
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

    #Print after generation
    print("Generation: " + str(generation));
    print("Best Solution is: " + repr(BESTINDIVIDUAL.realNumber));
    print("Lowest Fitness is: " + str(BESTINDIVIDUAL.fitness) +"\n");
  
  
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print "Didn't find the best solution"

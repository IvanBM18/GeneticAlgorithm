from random import choices, randint, random
from typing import List, Tuple

GENOME_LENGTH = 7
#Genetic Representation of a solution
Genome = List[int] #Ex: [0000000,1010101], where 0000000 is 5.04 and 1111111 is 5.12
Population = List[Genome]

#Generate a random genome
def generateGenome() -> Genome:
    return choices([0,1],k=GENOME_LENGTH)

#Generates a population of genomes
def generatPopulation(size:int) -> Population:
    return [generateGenome() for _ in range(size)]

#Genome to decimal
def genomeToDecimal(genome:Genome) -> float:
    return (int(''.join(map(str,genome)),2) * 0.08) - 5.04
    

#Fitness function, evaluates the genome based of the sphere function
def fitness(genome:Genome) -> float:
    return genomeToDecimal(genome)**2

#Selects the best genome from a population
def selectBest(population:Population) -> Population:
    return choices(
        population= population,
        weights= [fitness(genome) for genome in population],
        k=2 #Selects 2 genomes
    )

#Generates two new Genomes from two parents
def singlePointCrossOver(parent1:Genome, parent2:Genome) -> Tuple[Genome,Genome]:
    if(len(parent1) != len(parent2)):
        raise Exception("Parents must be of the same length")
    #If parents are to short to create a new genome
    if(len(parent1) < 2):
        return parent1,parent2
    #Selects a random point to cross over
    crossOverPoint = randint(0,GENOME_LENGTH-1)
    #Crosses over the genomes
    return parent1[0:crossOverPoint] + parent2[crossOverPoint:], parent2[0:crossOverPoint] + parent1[crossOverPoint:]

#Mutation Function
def mutation(genome:Genome) -> Genome:
    #Selects a random index to mutate
    mutationIndex = randint(0,GENOME_LENGTH-1)
    #Mutates the genome
    genome[mutationIndex] = genome[mutationIndex] if random() > 0.5 else abs(genome[mutationIndex]-1)
    return genome

#Main Function
def runEvolution(generationLimit : int):
    population = generatPopulation(50)
    
    for i in range(generationLimit):
        population = sorted(population, key= lambda genome: fitness(genome ), reverse=True)
        #Gets the minimum fitness
        if(fitness(population[0]) == 0):
            print(f"Generation {i} x = {genomeToDecimal(population[0])}, f(x) = {fitness(population[0])}")
            break
        #Gets the maximum fitness
        if(fitness(population[0]) >= 5.12**2):
            print(f"Generation {i} x = {genomeToDecimal(population[0])}, f(x) = {fitness(population[0])}")
            break
        #Selects the best genomes
        nextGeneration = population[0:2]
        #Creates the next generation
        for j in range(int(len(population) / 2) -1):
            parents = selectBest(population)
            son1, son2 = singlePointCrossOver(parents[0],parents[1])
            
            #Apply Mutation to the sons
            son1 = mutation(son1)
            son2 = mutation(son2)
            
            nextGeneration += [son1,son2]
        #Replaces the old genomes with the new ones
        population = nextGeneration
        
    population = sorted(population, key= lambda genome: fitness(genome), reverse=True)
    return population[0]
        
generations = int(input("Ingrese el numero máximo de Generación: "))
bestSolution = runEvolution(generations)
# print(f"Best Solution: {genomeToDecimal(bestSolution)} eval: {fitness(bestSolution)}")
from random import choices, randint
from typing import List, Tuple

GENOME_LENGTH = 7
GENERATION_LIMIT = 100
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
    genome[mutationIndex] = genome[mutationIndex] if genome[mutationIndex] == 0 else abs(genome[mutationIndex]-1)
    return genome

#Main Function
def runEvolution():
    population = generatPopulation(8)
    
    for i in range(GENERATION_LIMIT):
        #Selects the best genomes
        best = selectBest(population)
        #Crosses over the genomes
        child1,child2 = singlePointCrossOver(best[0],best[1])
        #Mutates the genomes
        child1 = mutation(child1)
        child2 = mutation(child2)
        #Replaces the worst genomes with the new ones
        population = population[:-2] + [child1,child2]
        #Prints the best genome of the current generation
        print(f"Generation {i} Best: {genomeToDecimal(selectBest(population)[0])}")
        
runEvolution()
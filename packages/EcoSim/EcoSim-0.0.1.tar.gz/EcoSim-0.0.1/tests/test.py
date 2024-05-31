from ecosim import Climate, AnimalPopulation, PlantDistribution, Ecosystem, PredatorPreyPopulation, plot_simulation

def main():
    climate = Climate(initial_temperature=15.0, temperature_variability=1.0, initial_precipitation=100.0, precipitation_variability=10.0)
    animal_population = AnimalPopulation(initial_population=100, birth_rate=0.1, death_rate=0.05, migration_rate=0.01)
    plant_distribution = PlantDistribution(initial_distribution=1000, spread_rate=50, competition_factor=0.01)
    predator_prey_population = PredatorPreyPopulation(prey_population=500, predator_population=50, prey_birth_rate=0.2, predator_birth_rate=0.1, predation_rate=0.01, predator_death_rate=0.05)

    ecosystem = Ecosystem(climate, animal_population, plant_distribution, predator_prey_population)

    data = {
        'Temperature': [],
        'Precipitation': [],
        'Animal Population': [],
        'Plant Distribution': [],
        'Prey Population': [],
        'Predator Population': []
    }

    for year in range(50):
        ecosystem.simulate_year()
        data['Temperature'].append(climate.temperature)
        data['Precipitation'].append(climate.precipitation)
        data['Animal Population'].append(animal_population.population)
        data['Plant Distribution'].append(plant_distribution.distribution)
        data['Prey Population'].append(predator_prey_population.prey_population)
        data['Predator Population'].append(predator_prey_population.predator_population)
    
    plot_simulation(data, 'Ecosystem Simulation Over 50 Years').show()

if __name__ == '__main__':
    main()

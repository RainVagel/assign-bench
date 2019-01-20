import graph as grp
from car_generator import CarGenerator
from passenger import create_passenger
from min_cost_flow import MinCostFlowNetwork
import time

PASSENGER_INTERVAL = 10
DIAMETER_CONSTANT = 1.5
PASSENGER_ID = 0


def try_testing():
    graph = grp.read_graph("graph.json")
    node_id_node = grp.node_id_to_node(graph)
    id_node = grp.node_to_node_id(graph)

    car_gen = CarGenerator(graph)
    generated_cars = car_gen.generate_cars(3, node_id_node, graph)

    #print(car_gen.generated_cars)

    # Generate a car and a passenger
    test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
    test_passenger = create_passenger(1, graph, 10)

    while test_car.location == test_passenger.location:
        test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
        test_passenger = create_passenger(1, graph, 10)

    print(car_gen.generated_cars)
    print(test_passenger)

    dist, prev = grp.dijkstra(graph, node_id_node, test_car.location, test_passenger.location)

    path_to_destination = grp.path_to_target(prev, test_passenger.location)
    # Car - go to passenger location
    #test_car.set_path(path_to_passenger)
    test_car.start_task(test_passenger)
    print(list(reversed(test_car.path)))

    test_car.movement()
    # Testi, kui auto ja vend spawnivad samas kohas


def passenger_generator(graph, ticker, diameter, waiting_passengers):
    global PASSENGER_INTERVAL, PASSENGER_ID
    if ticker % PASSENGER_INTERVAL == 0:
        waiting_passengers[PASSENGER_ID] = create_passenger(PASSENGER_ID, graph, diameter)
        PASSENGER_ID += 1
    # After every 100 passengers created, increase the speed at which new passengers are created
    if PASSENGER_ID % 100 == 0:
        PASSENGER_INTERVAL -= 1
    return waiting_passengers


def simulate(input_graph, nr_of_cars):
    graph = grp.read_graph(input_graph)
    node_id_node = grp.node_id_to_node(graph)
    id_node = grp.node_to_node_id(graph)
    
    free_cars = {}
    driving_cars = {}
    waiting_passengers = {}
    picked_up_passengers = {}

    avg_wait = []
    passenger_nr_statistics = []
    
    car_generator = CarGenerator(graph)
    generated_cars = car_generator.generate_cars(nr_of_cars, node_id_node, graph)

    for car in generated_cars:
        free_cars[car.id] = car
    
    global PASSENGER_INTERVAL, DIAMETER_CONSTANT
    diam = grp.get_diameter(graph) * DIAMETER_CONSTANT
    ticker = 0
    # while True is only for testing purpouses. Eventually will be handled by SimulatorManager
    while ticker < 20:
        waiting_passengers = passenger_generator(graph, ticker, diam, waiting_passengers)
        print("After passenger creation:", waiting_passengers)
        print("Passenger nr after creation:", len(waiting_passengers))

        # Moves all of the cars
        for car in driving_cars.values():
            car.movement()

        # Taking down the waiting time from all of the passengers in the waiting list.
        # If one of them reaches 0 waiting time, then remove him from the list since he has waited too long
        for passenger_key in waiting_passengers.keys():
            if waiting_passengers[passenger_key].time_movement():
                waiting_passengers.remove(passenger_key)

        print("After passengers waited:", waiting_passengers)
        # Collect waiting passengers avg_waiting time if total nr of passengers is divisible by 100
        if PASSENGER_ID % 10 == 0:
            total_time = 0
            for passenger_key in waiting_passengers.keys():
                total_time += waiting_passengers[passenger_key].time_waited
            passenger_nr_statistics.append(PASSENGER_ID)
            avg_wait.append(total_time / len(waiting_passengers.keys()))
        # print(waiting_passengers)
        print("Statisics time", avg_wait)
        print("Passenger nr", passenger_nr_statistics)

        # Start assignment procedure
        if len(free_cars.keys()) > 0 and len(waiting_passengers) > 0:
            # Create flow network to get assignments for taxis
            network = MinCostFlowNetwork(graph, free_cars.values(), waiting_passengers.values())
            assignments = network.get_assignment()

            for assignment in assignments:
                car = free_cars[assignment[0]] # Car object
                del free_cars[car.id]
                passenger = waiting_passengers[assignment[1]] # Passenger object
                del waiting_passengers[passenger.id]
                car.start_task(passenger)
                driving_cars[car.id] = car
                picked_up_passengers[passenger.id] = passenger
            print("Assingment done")
            print("Free cars", free_cars)
            print("Waiting passengers", waiting_passengers)
            print("Driving cars", driving_cars)
            print("Picked passengers", picked_up_passengers)

        time.sleep(1)
        ticker += 1

if __name__=="__main__":
    simulate("graph.json", 5)

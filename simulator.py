import graph as grp
from car_generator import CarGenerator
from passenger import create_passenger
from min_cost_flow import MinCostFlowNetwork
from min_cost_flow_priority import MinCostFlowPriorityNetwork
from plot import Plot
import time
from tqdm import tqdm


PASSENGER_INTERVAL = 10
DIAMETER_CONSTANT = 1.5
PASSENGER_ID = 0


def try_testing():
    graph = grp.read_graph("graph.json")
    node_id_node = grp.node_id_to_node(graph)
    id_node = grp.node_to_node_id(graph)

    car_gen = CarGenerator(graph)
    generated_cars = car_gen.generate_cars(3, node_id_node, graph)

    # print(car_gen.generated_cars)

    # Generate a car and a passenger
    test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
    test_passenger = create_passenger(1, graph, 10)

    while test_car.location == test_passenger.location:
        test_car = car_gen.generate_cars(1, node_id_node, graph)[0]
        test_passenger = create_passenger(1, graph, 10)

    # print(car_gen.generated_cars)
    # print(test_passenger)

    dist, prev = grp.dijkstra(graph, node_id_node, test_car.location, test_passenger.location)

    path_to_destination = grp.path_to_target(prev, test_passenger.location)
    # Car - go to passenger location
    # test_car.set_path(path_to_passenger)
    test_car.start_task(test_passenger)
    # print(list(reversed(test_car.path)))

    test_car.movement()
    # Testi, kui auto ja vend spawnivad samas kohas


def passenger_generator(graph, ticker, diameter, waiting_passengers):
    global PASSENGER_INTERVAL, PASSENGER_ID
    if PASSENGER_INTERVAL == 0:
        waiting_passengers[PASSENGER_ID] = create_passenger(PASSENGER_ID, graph, diameter)
        PASSENGER_ID += 1
    elif ticker % PASSENGER_INTERVAL == 0:
        waiting_passengers[PASSENGER_ID] = create_passenger(PASSENGER_ID, graph, diameter)
        PASSENGER_ID += 1
    # After every 100 passengers created, increase the speed at which new passengers are created
    if PASSENGER_ID % 100 == 0:
        if PASSENGER_INTERVAL != 0:
            PASSENGER_INTERVAL -= 1
    return waiting_passengers


def passenger_deleter(deletion_dict, delete_from_dict):
    for passenger in deletion_dict.values():
        del delete_from_dict[passenger.id]

    deletion_dict.clear()
    return deletion_dict, delete_from_dict


def simulate(input_graph, nr_of_cars, assignment_algorithm):
    graph = grp.read_graph(input_graph)
    node_id_node = grp.node_id_to_node(graph)
    id_node = grp.node_to_node_id(graph)
    
    free_cars = {}
    driving_cars = {}
    waiting_passengers = {}
    picked_up_passengers = {}
    assigned_passengers = {}
    cars_to_move = {}
    passengers_to_delete = {}
    pass_thrown_away = 0
    succ_pass = 0
    checker = 0
    car_number = []

    avg_wait = []
    passenger_nr_statistics = []
    pass_thrown_away_list = []
    
    car_generator = CarGenerator(graph)
    generated_cars = car_generator.generate_cars(nr_of_cars, node_id_node, graph)

    for car in generated_cars:
        free_cars[car.id] = car
    
    global PASSENGER_INTERVAL, DIAMETER_CONSTANT, PASSENGER_ID
    PASSENGER_ID = 0
    PASSENGER_INTERVAL = 10

    diam = grp.get_diameter(graph) * DIAMETER_CONSTANT
    #ticker = 0
    thrown_away_pass_counter = 0
    # while True is only for testing purpouses. Eventually will be handled by SimulatorManager
    for ticker in tqdm(range(1000)):
        waiting_passengers = passenger_generator(graph, ticker, diam, waiting_passengers)
        # print("After passenger creation:", waiting_passengers)
        # print("Passenger nr after creation:", len(waiting_passengers))

        # Moves all of the cars
        for car in driving_cars.values():
            car.movement()

        # Move passengers from assigned to picked up if they are picked up.
        for passenger in assigned_passengers.values():
            if passenger.on_car:
                picked_up_passengers[passenger.id] = passenger
                passengers_to_delete[passenger.id] = passenger

        passengers_to_delete, assigned_passengers = passenger_deleter(passengers_to_delete, assigned_passengers)

        # Deletes any passenger who has reached his destination and has been dropped off by the car
        for passenger in picked_up_passengers.values():
            if passenger.location == passenger.destination and passenger.on_car is False:
                passengers_to_delete[passenger.id] = passenger
                succ_pass += 1

        passengers_to_delete, picked_up_passengers = passenger_deleter(passengers_to_delete, picked_up_passengers)

        # If car path is None, it is not moving anywhere and does not have a passenger, but did drive before
        # Then it will be deleted from the driving_cars dictionary and moved to the free_cars dictionary
        # so that it can be assigned again
        for car in driving_cars.values():
            if car.path is None and car.moving_to is None and car.passenger is None:
                cars_to_move[car.id] = car

        # Helper loop to move cars between lists
        for car in cars_to_move.values():
            free_cars[car.id] = car
            del driving_cars[car.id]

        cars_to_move.clear()

        # Taking down the waiting time from all of the passengers in the waiting list.
        # If one of them reaches 0 waiting time, then remove him from the list since he has waited too long
        for passenger_key in waiting_passengers.keys():
            if waiting_passengers[passenger_key].time_movement():
                passengers_to_delete[passenger_key] = waiting_passengers[passenger_key]
                pass_thrown_away += 1
                # thrown_away_pass_counter += 1
                # if thrown_away_pass_counter == 5:
                #     generated_cars = car_generator.generate_cars(1, node_id_node, graph)
                #     thrown_away_pass_counter = 0
                #
                #     for car in generated_cars:
                #         free_cars[car.id] = car

        passengers_to_delete, waiting_passengers = passenger_deleter(passengers_to_delete, waiting_passengers)

        # Taking down waiting time from passengers who have been assigned to some car. If waiting_time goes 0 or below
        # then they will be removed.
        # for passenger in assigned_passengers.values():
        #     if assigned_passengers[passenger.id].time_movement():
        #         passengers_to_delete[passenger.id] = passenger
        #         pass_thrown_away += 1

        # If a passenger's wait time is <0, then remove a passenger from that car and make the
        # car available to be assigned.
        # for car in driving_cars.values():
        #     if car.passenger in passengers_to_delete.values():
        #         car.path = None
        #         car.moving_to = None
        #         car.passenger = None
        #         car.picked_up = False
        #         cars_to_move[car.id] = car
        #
        # for car in cars_to_move.values():
        #     free_cars[car.id] = car
        #     del driving_cars[car.id]
        #
        # cars_to_move.clear()
        # passengers_to_delete, assigned_passengers = passenger_deleter(passengers_to_delete, assigned_passengers)

        # print("After passengers waited:", waiting_passengers)
        # Collect waiting passengers avg_waiting time if total nr of passengers is divisible by 100
        if PASSENGER_ID % 10 == 0 and PASSENGER_ID != checker:
            total_time = 0
            car_number.append(len(driving_cars) + len(free_cars))
            checker = PASSENGER_ID
            pass_thrown_away_list.append(pass_thrown_away)
            pass_thrown_away = 0
            for passenger_key in waiting_passengers.keys():
                total_time += waiting_passengers[passenger_key].time_waited
            for passenger in assigned_passengers.values():
                total_time += assigned_passengers[passenger.id].time_waited
            passenger_nr_statistics.append(PASSENGER_ID)
            if len(waiting_passengers.keys()) + len(assigned_passengers.keys()) == 0:
                avg_wait.append(total_time / (len(waiting_passengers.keys()) + len(assigned_passengers.keys()) + 1))
            else:
                avg_wait.append(total_time / (len(waiting_passengers.keys()) + len(assigned_passengers.keys())))
        # print("Statisics time", avg_wait)
        # print("Passenger nr", passenger_nr_statistics)

        # Start assignment procedure
        if len(free_cars.keys()) > 0 and len(waiting_passengers) > 0:
            # Create flow network to get assignments for taxis
            # network = MinCostFlowNetwork(graph, free_cars.values(), waiting_passengers.values())
            #print(graph)
            #print(assignment_algorithm)
            assingment_object = assignment_algorithm(graph, list(free_cars.values()), list(waiting_passengers.values()))
            assignments = assingment_object.get_assignment()

            for assignment in assignments:
                car = free_cars[assignment[0]]  # Car object
                del free_cars[car.id]
                passenger = waiting_passengers[assignment[1]]  # Passenger object
                del waiting_passengers[passenger.id]
                assigned_passengers[passenger.id] = passenger
                car.start_task(passenger)
                driving_cars[car.id] = car
        #     print("Assingment done")
        # print("Free cars", free_cars)
        # print("Waiting passengers", waiting_passengers)
        # print("Driving cars", driving_cars)
        # print("Picked passengers", picked_up_passengers)
        # print("Assigned passengers", assigned_passengers)

        # time.sleep(5)
        #ticker += 1
    # print(avg_wait)
    # print(passenger_nr_statistics)
    # print(PASSENGER_ID)
    # print("Thrown away:", pass_thrown_away)
    # print("Success:", succ_pass)
    # print(pass_thrown_away_list)
    # new_wait = []
    # new_nr_statistics = []
    # avg_thrown = []
    # prev = passenger_nr_statistics[0]
    # temp_time = []
    # temp_thrown = []
    # for i in range(0, len(avg_wait)):
    #     if passenger_nr_statistics[i] != prev:
    #         new_wait.append(sum(temp_time) / len(temp_time))
    #         temp_time.clear()
    #         avg_thrown.append(sum(temp_thrown) / len(temp_thrown))
    #         temp_thrown.clear()
    #         new_nr_statistics.append(prev)
    #         prev = passenger_nr_statistics[i]
    #     else:
    #         temp_time.append(avg_wait[i])
    #         temp_thrown.append(pass_thrown_away_list[i])
    # new_wait.append(sum(temp_time) / len(temp_time))
    # avg_thrown.append(sum(temp_thrown) / len(temp_thrown))
    # new_nr_statistics.append(prev)
    # print(new_wait)
    # print(new_nr_statistics)
    # print(avg_thrown)
#    print("Amount of taxis:", str(len(free_cars) + len(driving_cars)))
    return avg_wait, passenger_nr_statistics, pass_thrown_away_list

def start_simulate(nr_of_cars, graph="graph", algorithm=MinCostFlowNetwork, algorithm_name="Network Flow"): # TODO
    if (algorithm == MinCostFlowNetwork):
        main(nr_of_cars)
    else:
        print("Starting algorithm")
        avg_wait, passenger_nr_statistics, pass_thrown_away_list = simulate(graph, nr_of_cars, algorithm)
        print("Algorithm finished")
        plot = Plot([passenger_nr_statistics], [pass_thrown_away_list])
        legend = [algorithm_name,] 
        x_label = "Nr of passenger"
        y_label = "Nr of cancelled orders"
        plot.create_line_plot(x_label, y_label, legend, title="Cancelled orders over time")
        plot_2 = Plot([passenger_nr_statistics], [avg_wait])
        plot_2.create_line_plot("Nr of passenger", "Average waiting time", legend, title="Average waiting time per passenger")
        print("Plots have been saved to the working directory.")

def main(nr_of_cars):
    print("Starting algorithms")
    avg_wait, passenger_nr_statistics, pass_thrown_away_list = simulate("graph", nr_of_cars, MinCostFlowNetwork)
    avg_wait_prior, passenger_nr_statistics_prior, pass_thrown_away_list_prior =  simulate("graph", nr_of_cars, MinCostFlowPriorityNetwork)
    print("Algorithms finished")
    plot = Plot([passenger_nr_statistics, passenger_nr_statistics_prior],
                [pass_thrown_away_list, pass_thrown_away_list_prior])
    legend = ["Network flow", "Priority network flow"]
    x_label = "Nr of passenger"
    y_label = "Nr of cancelled orders"
    plot.create_line_plot(x_label, y_label, legend, title="Cancelled orders over time")
    plot_2 = Plot([passenger_nr_statistics, passenger_nr_statistics_prior],
                [avg_wait, avg_wait_prior])
    plot_2.create_line_plot("Nr of passenger", "Average waiting time", legend, title="Average waiting time per passenger")
    print("Plots have been saved to the working directory.")

if __name__ == "__main__":
    main()

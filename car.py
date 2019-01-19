from graph import node_id_to_node, dijkstra, path_to_target

class Car:
    """
    :param self.path Queue, which houses tuples of type (node, time)
    :param self.location Current node. If moving between nodes a - b, then it is a.
    :param self.time_till_next How much time it still has no move before getting to the next node
    """

    # Not sure if the self.passenger value should be a Boolean or house the passenger object itself

    def __init__(self, location, new_id, node_ids, graph):
        self.id = new_id
        self.location = location # Location is a node
        self.time_till_next = 0
        self.moving_to = None # Should also be a node
        self.passenger = None
        self.path = None
        self.picked_up = False
        self.node_ids = node_ids
        self.graph = graph

    def decrease_time(self):
        self.time_till_next -= 1

    def set_time(self, time):
        self.time_till_next = time

    def set_moving_to(self, dest):
        self.moving_to = dest

    def movement(self):
        if self.time_till_next == 0 and self.path is None:
            pass
        elif self.time_till_next == 0 and self.path is not None:
            # If car is at moving_to node and doesn't have a passenger,
            # then it as the passengers locations and should pick him up
            if self.moving_to is not None and self.picked_up == False \
                    and self.moving_to.id_nr == self.passenger.starting_location.id_nr:
                self.pick_up_passenger()
            if len(self.path) != 0: 
                if self.moving_to != None: # Updating current location to arrived location
                    self.location = self.moving_to
                    if self.picked_up: # Also updating passengers location
                        self.passenger.set_location(self.moving_to)
                next_node = self.path.pop()
                next_node = self.node_ids[next_node]
                time_to_node = self.find_time_to_next_node(next_node)
                self.set_time(time_to_node)
                self.set_moving_to(next_node)
                #if self.picked_up:
                   # self.passenger.set_location(self.location)
            else:
                self.path = None
                self.location = self.moving_to
                if self.picked_up:
                    self.put_down_passenger()
                self.moving_to = None
                self.passenger = None
                self.picked_up = False

        else:
            self.decrease_time()
        # print("Debug, moving to: " + str(self.moving_to) + ", time left: " + str(self.time_till_next))
        # if len(self.path) > 0:
        #     print("Debug, path: " + str(list(reversed(self.path))))
    
    def set_path(self, path):
        self.path = list(reversed(path))
        
    def find_time_to_next_node(self, dest):
        lst = self.location.adj_list
        for pair in lst:
            if pair[0] == dest.id_nr:
                return pair[1]
            
    def start_task(self, passenger):
        if passenger.starting_location.id_nr == self.location.id_nr:
            self.passenger = passenger
            self.pick_up_passenger()
        else:
            _, prev = dijkstra(self.graph, self.node_ids, self.location, passenger.location)
            path_to_passenger = path_to_target(prev, self.node_ids, self.location, passenger.location)
            self.passenger = passenger
            self.set_path(path_to_passenger)
    
    def pick_up_passenger(self):
        print("Picking up passenger")
        self.picked_up = True
        self.passenger.set_on_car(True)
        
        # when picking up, set new path
        self.location = self.passenger.starting_location
        
        _, prev = dijkstra(self.graph, self.node_ids, self.passenger.starting_location, self.passenger.destination)
        path_to_destination = path_to_target(prev, self.node_ids,
                                             self.passenger.starting_location, self.passenger.destination)
        self.set_path(path_to_destination)
        
        # When picking up, passenger should be removed from node
#         Missing the necessary methods to find out the path to passengers destination# -*- coding: utf-8 -*- 
        
    def put_down_passenger(self):
        self.passenger.set_on_car(False)
        self.passenger.location = self.location
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()


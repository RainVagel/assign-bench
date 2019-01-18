class Car:
    """
    :param self.path Queue, which houses tuples of type (node, time)
    :param self.location Current node. If moving between nodes a - b, then it is a.
    :param self.time_till_next How much time it still has no move before getting to the next node
    """

    # Not sure if the self.passenger value should be a Boolean or house the passenger object itself

    def __init__(self, location, new_id):
        self.id = new_id
        self.location = location
        self.time_till_next = 0
        self.moving_to = None
        self.passenger = False
        self.path = None

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
            if len(self.path) != 0:
                next_node = self.path.pop()
                print(next_node)
                self.set_time(next_node[1])
                self.set_moving_to(next_node[0])
            else:
                self.path = None
                self.location = self.moving_to
                self.moving_to = None
        else:
            self.decrease_time()

    def pick_up_passenger(self):
        self.passenger = True
        self.location.remove_passenger()
#         Missing the necessary methods to find out the path to passengers destination# -*- coding: utf-8 -*-
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()


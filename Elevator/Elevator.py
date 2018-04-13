import threading
import time


class Elevator:
    __direction = "S"  # posible states are S = STILL, D = DOWN, U = UP
    __actual_floor = 1
    __array_floors = []
    __idElevator = 0

    def __init__(self, id):
        self.__idElevator = id
        self.__direction = "S"  # posible states are S = STILL, D = DOWN, U = UP
        self.__actual_floor = 1
        self.__array_floors = []
        self.__to_floor = 1

    def distance_request(self, direction, floor):
        '''
        :param direction: Get the direction requested, can be "U" for UP or "D" for DOWN
        :param floor: Get the floor of the destination
        :return: the distance between the elevator steps an a request
        '''
        if (self.__direction == "S" or self.__direction == direction):
            return self.__idElevator, abs(floor - self.__actual_floor)
        if (self.__direction == "U"):
            max_floor = max(self.__array_floors)
            # Distance from actual floor to the max floor      distance from max floor to floor from request
            return (max_floor - self.__actual_floor) + abs(max_floor - floor)

        # If the direction are different and the actual direction is down
        min_floor = min(self.__array_floors)
        # Distance from actual floor to the min floor       distance from min floor to request floor
        return (self.__actual_floor - min_floor) + abs(min_floor - floor)


    def __insert_order_request(self, direction, floor):
        '''
        :param direction: The direction of the request UP or DOWN
        :param floor: The number of floor of the request
        :return: insert the request in the queue
        '''
        distante_to_request = self.distance_request(direction, floor)
        for i in range(self.__array_floors):
            distance_request_i = self.distance_request(self.__direction, self.__array_floors[i])
            if distance_request_i > distante_to_request:
                break

        if i == 0:
            self.__to_floor = floor
            self.__array_floors = [floor] + self.__array_floors
        else:
            left_array = self.__array_floors[:i]
            right_array = self.__array_floors[i:]
            left_array.append(floor)
            self.__array_floors = left_array + right_array

    def assing_request(self, direction, floor):
        self.__insert_order_request(direction, floor)

    def __get_direction(self):
        if self.__direction == "S":
            return "STILL"
        if self.__direction == "D":
            return "DOWN"
        return "UP"

    def __move_elevator(self):
        '''
        This function move the elevator
        :return:
        '''
        if self.__direction == "S":
            #If we moving or wating
            if len(self.__array_floors) > 0:
                #If there are something in the queue
                self.__dispatch_next()
            elif self.__actual_floor > 1:
                #If we are wating, the queue is empty and the actual floor is bigger than 1
                self.__actual_floor -= 1
        elif self.__to_floor == self.__actual_floor:
            #If we are in the objective floor we took another from the queue
            self.__dispatch_next()
        elif self.__actual_floor < self.__to_floor:
            #If the actual floor is smaller that the objective floor we move up and add one floor to the elevator
            self.__direction = "U"
            self.__actual_floor += 1
        else:
            #If the actual floor if greater than the objective floor we move down and rest one floor to the elevator
            self.__direction = "D"
            self.__actual_floor -= 1

    def __dispatch_next(self):
        '''
        This Function dispatch the next element in the queue, if the queue is empty our objective is the floor 1
        '''
        if len(self.__array_floors) == 0:
            self.__to_floor = 1
            self.__direction = "S"
        else:
            self.__to_floor = self.__array_floors[0]
            del self.__array_floors[0]


    def start_working_elevator(self):
        '''
        This function start the thread of the elevator
        :return:
        '''
        while True:
            print "Elevator # " + str(self.__idElevator) + " actual floor: " + str(self.__actual_floor) + " going to floor: " + str(self.__to_floor) + " my direction is: " + self.__get_direction()
            self.__move_elevator()
            time.sleep(1)
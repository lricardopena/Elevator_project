import time
from Elevator import Elevator


el = Elevator.Elevator(1)

el.start()





print(el.distance_request("U", 3))

el.push_button_floor(3)

el.push_button_floor(4)

el.push_button_floor(6)



el.assing_request("D", 10)

time.sleep(3)

el.assing_request("D", 2)
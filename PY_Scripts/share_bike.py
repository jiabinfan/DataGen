from collections import defaultdict
import math
import csv
import os
import generate_tsp

depot_x = 34.275555
depot_y = 108.955555
FULL = "full"
INFINIT = 9999999
TRUCK_WEIGHT = 0

truckFull = 15

class Station:
    full_load = 20
    target_load = 10

    def __init__(self, id, num_b, x, y):
        self.id = id
        self.num_b = num_b
        self.x = x
        self.y = y

    def change(self, num_drop):
        self.num_b += num_drop

    def lessthan_target(self):
        if self.num_b < 0:
            return True

        elif 0 == self.num_b:
            return FULL

        else:
            return False

    def get_num_bikes(self):
        return self.num_b

    def get_pos(self):
        return (self.x, self.y)

    def get_id(self):
        return self.id

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Truck:
    full_load = truckFull

    def __init__(self, load, depot_x, depot_y):
        self.num_bikes = load
        self.x = depot_x
        self.y = depot_y

    def get_num_bikes(self):
        return self.num_bikes

    def change_bikes(self, val, station):
        self.num_bikes += val
        station.change(-val)

    def get_pos(self):
        return (self.x, self.y)

    def move_to(self, pos):
        self.x = pos[0]
        self.y = pos[1]


def getDistance(pos1, pos2):
    d = pow((pos1[0] - pos2[0]), 2) + pow((pos1[1] - pos2[1]), 2)
    return math.sqrt(d)


def get_tsp(stations, start):
    '''
    if len(stations) == 0:
        return tsp
    else:
        next_station = None
        dist = INFINIT
        for station in stations:
            if getDistance(station.get_pos(),start.get_pos())<dist:
                dist = getDistance(station.get_pos(),start.get_pos())
                next_station = station
        tsp.append(next_station)
        stations.remove(next_station)
        return generate_tsp(stations,next_station,tsp)
        '''
    stations.insert(0, start)
    coord_list = []
    for station in stations:
        each_coord = []
        each_coord.append(station.get_pos()[0])
        each_coord.append(station.get_pos()[1])
        coord_list.append(each_coord)

    tour_length, tour_path = generate_tsp.tsp(coord_list)
    tour_path.pop(-1)

    final_tour = []
    if tour_path[0] == 0:
        final_tour = tour_path.copy()
    else:
        tour_path.pop(-1)
        lenth = len(tour_path)
        index = tour_path.index(0)
        for i in range(0, lenth):
            next_i = (i + index) % lenth

            final_tour.append(tour_path[next_i])

        final_tour.append(0)

    # print(len(final_tour),final_tour)
    return final_tour


def set_vplus(edge_index, tsp):
    for i in range(edge_index, len(tsp)):
        if tsp[i].lessthan_target() == False:
            return tsp[i]
    return tsp[-1]


def set_vminus(edge_index, tsp):
    for i in range(0, len(tsp)):
        if tsp[i].lessthan_target() == True:
            return tsp[i]

    return tsp[-1]


def move_to_first_can_be_colletted(v_plus, tsp, truck, carbon, sum_distance):
    if Truck.full_load - truck.get_num_bikes() > (v_plus.get_num_bikes()):
        carbon += getDistance(truck.get_pos(), v_plus.get_pos()) * (TRUCK_WEIGHT + truck.get_num_bikes())
        sum_distance += getDistance(truck.get_pos(), v_plus.get_pos())
        # print("truck's position: ",pos_to_id(truck.get_pos(),tsp), " ", truck.get_num_bikes(), "sum distance so far: ",sum_distance, "sum carbonP: ", carbon)

        truck.move_to(v_plus.get_pos())
        truck.change_bikes(v_plus.get_num_bikes(), v_plus)

        return truck, carbon, sum_distance
    else:
        edge_index = get_index(tsp, v_plus)
        v_plus = set_vplus(edge_index + 1, tsp)
        return move_to_first_can_be_colletted(v_plus, tsp, truck, carbon, sum_distance)


def generate_data(path):
    # Driver code

    csvF = open(path, "r")
    reader = csv.reader(csvF)

    stations = []
    rows = []
    k = 1
    asum = 0
    for row in reader:
        # print(row)
        asum += int(row[2])
        station = Station(k, int(row[2]), float(row[0]), float(row[1]))
        k += 1
        stations.append(station)
        rows.append(row)
    # print(rows)
    return stations


def get_index(tsp, station):
    k = 0
    for i in tsp:

        if i.id == station.id:
            return k
        k += 1


def read_csv():
    csv_path = []
    for i in range(1, 27):
        path = data_path + str(i) + ".csv"
        csv_path.append(path)
    return csv_path


def generate_carbon(stations,extraNum):
    sum_x = 0
    sum_y = 0

    for station in stations:
        sum_x += station.x
        sum_y += station.y

    avg_x = sum_x / len(stations)
    avg_y = sum_y / len(stations)

    depot = Station(0, 0, depot_x, depot_y)

    carbon = 0
    edge_index = 0
    v_plus = None
    v_minus = None

    tsp_path = get_tsp(stations, depot)

    tsp = []
    for i in tsp_path:
        for station in stations:
            if station.id == i:
                tsp.append(station)

    num_b = 0
    sum_bikes = 0
    for i in tsp:
        sum_bikes += i.get_num_bikes()
        # print(i.id, i.get_num_bikes())

    # print("sum+bikes ",sum_bikes)
    tsp[-1].num_b = 0
    if sum_bikes >= 0:

        truck = Truck(0 + extraNum, depot_x, depot_y)
    else:
        truck = Truck(abs(sum_bikes) + extraNum, depot_x, depot_y)

    p = 0
    sum_distance = 0

    truck_pos = 9999
    while edge_index <= len(tsp) - 2 and p <= 35 and truck_pos != 0:
        p += 1
        v_plus = set_vplus(0, tsp)
        v_minus = set_vminus(edge_index, tsp)
        # print("v_minus id: ",v_minus.id)

        # print(sum_distance)
        if truck.get_num_bikes() >= abs(v_minus.get_num_bikes()):

            carbon += getDistance(truck.get_pos(), v_minus.get_pos()) * (TRUCK_WEIGHT + truck.get_num_bikes())
            sum_distance += getDistance(truck.get_pos(), v_minus.get_pos())

            if carbon > 2000:
                print(pos_to_id(truck.get_pos(), tsp), v_minus.id, getDistance(truck.get_pos(), v_minus.get_pos()))
                exit()
            # print("truck's position: ",pos_to_id(truck.get_pos(),tsp), " ", truck.get_num_bikes(), "sum distance so far: ",sum_distance, "sum carbonP: ", carbon)

            truck.move_to(v_minus.get_pos())
            truck.change_bikes(v_minus.get_num_bikes(), v_minus)

            edge_index = get_index(tsp, v_minus)
            # edge_index +=1

        elif get_index(tsp, v_minus) < get_index(tsp, v_plus) and truck.get_num_bikes() + v_plus.get_num_bikes() > abs(
                v_minus.get_num_bikes()):

            carbon += getDistance(truck.get_pos(), v_plus.get_pos()) * (TRUCK_WEIGHT + truck.get_num_bikes())
            sum_distance += getDistance(truck.get_pos(), v_plus.get_pos())
            # print("truck's position: ",pos_to_id(truck.get_pos(),tsp), " ", truck.get_num_bikes(), "sum distance so far: ",sum_distance, "sum carbonP: ", carbon)

            truck.move_to(v_plus.get_pos())
            truck.change_bikes(v_plus.get_num_bikes(), v_plus)

            carbon += getDistance(truck.get_pos(), v_minus.get_pos()) * (TRUCK_WEIGHT + truck.get_num_bikes())
            sum_distance += getDistance(truck.get_pos(), v_minus.get_pos())
            # print("truck's position: ",pos_to_id(truck.get_pos(),tsp), " ", truck.get_num_bikes(), "sum distance so far: ",sum_distance, "sum carbonP: ", carbon)

            truck.move_to(v_minus.get_pos())
            truck.change_bikes(v_minus.get_num_bikes(), v_minus)

            edge_index = get_index(tsp, v_plus)
            # edge_index +=2

        elif Truck.full_load - truck.get_num_bikes() > v_plus.get_num_bikes():

            carbon += getDistance(truck.get_pos(), v_plus.get_pos()) * (TRUCK_WEIGHT + truck.get_num_bikes())
            sum_distance += getDistance(truck.get_pos(), v_plus.get_pos())

            # print("truck's position: ",pos_to_id(truck.get_pos(),tsp), " ", truck.get_num_bikes(), "sum distance so far: ",sum_distance, "sum carbonP: ", carbon)

            truck.move_to(v_plus.get_pos())
            truck.change_bikes(v_plus.get_num_bikes(), v_plus)

            edge_index = get_index(tsp, v_plus)
            # edge_index +=1

        elif Truck.full_load - truck.get_num_bikes() <= v_plus.get_num_bikes():

            truck, carbon, sum_distance = move_to_first_can_be_colletted(v_plus, tsp, truck, carbon, sum_distance)

            edge_index = get_index(tsp, v_plus)

        truck_pos = pos_to_id(truck.get_pos(), tsp)

    return carbon, sum_distance


def pos_to_id(pos, tsp):
    for station in tsp:
        if station.get_pos() == pos:
            return station.id


def main():
    csv_list = read_csv()
    sum_car = 0
    i = 0

    result = []
    for csv_f in csv_list:
        # print(csv_f)
        i += 1
        if i:
            # print(csv_f)

            #stations = generate_data(csv_f)
            #carbon, sum_distance = generate_carbon(stations)

            # print("each_carbon: ",carbon,"sum_distance: ", sum_distance)
            #print(sum_distance)
            # print(carbon)
            # sum_car += carbon
            pass
    # avg_car= sum_car/len(csv_list)
    # print("avg_car: ",avg_car)


def station_125(data_path,k, goPath):
    carbon_list = []
    distance_list = []
    
    if True:
        stations = generate_data(data_path)
        # tsp = get_tsp(stations,Station(0,9999,depot_x,depot_y))
        carbon, sum_distance = generate_carbon(stations,k)
        carbon_list.append(carbon)
        distance_list.append(sum_distance)
        
        #print(carbon)
        # print(sum_distance)
        # print("each_carbon: ",carbon,"sum_distance: ", sum_distance)    
   
    f = open(str(goPath) + "OUT + " + str(k) ,"w+")
    print("###############################################################################")
    print("                 DONE                                    DONE          ")
    print("                                     /")
    print("                                    /")
    print("                                   /")
    print("                                  /___")
    print()
    print("           ___________                              ______________")
    print("                      |                             |")
    print("                      |_____________________________|")
    print()
    print("###############################################################################")
    for i in range(0,len(carbon_list)):
        f.write(str(carbon_list[i])+",")
        f.write(str(distance_list[i])+"\n")
        #print(i)
    f.write("\n")
    #print("distance: ")
    #f.write("distance: ")
    #for i in distance_list:
    #   print(i)

def net_function():
    l = ["/home/agao/ALL_DATA_7-25/", "/home/agao/ALL_DATA_7-25-110/",  "/home/agao/ALL_DATA_7-1000/", "/home/agao/ALL_DATA_7-1000-110/", "/home/agao/ALL_DATA_7-100000/", "/home/agao/ALL_DATA_12-25/", "/home/agao/ALL_DATA_12-25-110/",  "/home/agao/ALL_DATA_12-1000/", "/home/agao/ALL_DATA_12-1000-110/", "/home/agao/ALL_DATA_12-100000/", "/home/agao/ALL_DATA_25-25/", "/home/agao/ALL_DATA_25-25-110/",  "/home/agao/ALL_DATA_25-1000/", "/home/agao/ALL_DATA_25-1000-110/", "/home/agao/ALL_DATA_25-100000/"]

    nCsv = [26,26,1000,1000,100000,26,26,1000,1000,100000,26,26,1000,1000,100000]
    for data_path in l:
        print(l.index(data_path))
        if l.index(data_path) in [6]:
            TRUCK_WEIGHT = 10
            truckFull = 25
        if l.index(data_path) in [11]:
            TRUCK_WEIGHT = 20
            truckFull = 50
        

        for i in range(0,nCsv[l.index(data_path)]):
            print("datapath1: ",data_path)
            Data_path = data_path + str(i) +".csv"
            print("datapath2: ",data_path)
            station_125(Data_path,0,data_path)

        for i in range(0,nCsv[l.index(data_path)]):
            Fata_path = data_path + str(i) +".csv"
            station_125(Fata_path,5,data_path)

        for i in range(0,nCsv[l.index(data_path)]):
            Kata_path = data_path + str(i) +".csv"
            station_125(Kata_path,10,data_path)
            
# main()


#station_125()

net_function()
# depot = Station(0,9999,depot_x,depot_y)

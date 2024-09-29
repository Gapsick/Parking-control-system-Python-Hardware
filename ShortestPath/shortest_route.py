import heapq

def main(yolo_data_queue, car_number_data_queue, route_data_queue):
    """차량 추적 데이터와 차량 번호 데이터를 받아오는 메인 함수"""
    while True:
        # 큐에서 데이터 가져오기
        tracking_data = yolo_data_queue.get()
        if tracking_data is None:  # 종료 신호 (None) 받으면 종료
            break

        # 데이터 처리
        vehicles = tracking_data["vehicles"]

        car_number = None

        # 라즈베리 파이로부터 차량 번호 수신
        if car_number_data_queue.qsize() > 0:
            car_number = car_number_data_queue.get()
            print(f"2번 쓰레드: 라즈베리 파이로부터 수신한 차량 번호: {car_number}")

        parking_positions = {}  # 주차한 차량의 위치 정보
        walking_positions = {}  # 이동 중인 차량의 위치 정보

        # 차량 번호를 차량에 매핑
        if car_number:
            for vehicle in vehicles:
                if entry_x[0] <= vehicle["position"][0] <= entry_x[1]\
                and entry_y[0] <= vehicle["position"][1] <= entry_y[1]:
                    car_numbers[vehicle["id"]] = {"car_number": car_number, "status": "entry", "parking": set_goal(car_number)}
                    print(f"2번 쓰레드: 차량 {vehicle['id']}의 번호: {car_number}")

        for vehicle in vehicles:
            check_position(vehicle, parking_positions, walking_positions)

        set_parking_space(parking_positions)
        set_walking_space(walking_positions)

        for key, value in walking_positions.items():
            # TODO 경로 계산 시에는 해당 주차 구역의 번호가 아닌 이동 구역의 번호를 가져올 필요가 있음
            print("경로 계산", key, car_numbers[value]["parking"])
            route = a_star(graph, congestion, key, car_numbers[value]["parking"])
            print(route)

        # TODO 경로 내에 비어있는 주차 구역이 있는 경우 해당 주차 구역으로 변경 하는 코드

        print("주차한 차량: ", parking_positions)
        print("이동 중인 차량: ", walking_positions)
        print(car_numbers)



        yolo_data_queue.task_done()  # 처리 완료 신호

# 차량의 위치를 확인하는 함수
def check_position(vehicle, arg_parking_positions, arg_walking_positions):
    """차량의 위치를 확인하는 함수"""
    for key, value in parking_space.items():
        if value["position"][0][0] <= vehicle["position"][0] <= value["position"][1][0]\
        and value["position"][0][1] <= vehicle["position"][1] <= value["position"][1][1]:
            arg_parking_positions[key] = vehicle["id"]
            return

    for key, value in walking_space.items():
        if value["position"][0][0] <= vehicle["position"][0] <= value["position"][1][0]\
        and value["position"][0][1] <= vehicle["position"][1] <= value["position"][1][1]:
            arg_walking_positions[key] = vehicle["id"]
            return

# 주차 공간을 설정하는 함수
def set_parking_space(arg_parking_positions):
    """주차 공간을 설정하는 함수"""
    for key, value in parking_space.items():
        if value["name"] in arg_parking_positions:
            parking_space[key]["status"] = "occupied"
            parking_space[key]["car_number"] = arg_parking_positions[value["name"]]
        elif value["status"] == "target":
            pass
        else:
            parking_space[key]["status"] = "empty"
            parking_space[key]["car_number"] = None

# 이동 공간을 설정하는 함수
def set_walking_space(arg_walking_positions):
    """이동 공간을 설정하는 함수"""
    for key, value in walking_space.items():
        if value["name"] in arg_walking_positions:
            walking_space[key]["status"] = "occupied"
            walking_space[key]["car_number"] = arg_walking_positions[value["name"]]
        else:
            walking_space[key]["status"] = "empty"
            walking_space[key]["car_number"] = None

# 주차할 공간을 지정하는 함수
def set_goal(arg_car_number):
    """주차할 공간을 지정하는 함수"""
    for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21):    # 할당할 주차 구역 순서
        if parking_space[i]["status"] == "empty":
            parking_space[i]["status"] = "target"
            parking_space[i]["car_number"] = arg_car_number
            return i

# A* 알고리즘
def heuristic(a, b):
    # 휴리스틱 함수: 여기서는 간단하게 두 노드 간 차이만 계산 (유클리드 거리는 필요하지 않음)
    # 예측용 함수로 모든 계산을 하기 전에 대략적인 예측을 하여 가능성 높은곳만 계산하도록 도와줌
    return 0

# A* 알고리즘
def a_star(graph, congestion, start, goal):
    """경로를 계산하여 반환하는 함수"""
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while pq:
        current = heapq.heappop(pq)[1]
        
        if current == goal:
            break
        
        for next_node in graph[current]:
            new_cost = cost_so_far[current] + graph[current][next_node] + congestion[current][next_node]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(pq, (priority, next_node))
                came_from[next_node] = current
    
    # 경로를 역추적하여 반환
    current = goal
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    
    return path

# 주차 구역의 좌표값
parking_space = {
    # status = empty, occupied, target
    0: {"name": "A1", "status": "empty", "car_number": None, "position": ((0, 0), (50, 50))},
    1: {"name": "A2", "status": "empty", "car_number": None, "position": ((50, 0), (100, 50))},
    2: {"name": "A3", "status": "empty", "car_number": None, "position": ((100, 0), (150, 50))},
    3: {"name": "A4", "status": "empty", "car_number": None, "position": ((150, 0), (200, 50))},
    4: {"name": "A5", "status": "empty", "car_number": None, "position": ((200, 0), (250, 50))},
    5: {"name": "A6", "status": "empty", "car_number": None, "position": ((250, 0), (300, 50))},
    6: {"name": "B1", "status": "empty", "car_number": None, "position": ((0, 50), (50, 100))},
    7: {"name": "B2", "status": "empty", "car_number": None, "position": ((50, 50), (100, 100))},
    8: {"name": "B3", "status": "empty", "car_number": None, "position": ((100, 50), (150, 100))},
    9: {"name": "B4", "status": "empty", "car_number": None, "position": ((150, 50), (200, 100))},
    10: {"name": "C1", "status": "empty", "car_number": None, "position": ((0, 100), (50, 150))},
    11: {"name": "C2", "status": "empty", "car_number": None, "position": ((50, 100), (100, 150))},
    12: {"name": "C3", "status": "empty", "car_number": None, "position": ((100, 100), (150, 150))},
    13: {"name": "C4", "status": "empty", "car_number": None, "position": ((150, 100), (200, 150))},
    14: {"name": "D1", "status": "empty", "car_number": None, "position": ((0, 150), (50, 200))},
    15: {"name": "D2", "status": "empty", "car_number": None, "position": ((50, 150), (100, 200))},
    16: {"name": "D3", "status": "empty", "car_number": None, "position": ((100, 150), (150, 200))},
    17: {"name": "D4", "status": "empty", "car_number": None, "position": ((150, 150), (200, 200))},
    18: {"name": "D5", "status": "empty", "car_number": None, "position": ((200, 150), (250, 200))},
    19: {"name": "D6", "status": "empty", "car_number": None, "position": ((250, 150), (300, 200))},
    20: {"name": "D7", "status": "empty", "car_number": None, "position": ((0, 200), (50, 250))},
    21: {"name": "D8", "status": "empty", "car_number": None, "position": ((50, 200), (100, 250))},
}

# 이동 구역의 좌표값
walking_space = {
    0: {"name": "Entry", "position": ((250, 250), (300, 300)), "parking_space": None},
    1: {"name": "Path_2", "position": ((310, 250), (360, 300)), "parking_space": None},
    2: {"name": "Path_3", "position": ((370, 250), (420, 300)), "parking_space": None},
    3: {"name": "Path_4", "position": ((250, 310), (300, 360))},
    4: {"name": "Path_5", "position": ((310, 310), (360, 360))},
    5: {"name": "Path_6", "position": ((370, 310), (420, 360))},
    6: {"name": "Path_7", "position": ((250, 370), (300, 420))},
    7: {"name": "Path_8", "position": ((310, 370), (360, 420))},
    8: {"name": "Path_9", "position": ((370, 370), (420, 420))},
    9: {"name": "Path_10", "position": ((250, 430), (300, 480))},
    10: {"name": "Path_11", "position": ((310, 430), (360, 480))},
    11: {"name": "Path_12", "position": ((370, 430), (420, 480))},
    12: {"name": "Path_13", "position": ((250, 490), (300, 540))},
    13: {"name": "Path_14", "position": ((310, 490), (360, 540))},
    14: {"name": "Exit", "position": ((370, 490), (420, 540))},
}

# 그래프
graph = {
    0: {1: 1},
    1: {0: 1, 2: 1, 4: 1},
    2: {1: 1, 3: 1},
    3: {2: 1, 5: 1},
    4: {1: 1, 6: 1},
    5: {3: 1, 8: 1},
    6: {4: 1, 7: 1, 9: 1},
    7: {6: 1, 8: 1},
    8: {5: 1, 7: 1, 10: 1},
    9: {6: 1, 11: 1},
    10: {8: 1, 13: 1},
    11: {9: 1, 12: 1, 14: 1},
    12: {11: 1, 13: 1},
    13: {10: 1, 12: 1},
    14: {11: 1}
}

# 혼잡도
congestion = {
    0: {1: 1},
    1: {0: 1, 2: 1, 4: 1},
    2: {1: 1, 3: 1},
    3: {2: 1, 5: 1},
    4: {1: 1, 6: 1},
    5: {3: 1, 8: 1},
    6: {4: 1, 7: 1, 9: 1},
    7: {6: 1, 8: 1},
    8: {5: 1, 7: 1, 10: 1},
    9: {6: 1, 11: 1},
    10: {8: 1, 13: 1},
    11: {9: 1, 12: 1, 14: 1},
    12: {11: 1, 13: 1},
    13: {10: 1, 12: 1},
    14: {11: 1}
}

# 차량의 번호와 ID를 매핑
car_numbers = {
    # status = entry, parking, exit
    # parking = 상태가 entry일 경우에는 주차할 구역, parking일 경우에는 주차한 구역
    # id: {"car_number": "1234", "status": "entry", "parking": 0}
    0: {"car_number": "12가1234", "status": "entry", "parking": 0},
}

# 경로
routes = {

}

# 입구의 좌표
entry_x = (0, 100)
entry_y = (0, 100)

if __name__ == "__main__":

    start = 1
    goal = 13

    path = a_star(graph, congestion, start, goal)
    print(path)
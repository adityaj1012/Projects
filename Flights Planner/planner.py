import sys
sys.setrecursionlimit(10**7)
class CustomHeapq:
    def __init__(self):
        self.heap = []

    def heappush(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def heappop(self):
        if len(self.heap) == 0:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self.heap) - 1)
        smallest = self.heap.pop()
        if len(self.heap) > 0:
            self._sift_down(0)
        return smallest

    def _sift_up(self, idx):
        parent_idx = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent_idx]:
            self._swap(idx, parent_idx)
            idx = parent_idx
            parent_idx = (idx - 1) // 2

    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            left_child = 2 * idx + 1
            right_child = 2 * idx + 2
            smallest = idx
            if left_child < n and self.heap[left_child] < self.heap[smallest]:
                smallest = left_child
            if right_child < n and self.heap[right_child] < self.heap[smallest]:
                smallest = right_child
            if smallest == idx:
                break
            self._swap(idx, smallest)
            idx = smallest

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __len__(self):
        return len(self.heap)

    def peek(self):
        if len(self.heap) > 0:
            return self.heap[0]
        raise IndexError("peek from empty heap")
    
class CustomDeque:
    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def append_left(self, item):
        self.data.insert(0, item)

    def pop(self):
        if len(self.data) == 0:
            raise IndexError("pop from empty deque")
        return self.data.pop()

    def pop_left(self):
        if len(self.data) == 0:
            raise IndexError("pop_left from empty deque")
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def peek(self):
        if len(self.data) == 0:
            raise IndexError("peek from empty deque")
        return self.data[-1]

    def peek_left(self):
        if len(self.data) == 0:
            raise IndexError("peek_left from empty deque")
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def clear(self):
        self.data.clear()

class Planner:
    def __init__(self, flights):
        self.flights = flights
        self.total_flights = len(flights)
        city_count = max(max(flight.start_city, flight.end_city) for flight in flights) + 1
        self.city_data = [[[], []] for _ in range(city_count)]
        for index, flight in enumerate(flights):
            self.city_data[flight.start_city][1].append(index)  # Departures
            self.city_data[flight.end_city][0].append(index)    # Arrivals
        self.routes = [[] for _ in range(self.total_flights)]
        for index, flight in enumerate(flights):
            destination = flight.end_city
            for following_flight_index in self.city_data[destination][1]:
                following_flight = flights[following_flight_index]
                if following_flight.departure_time - flight.arrival_time >= 20:
                    self.routes[index].append(following_flight_index)

    def least_flights_earliest_route(self, origin_city, destination_city, start_time, end_time):
        if origin_city == destination_city:
            return []
        best_path, fewest_stops, earliest_arrival = None, float('inf'), end_time
        def traverse(start_flight_index):
            queue = CustomDeque()
            queue.append((start_flight_index, 0, [start_flight_index]))  # (flight index, count, path)
            visited = [False] * self.total_flights
            visited[start_flight_index] = True
            while not queue.is_empty():
                current_index, level, path = queue.pop_left()
                current_flight = self.flights[current_index]
                arrival = current_flight.arrival_time
                if current_flight.end_city == destination_city and arrival <= end_time:
                    nonlocal best_path, fewest_stops, earliest_arrival
                    if level < fewest_stops or (level == fewest_stops and arrival < earliest_arrival):
                        best_path = path[:]
                        fewest_stops = level
                        earliest_arrival = arrival
                    continue
                for next_index in self.routes[current_index]:
                    next_flight = self.flights[next_index]
                    if not visited[next_index] and next_flight.departure_time - arrival >= 20:
                        visited[next_index] = True
                        queue.append((next_index, level + 1, path + [next_index]))
        for initial_index in self.city_data[origin_city][1]:
            initial_flight = self.flights[initial_index]
            if start_time <= initial_flight.departure_time <= end_time:
                traverse(initial_index)
        return [self.flights[idx] for idx in (best_path or [])]

    def cheapest_route(self, origin_city, destination_city, start_time, end_time):
        if origin_city == destination_city:
            return []
        best_path, lowest_cost = None, float('inf')
        priority_queue = CustomHeapq()
        visited = [False] * self.total_flights
        for initial_index in self.city_data[origin_city][1]:
            initial_flight = self.flights[initial_index]
            if start_time <= initial_flight.departure_time <= end_time:
                priority_queue.heappush((initial_flight.fare, initial_index, [initial_index]))
        while len(priority_queue) > 0:
            current_cost, current_index, path = priority_queue.heappop()
            current_flight = self.flights[current_index]
            arrival = current_flight.arrival_time
            if current_flight.end_city == destination_city and arrival <= end_time:
                if current_cost < lowest_cost:
                    best_path = path[:]
                    lowest_cost = current_cost
                continue
            visited[current_index] = True
            for next_index in self.routes[current_index]:
                next_flight = self.flights[next_index]
                if not visited[next_index] and next_flight.departure_time - arrival >= 20:
                    new_cost = current_cost + next_flight.fare
                    priority_queue.heappush((new_cost, next_index, path + [next_index]))
        return [self.flights[idx] for idx in (best_path or [])]

    def least_flights_cheapest_route(self, origin_city, destination_city, start_time, end_time):
        if origin_city == destination_city:
            return []
        best_path, fewest_stops, lowest_cost = None, float('inf'), float('inf')
        priority_queue = CustomHeapq() 
        for initial_index in self.city_data[origin_city][1]:
            initial_flight = self.flights[initial_index]
            if initial_flight.departure_time >= start_time:
                priority_queue.heappush((1, initial_flight.fare, initial_index, [initial_index]))
        while len(priority_queue) > 0:
            stop_count, current_cost, current_index, path = priority_queue.heappop()
            current_flight = self.flights[current_index]
            arrival = current_flight.arrival_time
            if current_flight.end_city == destination_city and arrival <= end_time:
                if (stop_count < fewest_stops or 
                    (stop_count == fewest_stops and current_cost < lowest_cost)):
                    best_path = path[:]
                    fewest_stops = stop_count
                    lowest_cost = current_cost
                continue
            for next_index in self.routes[current_index]:
                next_flight = self.flights[next_index]
                if next_flight.departure_time - arrival >= 20 and next_flight.departure_time <= end_time:
                    priority_queue.heappush((
                        stop_count + 1,
                        current_cost + next_flight.fare,
                        next_index,
                        path + [next_index]
                    ))
        return [self.flights[idx] for idx in (best_path or [])]

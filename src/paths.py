import heapq
from typing import Callable, Dict, List, Set, Tuple


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


class PathBuilder:
    def __init__(
        self, is_passable: Callable[[int, int], bool], acceptable_error: int = 5
    ) -> None:
        self.is_passable = is_passable
        self.acceptable_error = acceptable_error

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and self.is_passable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def build_path(self, start_x: int, start_y: int, goal_x: int, goal_y: int):
        """
        Try to walk from start to goal and if that fais walk from goal to start.
        """
        start_to_goal = self._build_path(start_x, start_y, goal_x, goal_y)
        if len(start_to_goal) > 0:
            return start_to_goal
        return self._build_path(goal_x, goal_y, start_x, start_y)

    def _build_path(
        self, start_x: int, start_y: int, goal_x: int, goal_y: int
    ) -> List[Tuple[int, int]]:
        open_set = [(0, 0, start_x, start_y)]
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], int] = {(start_x, start_y): 0}
        closed_set: Set[Tuple[int, int]] = set()

        while open_set:
            _, current_g, x, y = heapq.heappop(open_set)

            if (x, y) in closed_set:
                continue

            closed_set.add((x, y))

            if x == goal_x and y == goal_y:
                path = []
                current = (x, y)
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append((start_x, start_y))
                return list(reversed(path))

            for nx, ny in self._get_neighbors(x, y):
                if (nx, ny) in closed_set:
                    continue

                tentative_g = current_g + 1

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = (x, y)
                    g_score[(nx, ny)] = tentative_g
                    f_score = tentative_g + manhattan_distance(nx, ny, goal_x, goal_y)
                    heapq.heappush(open_set, (f_score, tentative_g, nx, ny))

        # the end is unreachable but maybe something in its proximity is
        for x_offset in range(-self.acceptable_error, self.acceptable_error + 1):
            for y_offset in range(-self.acceptable_error, self.acceptable_error + 1):
                if abs(x_offset) + abs(y_offset) != self.acceptable_error:
                    continue
                current = (goal_x + x_offset, goal_y + y_offset)
                if current in came_from:
                    path = []
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.append((start_x, start_y))
                    return list(reversed(path))

        return []

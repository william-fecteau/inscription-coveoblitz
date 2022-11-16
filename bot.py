from game_message import Action, Anchor, Dock, Sail, Spawn, Tick, directions


def getNeighbours(position, mapSize):
    maxIndex = mapSize * mapSize - 1

    neighbours = []
    if position > maxIndex:
        return neighbours

    for i in range(-1, 2):
        cur = position + (i * mapSize)
        if cur < 0 or cur > maxIndex:
            continue

        startRow = cur - (cur % mapSize)
        endRow = startRow + mapSize - 1

        for j in range(-1, 2):
            value = cur + j

            if value >= startRow and value <= endRow and value != position:
                neighbours.append(value)

    return neighbours


def bfs(src, dest, mapSize):
    visited = [False] * (mapSize * mapSize)
    queue = []
    queue.append(src)
    visited[src] = True
    while queue:
        s = queue.pop(0)
        for i in getNeighbours(s, mapSize):
            if visited[i] == False:
                visited[i] = True
                queue.append(i)

    return visited[dest]


if __name__ == "__main__":
    print(getNeighbours(22, 5))


class Bot:
    def __init__(self):
        self.shouldDock = False
        self.mapSize = 10
        print("Initializing your super mega duper bot")

    def get_next_move(self, tick: Tick) -> Action:
        if tick.currentLocation is None:
            self.shouldDock = True
            self.mapSize = len(tick.map.topology)
            return Spawn(tick.map.ports[0])
        elif self.shouldDock:
            self.shouldDock = False
            return Dock()

        return Sail(directions[tick.currentTick % len(directions)])

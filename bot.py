import math
from typing import List, Union

import astar
from game_message import (Action, Anchor, Dock, Position, Sail, Spawn, Tick,
                          directions)


class Bot:
    def __init__(self):
        self.distanceMatrix = None
        self.nextPort = None
        self.maze = None
        self.curMove = 0

    def euclidianDistance(self, a: Position, b: Position):
        return math.sqrt((a.row - b.row)**2 + (a.column - b.column)**2)

    def buildDistanceMatrix(self, tick: Tick):
        distanceMatrix = []
        for port in tick.map.ports:
            row = []
            for port2 in tick.map.ports:
                row.append(self.euclidianDistance(port, port2))
            distanceMatrix.append(row)

        return distanceMatrix

    def buildMazeMatrix(self, tick: Tick):
        maxTide = tick.map.tideLevels.max

        maze = []
        for i in range(len(tick.map.topology)):
            row = []
            for j in range(len(tick.map.topology[i])):
                if tick.map.topology[i][j] >= maxTide:
                    row.append(1)
                else:
                    row.append(0)
            maze.append(row)

        print(*maze, sep='\n')
        return maze

    def computeDirection(self, positionA, positionB):
        dy = positionB[0] - positionA[0]
        dx = positionB[1] - positionA[1]

        if dx == 0 and dy < 0:
            return "N"
        if dx > 0 and dy < 0:
            return "NE"
        if dx > 0 and dy == 0:
            return "E"
        if dx > 0 and dy > 0:
            return "SE"
        if dx == 0 and dy > 0:
            return "S"
        if dx < 0 and dy > 0:
            return "SW"
        if dx < 0 and dy == 0:
            return "W"
        if dx < 0 and dy < 0:
            return "NW"

        return "lol"

    def getClosestPort(self, tick: Tick, indexPort: int):
        row = self.distanceMatrix[indexPort]

        min = 9999999999
        index = -1
        for i in range(len(row)):
            if i != indexPort and i not in tick.visitedPortIndices and row[i] < min:
                min = row[i]
                index = i

        return index

    def get_next_move(self, tick: Tick) -> Action:
        ports = tick.map.ports

        if self.distanceMatrix is None:
            self.distanceMatrix = self.buildDistanceMatrix(tick)
            self.maze = self.buildMazeMatrix(tick)

            self.nextPort = 0
            port = ports[self.nextPort]
            return Spawn(position=Position(row=port.row, column=port.column))

        # If we are at a port, we need to decide where to go next
        if tick.currentLocation.row == ports[self.nextPort].row and tick.currentLocation.column == ports[self.nextPort].column:
            self.nextPort = self.getClosestPort(tick, self.nextPort)
            if self.nextPort == -1:
                # We have visited all ports, go back to the first one TODO: change for something else than 0
                self.nextPort = 0

            self.oldLocation = tick.currentLocation
            port = ports[self.nextPort]
            self.path = astar.astar(
                self.maze, (tick.currentLocation.row, tick.currentLocation.column), (port.row, port.column))
            print(self.path)
            self.moi = 0

            return Dock()

        if tick.currentLocation.row != self.oldLocation.row or tick.currentLocation.column != self.oldLocation.column:
            self.moi += 1

        direction = self.computeDirection(
            self.path[self.moi], self.path[self.moi + 1])
        print(direction)
        self.oldLocation = tick.currentLocation

        return Sail(direction=direction)

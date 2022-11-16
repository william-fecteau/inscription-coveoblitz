import math
from typing import List, Union

from game_message import (Action, Anchor, Dock, Position, Sail, Spawn, Tick,
                          directions)


class Bot:
    def __init__(self):
        self.distanceMatrix = None
        self.nextPort = None

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

            self.nextPort = 0
            port = ports[self.nextPort]
            return Spawn(position=Position(row=port.row, column=port.column))

        # If we are at a port, we need to decide where to go next
        if tick.currentLocation.row == ports[self.nextPort].row and tick.currentLocation.column == ports[self.nextPort].column:
            self.nextPort = self.getClosestPort(tick, self.nextPort)
            if self.nextPort == -1:
                # We have visited all ports, go back to the first one TODO: change for something else than 0
                self.nextPort = 0

            print("LOL JE DOCKER ICI")
            return Dock()

        # return Sail(direction="N")
        # If we are not at a port, we need to sail to the next port
        port = ports[self.nextPort]
        if port.row > tick.currentLocation.row:
            return Sail(direction="S")
        elif port.row < tick.currentLocation.row:
            return Sail(direction="N")
        elif port.column > tick.currentLocation.column:
            return Sail(direction="E")
        elif port.column < tick.currentLocation.column:
            return Sail(direction="W")

        return Sail(directions[tick.currentTick % len(directions)])

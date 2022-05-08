import json
import os
import math


class Edge:
    def __init__(self, text, destination, locked=0, item=""):
        self.text = text
        self.destination = destination
        self.locked = locked
        self.item = item

    def toDict(self):
        return {"text": self.text, "destination": self.destination, "locked": self.locked, "item": self.item}

    @staticmethod
    def fromDict(dict):
        return Edge(dict["text"], dict["destination"], dict["locked"], dict["item"])


class Vertex:
    def __init__(self, text, event=0, item=None, edges=None):
        self.text = text
        self.event = event
        self.item = item
        if edges is None:
            edges = []
        self.edges = edges

    def toDict(self):
        if self.event == 4 or self.event == 5:
            return {"text": self.text, "event": self.event, "item": self.item.toDict(), "edges": [edge.toDict() for edge in self.edges]}
        return {"text": self.text, "event": self.event, "item": self.item, "edges": [edge.toDict() for edge in self.edges]}

    @staticmethod
    def fromDict(dict):
        if dict["event"] == 4:
            return Vertex(dict["text"], dict["event"], Entity.fromDict(dict["item"]), [Edge.fromDict(edge) for edge in dict["edges"]])
        if dict["event"] == 5:
            return Vertex(dict["text"], dict["event"], Weapon.fromDict(dict["item"]), [Edge.fromDict(edge) for edge in dict["edges"]])
        return Vertex(dict["text"], dict["event"], dict["item"], [Edge.fromDict(edge) for edge in dict["edges"]])


class Graph:
    def __init__(self):
        self.vertexes = []
        self.strengths = {}
        self.player = Entity()

    def load(self, file):
        if not os.path.exists(file):
            return False
        with open(file, "r") as load:
            self.strengths = json.loads(load.readline().strip())
            self.player = Entity.fromDict(json.loads(load.readline().strip()))
            for line in load:
                v = json.loads(line.strip())
                if v is not None:
                    v = Vertex.fromDict(v)
                self.vertexes.append(v)
        return True

    def addVertex(self, vertex):
        for i in range(len(self.vertexes)):
            if self.vertexes[i] is None:
                self.vertexes[i] = vertex
                return
        self.vertexes.append(vertex)

    def removeVertex(self, index):
        if index < 0 or index >= len(self.vertexes):
            return
        self.vertexes[index] = None
        for vertex in self.vertexes:
            if vertex is not None:
                for edge in vertex.edges:
                    if edge.destination == index:
                        vertex.edges.remove(edge)

    def findVertexSnippet(self, text):
        results = {}
        for i in range(len(self.vertexes)):
            if self.vertexes[i] is not None and text in self.vertexes[i].text:
                results[i] = self.vertexes[i].text
        return results

    def save(self, file):
        with open(file, "w") as save:
            save.write(json.dumps(self.strengths) + "\n")
            save.write(json.dumps(self.player.toDict()) + "\n")
            for v in self.vertexes:
                save.write(json.dumps(v.toDict() if v is not None else None) + "\n")

class Weapon:
    def __init__(self, name, damage, uses, maxUses, type):
        self.name = name
        self.damage = damage
        self.uses = uses
        self.maxUses = maxUses
        self.type = type

    def repair(self, value):
        self.uses = math.floor(min(self.uses + value, self.maxUses))

    def fullRepair(self):
        self.uses = self.maxUses

    def toDict(self):
        return {"name": self.name, "damage": self.damage, "uses": self.uses, "maxUses": self.maxUses, "type": self.type}

    @staticmethod
    def fromDict(dict):
        return Weapon(dict["name"], dict["damage"], dict["uses"], dict["maxUses"], dict["type"])

class Entity:
    def __init__(self, name="Player", hp=100, maxhp=100, type="None", weapons=None):
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.type = type
        if weapons is None:
            weapons = []
        self.weapons = weapons

    def attack(self, other, index, modifier):
        if self.weapons[index].uses <= 0:
            return False
        other.hp = math.floor(max(0, other.hp - self.weapons[index].damage * modifier))
        self.weapons[index].uses -= 1
        return True

    def heal(self, value):
        self.hp = math.floor(min(self.hp + value, self.maxhp))

    def fullHeal(self):
        self.hp = self.maxhp

    def getWeapon(self, name):
        for weapon in self.weapons:
            if weapon.name == name:
                return weapon
        return None

    def removeWeapon(self, name):
        for weapon in self.weapons:
            if weapon.name == name:
                self.weapons.remove(weapon)
                return True
        return False

    def toDict(self):
        return {"name": self.name, "hp": self.hp, "maxhp": self.maxhp, "type": self.type, "weapons": [weapon.toDict() for weapon in self.weapons]}

    @staticmethod
    def fromDict(dict):
        return Entity(dict["name"], dict["hp"], dict["maxhp"], dict["type"], [Weapon.fromDict(weapon) for weapon in dict["weapons"]])

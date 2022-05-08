from graph import *
import os
import json
import random

while True:
    graph = Graph()
    while True:
        file = input("Enter file name: ")
        os.system("cls")
        if graph.load(file+".game"):
            break
        print("File not found")

    if os.path.exists(file+".save") and input("Save file detected, load? (Y/N) ").upper() == "Y":
        with open(file+".save", "r") as load:
            vertex = graph.vertexes[json.loads(load.readline().strip())]
            player = Entity.fromDict(json.loads(load.readline().strip()))
            items = json.loads(load.readline().strip())
            info = json.loads(load.readline().strip())
            for i in range(len(graph.vertexes)):
                if graph.vertexes[i] is not None:
                    graph.vertexes[i].event = info[i][0]
                    for j in range(len(graph.vertexes[i].edges)):
                        graph.vertexes[i].edges[j].locked = info[i][1][j]
    else:
        vertex = graph.vertexes[0]
        player = graph.player
        items = []

    os.system("cls")

    def saveData():
        with open(file+".save", "w") as save:
            save.write(json.dumps(graph.vertexes.index(vertex)) + "\n")
            save.write(json.dumps(player.toDict()) + "\n")
            save.write(json.dumps(items) + "\n")
            save.write(json.dumps([[v.event, [e.locked for e in v.edges]] if v is not None else None for v in graph.vertexes]) + "\n")

    while True:
        try:
            print(vertex.text.replace("[player]", player.name))

            if vertex.event == 1:
                print("Event: You won!")
                break
            if vertex.event == 2:
                print("Event: You lost!")
                break
            if vertex.event == 3:
                print(f"Event: You got {vertex.item}")
                items.append(vertex.item)
                vertex.event = 0
                saveData()
            defeated = False
            if vertex.event == 4:
                if len(player.weapons) <= 0:
                    print("Event: You entered battle without any weapons. You automatically lost!")
                    break
                enemy = vertex.item
                print(f"Event: You encountered {enemy.name}")
                turn = True
                while True:
                    print(f"{player.name} HP: {player.hp}/{player.maxhp}, Type: {player.type}\n{enemy.name} HP: {enemy.hp}/{enemy.maxhp}, Type: {enemy.type}")
                    if turn:
                        while True:
                            for i in range(len(player.weapons)):
                                weapon = player.weapons[i]
                                print(f" {i}: {weapon.name}, Damage: {weapon.damage}, Uses: {weapon.uses}/{weapon.maxUses}, Type: {weapon.type}")
                            weapon = input("Enter weapon... ")
                            if not weapon.isnumeric() or int(weapon) < 0 or int(weapon) >= len(player.weapons):
                                os.system("cls")
                                print("Warning: Unavailable weapon")
                                print(f"{player.name} HP: {player.hp}/{player.maxhp}, Type: {player.type}\n{enemy.name} HP: {enemy.hp}/{enemy.maxhp}, Type: {enemy.type}")
                                continue
                            if player.attack(enemy, int(weapon), 2 if graph.strengths.get(player.weapons[int(weapon)].type) is not None and enemy.type in graph.strengths.get(player.weapons[int(weapon)].type) else (0.5 if graph.strengths.get(enemy.type) is not None and player.weapons[int(weapon)].type in graph.strengths.get(enemy.type) else 1)):
                                os.system("cls")
                                print(f"Event: Attacked {enemy.name} with {player.weapons[int(weapon)].name}")
                                if graph.strengths.get(player.weapons[int(weapon)].type) is not None and enemy.type in graph.strengths.get(player.weapons[int(weapon)].type):
                                    print("Info: Attack was super effective")
                                elif graph.strengths.get(enemy.type) is not None and player.weapons[int(weapon)].type in graph.strengths.get(enemy.type):
                                    print("Info: Attack was not very effective")
                                break
                            os.system("cls")
                            print("Warning: Cannot use that weapon")
                            print(f"{player.name} HP: {player.hp}/{player.maxhp}, Type: {player.type}\n{enemy.name} HP: {enemy.hp}/{enemy.maxhp}, Type: {enemy.type}")
                    else:
                        for i in range(len(enemy.weapons)):
                            weapon = enemy.weapons[i]
                            print(f" {i}: {weapon.name}, Damage: {weapon.damage}, Uses: {weapon.uses}/{weapon.maxUses}, Type: {weapon.type}")
                        input("Enter to continue... ")
                        while True:
                            weapon = random.randint(0, len(enemy.weapons)-1)
                            if enemy.attack(player, weapon, 2 if graph.strengths.get(enemy.weapons[weapon].type) is not None and player.type in graph.strengths.get(enemy.weapons[weapon].type) else (0.5 if graph.strengths.get(player.type) is not None and enemy.weapons[weapon].type in graph.strengths.get(player.type) else 1)):
                                os.system("cls")
                                print(f"Event: {enemy.name} attacked with {enemy.weapons[weapon].name}")
                                if graph.strengths.get(enemy.weapons[weapon].type) is not None and player.type in graph.strengths.get(enemy.weapons[weapon].type):
                                    print("Info: Attack was super effective")
                                elif graph.strengths.get(player.type) is not None and enemy.weapons[weapon].type in graph.strengths.get(player.type):
                                    print("Info: Attack was not very effective")
                                break

                    if enemy.hp <= 0:
                        print(f"Event: You defeated {enemy.name}")
                        break
                    if player.hp <= 0:
                        os.system("cls")
                        defeated = True
                        player.fullHeal()
                        for w in player.weapons:
                            w.fullRepair()
                        enemy.fullHeal()
                        for w in enemy.weapons:
                            w.fullRepair()
                        print("Event: You were defeated; restarting state")
                        break

                    turn = not turn

                if defeated:
                    continue
                vertex.event = 0
                saveData()

            if vertex.event == 5:
                print(f"Event: You got {vertex.item.name}")
                player.weapons.append(vertex.item)
                vertex.event = 0
                saveData()
            if vertex.event == 6:
                print(f"Event: You got healed for {min(player.maxhp - player.hp, vertex.item)} hp")
                player.heal(vertex.item)
                vertex.event = 0
                saveData()
            if vertex.event == 7:
                print(f"Event: Your weapons were repaired for a max of {vertex.item} uses")
                for weapon in player.weapons:
                    weapon.repair(vertex.item)
                vertex.event = 0
                saveData()

            for i in range(len(vertex.edges)):
                print(f" {i}: {vertex.edges[i].text} {['', '(LOCKED)', '(Will lock if gone through)', f'(Open with {vertex.edges[i].item})'][vertex.edges[i].locked]}")
            if len(vertex.edges) > 1:
                edge = vertex.edges[int(input("Enter an option... "))]
            else:
                input("Press enter to continue... ")
                edge = vertex.edges[0]

            os.system("cls")

            if edge.locked == 1:
                print("Warning: Path is locked")
                continue
            if edge.locked == 2:
                edge.locked = 1
                for e in graph.vertexes[edge.destination].edges:
                    if graph.vertexes[e.destination] == vertex:
                        e.locked = 1
                        break
                print("Event: Path has been closed behind you")
            if edge.locked == 3:
                if edge.item not in items:
                    print("Warning: You do not have the required item")
                    continue
                edge.locked = 0
                for e in graph.vertexes[edge.destination].edges:
                    if graph.vertexes[e.destination] == vertex:
                        e.locked = 0
                        break
                items.remove(edge.item)
                print("Event: Path has been unlocked")

            vertex = graph.vertexes[edge.destination]
            saveData()
        except:
            os.system("cls")
            print("Warning: An issue occurred")

    if input("Play again? (Y/N) ").upper() == "Y":
        os.system("cls")
        continue
    else:
        break

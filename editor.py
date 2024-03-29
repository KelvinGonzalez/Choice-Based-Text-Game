from graph import *

helpString = str("Commands:\n"
      " -traverse: Traverse to one of the connected states through a path\n"
      " -go to: Go to the state with the specified id\n"
      " -back: Go back to the state you previously were in\n"
      " -search: Search for a state by including snippets of its prompt\n"
      " -state info: See information about the current state\n"
      " -state info id: See information about the state with the specified id\n"
      " -edit player: Edit player's data\n"
      " -edit state: Edit state's data\n"
      " -delete state: Delete the current state\n"
      " -delete state id: Delete the state with the specified id\n"
      " -add path: Add a new path to the current state\n"
      " -edit path: Edit one of the current state's paths\n"
      " -delete path: Delete one of the current state's path\n"
      " -add type: Add a new type (Battle System)\n"
      " -remove type: Remove a type (Battle System)\n"
      " -types: View all types and their strengths (Battle System)\n"
      " -add strength: Add a strength to the specified type (Battle System)\n"
      " -remove strength: Remove a strength from the specified type (Battle System)\n"
      " -save: Save current data\n"
      " -exit: Save data and end program execution")

print(helpString)

graph = Graph()
file = input("Enter file name: ") + ".game"

print("File loaded" if graph.load(file) else "File created")

if len(graph.vertexes) == 0:
    graph.addVertex(Vertex(input("Enter prompt: ")))
    print("Initial state created")
vertex = graph.vertexes[0]

vertexStack = []

while True:
    try:
        answer = input("Enter command... ")
        if answer == "go to":
            i = int(input("Enter state id: "))
            vertexStack.append(vertex)
            vertex = graph.vertexes[i]
            print(f"Located on state {i}: '{vertex.text}'")
        elif answer == "search":
            print(graph.findVertexSnippet(input("Enter snippets of prompt: ")))
        elif answer == "state info":
            print(vertex.toDict())
        elif answer == "state info id":
            print(graph.vertexes[int(input("Enter state id: "))].toDict())
        elif answer == "edit player":
            print(graph.player.toDict())
            choice = input("Enter property (Name, HP, MaxHP, Type, Weapons): ")
            if choice.lower() == "name":
                graph.player.name = input("Enter name: ")
                print("Edited player name")
            elif choice.lower() == "hp":
                graph.player.hp = int(input("Enter hp: "))
                print("Edited player hp")
            elif choice.lower() == "maxhp":
                graph.player.maxhp = int(input("Enter maxhp: "))
                print("Edited player maxhp")
            elif choice.lower() == "type":
                graph.player.type = input("Enter type: ")
                print("Edited player type")
            elif choice.lower() == "weapons":
                while True:
                    choice = input("Add, remove, or edit weapon? (A/R/E/N) ").upper()
                    if choice != "A" and choice != "R" and choice != "E":
                        break
                    if choice == "A":
                        graph.player.weapons.append(Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: ")))
                    elif choice == "R":
                        graph.player.removeWeapon(input("Enter name: "))
                    else:
                        weapon = graph.player.getWeapon(input("Enter name: "))
                        weapon.name = input("Enter name: ") if input("Edit name? (Y/N) ").upper() == "Y" else weapon.name
                        weapon.damage = int(input("Enter damage: ")) if input("Edit damage? (Y/N) ").upper() == "Y" else weapon.damage
                        weapon.uses = int(input("Enter uses: ")) if input("Edit uses? (Y/N) ").upper() == "Y" else weapon.uses
                        weapon.maxUses = int(input("Enter max uses: ")) if input("Edit max uses? (Y/N) ").upper() == "Y" else weapon.maxUses
                        weapon.type = input("Enter type: ") if input("Edit type? (Y/N) ").upper() == "Y" else weapon.type
                print("Edited player weapons")
            else:
                print("Unavailable choice")
        elif answer == "edit state":
            dict = vertex.toDict()
            dict.pop("edges")
            print(dict)
            choice = input("Enter property (Text, Event, Item): ")
            if choice.lower() == "text":
                vertex.text = input("Enter prompt: ")
                print("State text changed")
            elif choice.lower() == "event":
                oldEvent = vertex.event
                vertex.event = int(input("Enter event (0=None, 1=Win, 2=Loss, 3=Item, 4=Battle, 5=Weapon, 6=Heal, 7=Repair, 8=Input): "))
                if vertex.event == oldEvent:
                    print("State event remained the same")
                    continue
                print("State event changed")
                if vertex.event == 0 or vertex.event == 1 or vertex.event == 2:
                    vertex.item = ""
                if vertex.event == 3:
                    vertex.item = input("Enter item name: ")
                    print("State item changed")
                if vertex.event == 4:
                    if isinstance(vertex.item, Entity):
                        weapons = vertex.item.weapons
                    else:
                        weapons = []
                    vertex.item = Entity(input("Enter enemy name: "), int(input("Enter enemy hp: ")), int(input("Enter enemy max hp: ")), input("Enter enemy type: "), weapons)
                    while True:
                        choice = input("Add, remove, or edit weapon? (A/R/E/N) ").upper()
                        if choice != "A" and choice != "R" and choice != "E":
                            break
                        if choice == "A":
                            vertex.item.weapons.append(Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: ")))
                        elif choice == "R":
                            vertex.item.removeWeapon(input("Enter name: "))
                        else:
                            weapon = vertex.item.getWeapon(input("Enter name: "))
                            weapon.name = input("Enter name: ") if input("Edit name? (Y/N) ").upper() == "Y" else weapon.name
                            weapon.damage = int(input("Enter damage: ")) if input("Edit damage? (Y/N) ").upper() == "Y" else weapon.damage
                            weapon.uses = int(input("Enter uses: ")) if input("Edit uses? (Y/N) ").upper() == "Y" else weapon.uses
                            weapon.maxUses = int(input("Enter max uses: ")) if input("Edit max uses? (Y/N) ").upper() == "Y" else weapon.maxUses
                            weapon.type = input("Enter type: ") if input("Edit type? (Y/N) ").upper() == "Y" else weapon.type
                    print("State enemy changed")
                if vertex.event == 5:
                    vertex.item = Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: "))
                    print("State weapon changed")
                if vertex.event == 6:
                    vertex.item = int(input("Enter hp value: "))
                    print("State hp value changed")
                if vertex.event == 7:
                    vertex.item = int(input("Enter uses value: "))
                    print("State uses value changed")
                if vertex.event == 8:
                    vertex.item = input("Enter variable name: ")
                    print("State variable name changed")
            elif choice.lower() == "item":
                if vertex.event == 3:
                    vertex.item = input("Enter item name: ")
                    print("State item name changed")
                elif vertex.event == 4:
                    if isinstance(vertex.item, Entity):
                        weapons = vertex.item.weapons
                    else:
                        weapons = []
                    vertex.item = Entity(input("Enter enemy name: ") if input("Edit name? (Y/N) ").upper() == "Y" else vertex.item.name, int(input("Enter enemy hp: ")) if input("Edit hp? (Y/N) ").upper() == "Y" else vertex.item.hp, int(input("Enter enemy max hp: ")) if input("Edit max hp? (Y/N) ").upper() == "Y" else vertex.item.maxhp, input("Enter enemy type: ") if input("Edit type? (Y/N) ").upper() == "Y" else vertex.item.type, weapons)
                    if input("Edit weapons? (Y/N) ").upper() == "Y":
                        while True:
                            choice = input("Add, remove, or edit weapon? (A/R/E/N) ").upper()
                            if choice != "A" and choice != "R" and choice != "E":
                                break
                            if choice == "A":
                                vertex.item.weapons.append(Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: ")))
                            elif choice == "R":
                                vertex.item.removeWeapon(input("Enter name: "))
                            else:
                                weapon = vertex.item.getWeapon(input("Enter name: "))
                                weapon.name = input("Enter name: ") if input("Edit name? (Y/N) ").upper() == "Y" else weapon.name
                                weapon.damage = int(input("Enter damage: ")) if input("Edit damage? (Y/N) ").upper() == "Y" else weapon.damage
                                weapon.uses = int(input("Enter uses: ")) if input("Edit uses? (Y/N) ").upper() == "Y" else weapon.uses
                                weapon.maxUses = int(input("Enter max uses: ")) if input("Edit max uses? (Y/N) ").upper() == "Y" else weapon.maxUses
                                weapon.type = input("Enter type: ") if input("Edit type? (Y/N) ").upper() == "Y" else weapon.type
                    print("State enemy changed")
                elif vertex.event == 5:
                    vertex.item = Weapon(input("Enter name: ") if input("Edit name? (Y/N) ").upper() == "Y" else vertex.item.name, int(input("Enter damage: ")) if input("Edit damage? (Y/N) ").upper() == "Y" else vertex.item.damage, int(input("Enter uses: ")) if input("Edit uses? (Y/N) ").upper() == "Y" else vertex.item.uses, int(input("Enter max uses: ")) if input("Edit max uses? (Y/N) ").upper() == "Y" else vertex.item.maxUses, input("Enter type: ") if input("Edit type? (Y/N) ").upper() == "Y" else vertex.item.type)
                    print("State weapon changed")
                elif vertex.event == 6:
                    vertex.item = int(input("Enter hp value: "))
                    print("State hp value changed")
                elif vertex.event == 7:
                    vertex.item = int(input("Enter uses value: "))
                    print("State uses value changed")
                elif vertex.event == 8:
                    vertex.item = input("Enter variable name: ")
                    print("State variable name changed")
                else:
                    print("State has no item to modify")
            else:
                print("Unavailable choice")
        elif answer == "delete state":
            if len(vertexStack) > 0:
                graph.removeVertex(graph.vertexes.index(vertex))
                vertex = vertexStack.pop()
                print(f"State deleted; located on state {graph.vertexes.index(vertex)}: {vertex.text}")
            else:
                print("No previous state available to go back to")
        elif answer == "delete state id":
            i = int(input("Enter state id: "))
            if i != graph.vertexes.index(vertex):
                if graph.vertexes[i] in vertexStack:
                    vertexStack.remove(graph.vertexes[i])
                graph.removeVertex(i)
                print(f"State deleted")
            else:
                print("Cannot delete the current state that you're in. Use 'delete state' instead")
        elif answer == "edit path":
            for i in range(len(vertex.edges)):
                print(f"{i}: {vertex.edges[i].toDict()}")
            i = int(input("Enter path id: "))
            choice = input("Enter property (Text, Destination, Lock, Item): ")
            if choice.lower() == "text":
                vertex.edges[i].text = input("Enter prompt: ")
                print("Path text changed")
            elif choice.lower() == "destination":
                vertex.edges[i].destination = int(input("Enter destination id: "))
                print("Path destination changed")
            elif choice.lower() == "lock":
                vertex.edges[i].locked = int(input("Enter lock (0=Unlocked, 1=Locked, 2=EnterLock, 3=ItemUnlock): "))
                print("Path lock changed")
            elif choice.lower() == "item":
                vertex.edges[i].item = input("Enter state item name: ")
                print("Path item changed")
            else:
                print("Unavailable choice")
        elif answer == "add path":
            edgeText = input("Enter path prompt: ")
            edgeLocked = int(input("Enter lock (0=Unlocked, 1=Locked, 2=EnterLock, 3=ItemUnlock): "))
            edgeItem = ""
            if edgeLocked == 3:
                edgeItem = input("Enter path item name: ")
            if input("Create new state? (Y/N) ").upper() == "Y":
                vertexText = input("Enter state prompt: ")
                vertexEvent = int(input("Enter event (0=None, 1=Win, 2=Loss, 3=Item, 4=Battle, 5=Weapon, 6=Heal, 7=Repair 8=Input): "))
                vertexItem = ""
                if vertexEvent == 3:
                    vertexItem = input("Enter state item name: ")
                if vertexEvent == 4:
                    weapons = []
                    vertexItem = Entity(input("Enter enemy name: "), int(input("Enter enemy hp: ")), int(input("Enter enemy max hp: ")), input("Enter enemy type: "), weapons)
                    while True:
                        choice = input("Add, remove, or edit weapon? (A/R/E/N) ").upper()
                        if choice != "A" and choice != "R" and choice != "E":
                            break
                        if choice == "A":
                            weapons.append(Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: ")))
                        elif choice == "R":
                            vertexItem.removeWeapon(input("Enter name: "))
                        else:
                            weapon = vertexItem.getWeapon(input("Enter name: "))
                            weapon.name = input("Enter name: ") if input("Edit name? (Y/N) ").upper() == "Y" else weapon.name
                            weapon.damage = int(input("Enter damage: ")) if input("Edit damage? (Y/N) ").upper() == "Y" else weapon.damage
                            weapon.uses = int(input("Enter uses: ")) if input("Edit uses? (Y/N) ").upper() == "Y" else weapon.uses
                            weapon.maxUses = int(input("Enter max uses: ")) if input("Edit max uses? (Y/N) ").upper() == "Y" else weapon.maxUses
                            weapon.type = input("Enter type: ") if input("Edit type? (Y/N) ").upper() == "Y" else weapon.type
                if vertexEvent == 5:
                    vertexItem = Weapon(input("Enter name: "), int(input("Enter damage: ")), int(input("Enter uses: ")), int(input("Enter max uses: ")), input("Enter type: "))
                if vertexEvent == 6:
                    vertexItem = int(input("Enter hp value: "))
                if vertexEvent == 7:
                    vertexItem = int(input("Enter uses value: "))
                if vertexEvent == 8:
                    vertexItem = input("Enter variable name: ")
                v = Vertex(vertexText, vertexEvent, vertexItem)
                graph.addVertex(v)
                i = graph.vertexes.index(v)
                print(f"State {i} created")
            else:
                i = int(input("Enter destination id: "))
            vertex.edges.append(Edge(edgeText, i, edgeLocked, edgeItem))
            print("Path added")
            if input("Go to destination state? (Y/N) ").upper() == "Y":
                vertexStack.append(vertex)
                vertex = graph.vertexes[i]
                print(f"Located on state {i}: '{vertex.text}'")
        elif answer == "delete path":
            for i in range(len(vertex.edges)):
                print(f"{i}: '{vertex.edges[i].text}'")
            i = int(input("Enter path id: "))
            destination = vertex.edges[i].destination
            vertex.edges.pop(i)
            print("Path deleted")
            if input("Delete destination state? (Y/N) ").upper() == "Y":
                if graph.vertexes[destination] in vertexStack:
                    vertexStack.remove(graph.vertexes[destination])
                graph.removeVertex(destination)
                print("State deleted")
        elif answer == "traverse":
            for i in range(len(vertex.edges)):
                print(f"{i}: '{vertex.edges[i].text}'")
            i = vertex.edges[int(input(f"Enter path id: "))].destination
            vertexStack.append(vertex)
            vertex = graph.vertexes[i]
            print(f"Located on state {i}: '{vertex.text}'")
        elif answer == "add type":
            graph.addType(input("Enter type: "))
            print("Type added")
        elif answer == "remove type":
            print("Type removed") if graph.removeType(input("Enter type: ")) else print("Type does not exist")
        elif answer == "types":
            print(graph.strengths)
        elif answer == "add strength":
            graph.addStrength(input("Enter type to edit: "), input("Enter strength: "))
            print("Strength for type added")
        elif answer == "remove strength":
            print("Strength for type removed") if graph.removeStrength(input("Enter type to edit: "), input("Enter strength: ")) else print("Type or strength does not exist")
        elif answer == "back":
            if len(vertexStack) > 0:
                vertex = vertexStack.pop()
                print(f"Located on state {graph.vertexes.index(vertex)}: '{vertex.text}'")
            else:
                print("No previous state available to go back to")
        elif answer == "help":
            print(helpString)
        elif answer == "save":
            graph.save(file)
            print("File saved")
        elif answer == "exit":
            break
    except:
        print("An issue occurred")

graph.save(file)

# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = 'Alejandro Garcia Carballo, William Gregorio Cruz Herrera, Sirlyn Graciela Aredo Pelaez'
__group__ = 'DV15.03'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
import math


class Node:
    # __init__ Constructor of Node Class.
    def __init__(self, station, father):
        """
        __init__: 	Constructor of the Node class
        :param
                - station: STATION information of the Station of this Node
                - father: NODE (see Node definition) of his father
        """

        self.station = station  # STATION information of the Station of this Node
        self.g = 0  # REAL cost - depending on the type of preference -
        # to get from the origin to this Node
        self.h = 0  # REAL heuristic value to get from the origin to this Node
        self.f = 0  # REAL evaluate function
        if father == None:
            self.parentsID = []
        else:
            self.parentsID = [father.station.id]
            self.parentsID.extend(father.parentsID)  # TUPLE OF NODES (from the origin to its father)
        self.father = father  # NODE pointer to his father
        self.time = 0  # REAL time required to get from the origin to this Node
        # [optional] Only useful for GUI
        self.num_stopStation = 0  # INTEGER number of stops stations made from the origin to this Node
        # [optional] Only useful for GUI
        self.walk = 0  # REAL distance made from the origin to this Node
        # [optional] Only useful for GUI
        self.transfers = 0  # INTEGER number of transfers made from the origin to this Node
        # [optional] Only useful for GUI

    def setEvaluation(self):
        """
        setEvaluation: 	Calculates the Evaluation Function. Actualizes .f value

        """
        self.f = self.h + self.g

    def setHeuristic(self, typePreference, node_destination, city):
        """"
        setHeuristic: 	Calculates the heuristic depending on the preference selected
        :params
                - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: PATH of the destination station
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        """

        if typePreference == 0:  # Si recibimos un 0 como tipo de preferencia no debemos aplicar ninguna heuristica. Por lo tanto devolvemos 0
            self.h = 0

        elif typePreference == 1:  # Si recibimos un 1 como tipo de preferencia, debemos aplicar la formula de la distancia euclidiana y dividirla entre la velocidad
            self.h = math.sqrt(pow((node_destination.station.x - self.station.x), 2) + pow(
                (node_destination.station.y - self.station.y), 2)) / city.max_velocity

        elif typePreference == 2:  #
            self.h = math.sqrt(pow((node_destination.station.x - self.station.x), 2) + pow(
                (node_destination.station.y - self.station.y), 2))
        elif typePreference == 3:  # Si recibimos un 3, debemos hacer el minimo de transbordos, lo que implica que debemos cambiar de linea el minimo de veces
            if self.station.line != node_destination.station.line:
                self.h = 1
            else:
                self.h = 0
        elif typePreference == 4:  # Si al movernos seguimos en la misma estacion, no sera una parada sino un transbordo
            if self.station.x != node_destination.station.x or self.station.y != node_destination.station.y:
                self.h = 1
            else:
                self.h = 0
        else:
            self.h = None

    def setRealCost(self, costTable):
        """
        setRealCost: 	Calculates the real cost depending on the preference selected
        :params
                 - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
        """

        # Consideramos el nodo actual como el nodo hijo
        nodo_hijo = self
        self.g = 0
        """print "______________NUEVA EJECUCION______________"
        print "***** COST TABLE *********"
        print costTable"""
        # Iremos desde el hijo, subiendo hacia arriba del arbol, pasando por los padres, para ir sumando sus costes, acumularlos y obtener el coste real
        while nodo_hijo.father != None:
            """print "______________NODO HIJO______________"
            print nodo_hijo.station.id

            print "_____________ NODO PADRE _____________"
            print nodo_hijo.father.station.id"""
            self.g += costTable[nodo_hijo.station.id][nodo_hijo.father.station.id]
            nodo_hijo = nodo_hijo.father


def Expand(fatherNode, stationList, typePreference, node_destination, costTable, city):
    """
       Expand: It expands a node and returns the list of connected stations (childrenList)
       :params
               - fatherNode: NODE of the current node that should be expanded
               - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
               - typePreference: INTEGER Value to indicate the preference selected:
                               0 - Null Heuristic
                               1 - minimum Time
                               2 - minimum Distance
                               3 - minimum Transfers
                               4 - minimum Stops
               - node_destination: NODE (see Node definition) of the destination
               - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                            cost can be in terms of any preference.
               - city: CITYINFO with the information of the city (see CityInfo class definition)
       :returns
               - childrenList:  LIST of the set of child Nodes for this current node (fatherNode)

   """

    #Lista donde anadiremos todos los hijos
    childList = []

    #Recorremos todos los hijos del padre, que son las conexiones a las que puede llegar, las cuales estan en destinationDic
    for child in fatherNode.station.destinationDic:
        #Debemos crear el Node que queremos anadir, los hijos son objetos Node, asi que debemos construirlos con los datos que nos envian por parametro de esta funcion
        #la destination es igual a la ID de la estacion, asi que buscaremos en la lista de las estaciones la estacion con la misma ID que nuestro nodo hijo
        #y se la pasaremos al constructor junto al nodo padre
        for station in stationList:
            if station.id == child:
                child = Node(station, fatherNode)
                child.setRealCost(costTable)
                child.setHeuristic(typePreference, node_destination, city)
                child.setEvaluation()

                # parentsID
                #child.parentsID = list(fatherNode.parentsID)
                #child.parentsID.append(fatherNode.station.id)

                # time
                child.time = fatherNode.time + setCostTable(1, stationList, city)[fatherNode.station.id][station.id]

                # walk
                child.walk = fatherNode.walk + setCostTable(2, stationList, city)[fatherNode.station.id][station.id]

                # Transfers
                child.transfers = fatherNode.transfers + setCostTable(3, stationList, city)[fatherNode.station.id][station.id]
                # Stops
                child.num_stopStation = fatherNode.num_stopStation + setCostTable(4, stationList, city)[fatherNode.station.id][station.id]

                childList.append(child)


    return childList


def RemoveCycles(childrenList):
    """
        RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
        :params
                - childrenList: LIST of the set of child Nodes for a certain Node
        :returns
                - listWithoutCycles:  LIST of the set of child Nodes for a certain Node which not includes cycles
    """

    listasinCiclos = []
    for i in childrenList:
        if not i.station.id in i.parentsID:
            listasinCiclos.append(i)
    return listasinCiclos


def RemoveRedundantPaths(childrenList, nodeList, partialCostTable):
    """
        RemoveRedundantPaths:   It removes the Redundant Paths. They are not optimal solution!
                                If a node is visited and have a lower g in this moment, TCP is updated.
                                In case of having a higher value, we should remove this child.
                                If a node is not yet visited, we should include to the TCP.
        :params
                - childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
                                or not.
                - nodeList : LIST of NODES to be visited
                - partialCostTable: DICTIONARY of the minimum g to get each key (Node) from the origin Node
        :returns
                - childrenList: LIST of NODES, set of childs without rendundant path.
                - nodeList: LIST of NODES to be visited updated (without redundant paths)
                - partialCostTable: DICTIONARY of the minimum g to get each key (Node) from the origin Node (updated)
    """

    childrensToRemove = []
    nodesToRemove = []

    for children in childrenList:
        if not partialCostTable or not partialCostTable.has_key(children.station.id): #Si el diccionario esta vacio
            partialCostTable[children.station.id] = children.g
        else: #Si el diccionario no esta vacio
            #if partialCostTable.has_key(children.station.id):
            if children.g < partialCostTable[children.station.id]:
                partialCostTable[children.station.id] = children.g
            else:
                if children.g > partialCostTable[children.station.id]: #El coste del nodo de entrada es mayor que el que tenemos en partialCostTable
                    #childrenList.remove(children)
                    childrensToRemove.append(children)

    for node in nodeList:
        if not partialCostTable or not partialCostTable.has_key(node.station.id):
            partialCostTable[node.station.id] = node.g
        else:
            #if partialCostTable.has_key(node.station.id):
            if node.g < partialCostTable[node.station.id]:
                partialCostTable[node.station.id] = node.g
            else:
                if node.g > partialCostTable[node.station.id]:
                    #nodeList.remove(node)
                    nodesToRemove.append(node)

    for children in childrensToRemove:
        childrenList.remove(children)

    for node in nodesToRemove:
        nodeList.remove(node)


    return childrenList, nodeList, partialCostTable


def sorted_insertion(nodeList, childrenList):
    """ Sorted_insertion: 	It inserts each of the elements of childrenList into the nodeList.
                            The insertion must be sorted depending on the evaluation function value.

        : params:
            - nodeList : LIST of NODES to be visited
            - childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
                                or not.
        :returns
                - nodeList: sorted LIST of NODES to be visited updated with the childrenList included
    """

    """En el caso de que nos den una lista de nodos a visitar vacia, necesitamos poner almenos el primer
       elemento de la lista de hijos para poder iniciar el algoritmo comparando las funciones de costes. Tambien inicializamos el valor del
       mayor coste como el ultimo elemento de la lista de nodos, ya que al estar ordenada el ultimo elemento siempre sera el de mayor coste"""

    if nodeList:
        mayorCoste = nodeList[-1].f  # Ya que la lista nos viene ordenada por defecto, este sera el coste mayor que hay actualmente en la lista
    else:
        nodeList.append(childrenList[0])
        mayorCoste = nodeList[-1].f

    """Comparamos cada funcion de coste de los hijos con la lista de nodos, en caso de que sea menor lo insertaremos en esa posicion.
    En caso contrario compararemos con el coste mayor"""
    for children in childrenList:
        posicioNode = 0

        for node in nodeList:
            if not children in nodeList:  # comprobamos que el nodo no este ya insertado en la lista de nodos
                if children.f < node.f:
                    nodeList.insert(posicioNode, children)
                if children.f >= mayorCoste:
                    nodeList.append(children)
                    mayorCoste = children.f

            posicioNode += 1

    return nodeList

def setCostTable(typePreference, stationList, city):
    """
    setCostTable :      Real cost of a travel.
    :param
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
            - city: CITYINFO with the information of the city (see CityInfo class definition)
    :return:
            - costTable: DICTIONARY. Relates each station with their adjacency an their g, depending on the
                                 type of Preference Selected.
    """
    dict = {}

    if typePreference == 0:
        return city.adjacency
    elif typePreference == 1:
        #Para cada una de las estaciones
        for station in stationList:
            #Creamos un diccionario con clave igual a la ID de la estacion
            dict[station.id] = {}
            """El destinationDic contiene el tiempo real entre estacion y estacion en forma de diccionario,
             donde esta como clave la ID de la estacion y valor el coste {2: 9.054757524726}
             Lo que haremos sera asociar todas las ID de las estaciones como clave en otro diccionario, con el destinationDic de
             los nodos a los que esta conectado como valor { 1: {2: 9.054757524726} }"""
            for j in station.destinationDic:
                time = station.destinationDic[j]
                dict[station.id][j] = time

    elif typePreference == 2:

        # Para cada una de las estaciones

        for station in stationList:
            # Creamos un diccionario con clave igual a la ID de la estacion
            dict[station.id] = {}
            for j in station.destinationDic: #Debemos mirar la distancia real entre las estaciones. No nos dan la distancia como tal, pero tenemos el tiempo y las velocidades. Asi que podemos calcualr la distancia como d=t*v
                time = station.destinationDic[j]
                velocidad = city.velocity_lines[station.line-1]
                distancia = time * velocidad
                if station.x != stationList[j-1].x or station.y != stationList[j-1].y:
                    dict[station.id][j] = distancia
                else:
                    dict[station.id][j] = 0
    elif typePreference == 3:
        for station in stationList:
            dict[station.id] = {}
            for j in station.destinationDic: #miramos si para cada conexion de la estacion, cambian de linea o no. En casi afirmativo habra transbordo y devolvemos 1. En caso contrario devolvemos 0.
                if stationList[j-1].line != station.line:
                    dict[station.id][j] = 1
                else:
                    dict[station.id][j] = 0
    elif typePreference == 4:
        for station in stationList:
            dict[station.id] = {}
            for j in station.destinationDic:
                if stationList[j-1].line == station.line: #al contrario que la anterior, consideraremos que es una parada si no es un transbordo, es decir, si no cambiamos de linea.
                    dict[station.id][j] = 1
                else:
                    dict[station.id][j] = 0
    else:
        print "Opcion no disponible"

    return dict


def coord2station(coord, stationList):
    """
    coord2station :      From coordinates, it searches the closest station.
    :param
            - coord:  LIST of two REAL values, which refer to the coordinates of a point in the city.
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)

    :return:
            - possible_origins: List of the Indexes of the stationList structure, which corresponds to the closest
            station
    """

    possible_origins = []
    distancia = -1

    for station in stationList:

        distanciaTemp = math.sqrt(pow((coord[0] - station.x), 2) + pow((coord[1] - station.y), 2))

        if distanciaTemp < distancia or distancia == -1:
            distancia = distanciaTemp
            estacion = station.id - 1
            possible_origins = []
            possible_origins.append(estacion)

        if distanciaTemp == distancia and (station.id-1) not in possible_origins:
            distancia = distanciaTemp
            estacion = station.id - 1
            possible_origins.append(estacion)

    return possible_origins

def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference, city, flag_redundants):
    """
     AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
     INPUTS:
            - stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
            - coord_origin: TUPLE of two values referring to the origin coordinates
            - coord_destination: TUPLE of two values referring to the destination coordinates
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - city: CITYINFO with the information of the city (see CityInfo class definition)
			- flag_redundants: [0/1]. Flag to indicate if the algorithm has to remove the redundant paths (1) or not (0)

    OUTPUTS:
            - time: REAL total required time to make the route
            - distance: REAL total distance made in the route
            - transfers: INTEGER total transfers made in the route
            - stopStations: INTEGER total stops made in the route
            - num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
            - depth: INTEGER depth of the solution
            - visitedNodes: LIST of INTEGERS, IDs of the stations corresponding to the visited nodes
            - idsOptimalPath: LIST of INTEGERS, IDs of the stations corresponding to the optimal path
            (from origin to destination)
            - min_distance_origin: REAL the distance of the origin_coordinates to the closest station
            - min_distance_destination: REAL the distance of the destination_coordinates to the closest station



            EXAMPLE:
            return optimalPath.time, optimalPath.walk, optimalPath.transfers,optimalPath.num_stopStation,
            len(expandedList), len(idsOptimalPath), visitedNodes, idsOptimalPath, min_distance_origin,
            min_distance_destination
    """

    typePreference = int(typePreference)
    lista_expandidos = [] #guardaremos los nodos que obtenemos de las expansiones
    cost_table = {} #guardaremos la cost table
    lista_nodos_visitar = [] #guardaremos la lista de nodos a visitar
    lista_nodos_visitados = []
    estacion_origen = stationList[coord2station(coord_origin, stationList)[0]]
    estacion_destino = stationList[coord2station(coord_destination, stationList)[0]]
    numero_expansiones = 0

    nodo_origen = Node(estacion_origen, None)
    nodo_destino = Node(estacion_destino, None)
    cost_table = setCostTable(typePreference, stationList, city)

    lista_nodos_visitar.append(nodo_origen)#comprobamos que el origen no sea el destino

    # para eliminar caminos redundantes necesitamos la tabla de costes parciales
    tabla_costes_parciales = {}
    tabla_costes_parciales[lista_nodos_visitar[0].station.id] = 0

    while lista_nodos_visitar[0].station.id != nodo_destino.station.id:

        if lista_nodos_visitar[0].station.id not in lista_nodos_visitados:
            lista_nodos_visitados.append(lista_nodos_visitar[0].station.id)

        lista_expandidos = Expand(lista_nodos_visitar[0], stationList, typePreference, nodo_destino, cost_table, city)  # expandir
        numero_expansiones += 1
        lista_expandidos = RemoveCycles(lista_expandidos)  # eliminamos ciclos

        lista_nodos_visitar = list(lista_nodos_visitar[1:])

        if len(lista_expandidos) > 0:
            lista_nodos_visitar = sorted_insertion(lista_nodos_visitar,lista_expandidos)  # anadimos de forma ordenada los nodos expandidos

        if (flag_redundants == 1):
            lista_expandidos, lista_nodos_visitar, tabla_costes_parciales = RemoveRedundantPaths(lista_expandidos, lista_nodos_visitar, tabla_costes_parciales)

    min_distance_origin =  math.sqrt(pow((nodo_origen.station.x - coord_origin[0]), 2) + pow((nodo_origen.station.y - coord_origin[1]), 2))
    min_distance_destination = math.sqrt(pow((nodo_destino.station.x - coord_destination[0]), 2) + pow((nodo_destino.station.y - coord_destination[1]), 2))
    nodo_encontrado = lista_nodos_visitar[0]
    idsOptimalPath = list(lista_nodos_visitar[0].parentsID[::-1])
    idsOptimalPath.append(lista_nodos_visitar[0].station.id)

    print "************************"
    print nodo_encontrado.g
    print nodo_encontrado.time
    print nodo_encontrado.walk
    print nodo_encontrado.transfers
    print nodo_encontrado.num_stopStation
    print "************************"

    return nodo_encontrado.time, nodo_encontrado.walk, nodo_encontrado.transfers, nodo_encontrado.num_stopStation, numero_expansiones, len(idsOptimalPath), lista_nodos_visitados, idsOptimalPath, min_distance_origin, min_distance_destination
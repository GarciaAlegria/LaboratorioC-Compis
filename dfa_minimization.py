import pydotplus


def create_dfa_graph(states, acceptance_states, transitions, start_state):

    start_state = start_state[0]

    # Crear una representación del DFA en formato DOT
    dot = pydotplus.Dot()
    dot.set_rankdir("LR")  # Utilizar 'TB' para un diseño de arriba hacia abajo
    dot.set_prog("neato")

    # Crea nodos para cada estado
    state_nodes = {}
    num = 0
    for state in states:
        node = pydotplus.Node(state)
        node.set_shape("circle")

        if start_state == state:
            node.set_name("Start")
            node.set_shape("circle")
            node.set_style("filled")
        else:
            node.set_name(str(num))

        for final_state in acceptance_states:
            if final_state == state:
                node.set_name(str(num))
                node.set_shape("doublecircle")

        node.set_fontsize(12)  # Establece el tamaño de fuente
        node.set_width(0.6)  # Establece el ancho deseado
        node.set_height(0.6)  # Establece la altura deseada
        state_nodes[state] = node
        dot.add_node(node)
        num += 1

    # Agrega transiciones como arcos
    for (source, symbol, target) in transitions:
        edge = pydotplus.Edge(
            state_nodes[str(source)], state_nodes[str(target)], label=symbol)
        dot.add_edge(edge)

    return dot

def exec(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion, link):

    new_transitions = []

    partitions = {frozenset(state for state in estados if state in estados_aceptacion), frozenset(state for state in estados if state not in estados_aceptacion),}

    def encontrar_particion(state, particiones):
        for particion in particiones:
            if state in particion:
                return particion
        return None
    
    def encontrar_transiciones(estado, symbol):
        for transi in transiciones:
            if transi[0] == estado and transi[1] == symbol:
                return transi[2]
        return None
    
    finished = True
    while finished:
        new_partitions = set()
        finished = False
        for partition in partitions:
            partition_mapping = {}
            for state in partition:
                transicion_signature = tuple(
                    encontrar_particion(encontrar_transiciones(state, symbol), partitions)
                    for symbol in alfabeto
                )
                if transicion_signature not in partition_mapping:
                    partition_mapping[transicion_signature] = set()
                partition_mapping[transicion_signature].add(state)
            
            if len(partition_mapping) > 1:
                finished = True
                new_partitions.update(
                    frozenset(subset) for subset in partition_mapping.values()
                )
            else:
                new_partitions.add(partition)
        
        partitions = new_partitions

    new_states = [partition for partition in partitions if partition != frozenset()]

    old_to_new = {}
    for new_state in new_states:
        for old_state in estados:
            if old_state in new_state:
                old_to_new[old_state] = new_state

    def find_if_duplicate(state, symbol, transiciones):
        for transi in transiciones:
            if transi[0] == state and transi[1] == symbol:
                return True
        return False

    for new_state in new_states:
        for old_state in estados:
            if old_state in new_state:
                for tran in transiciones:
                    if old_state == tran[0]:
                        if not find_if_duplicate(new_state, tran[1], new_transitions):
                            new_transitions.append((new_state, tran[1], old_to_new[tran[2]]))

    new_estado_inicial = list(str(old_to_new[estado]) for estado in estado_inicial)
    new_estados_aceptacion = list(str(old_to_new[state]) for state in estados_aceptacion)
    new_states = list(str(state) for state in new_states)
    transit = [(str(tran[0]), tran[1], str(tran[2])) for tran in new_transitions]

    pydotplus.find_graphviz()

    # Crear el grafo del DFA minimizado
    graph = create_dfa_graph(new_states, new_estados_aceptacion, transit, new_estado_inicial)

    # Guardar o mostrar el gráfico
    graph.write_png(link)  # Guardar archivo PNG

    return new_states, alfabeto, transit, new_estado_inicial[0], new_estados_aceptacion

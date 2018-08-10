"""A set of utilities to work with xAPI and other data formats."""


def graph2gephi(nodes, adjancy, filename='test.gdf'):
    """
    Formats the adjancy list to `.gdf` (Gephi file)

    Arguments
    ---------
    nodes: list[str]
        List of agent's names

    adjancy: dict(str: [Agents])
        Adjancy lists indexed by agent name (agent_names -> agents)
    """
    with open(filename, 'w') as f:
        f.write('nodedef> name VARCHAR, role VARCHAR\n')
        for name, role in nodes.items():
            f.write("{}, {}\n".format(name, role))
        f.write('edgedef> node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n')
        for parent, children in list(adjancy.items()):
            for child in children:
                weight = 1 if nodes[parent] == 'group' else 3
                f.write("{}, {}, {}\n".format(parent, child, weight))


def get_active_agents(statements):
    """
    Takes a list of statements and returns a reference users list.

    Arguments
    ---------
    nodes: list[statements]
        List of statements

    Returns
    -------
    users_list: list[str]
        List of users
    """
    return {s['actor'] for s in statements}


def filter_by_users(nodes, adjancy, active_agents):
    """
    Takes a list of nodes, an adjancy list. Remove the non referenced
    users from the passed user reference list.

    Arguments
    ---------
    nodes: set[str]
        List of agent's names.

    adjancy: dict(str: [Agents])
        Adjancy lists indexed by agent name (agent_names -> agents).

    user_reference: set[str]
        The reference set of users.

    Returns
    -------
    nodes_clean:
        The filtered nodes set.

    nodes_clean:
        The filtered adjancy list.
    """
    nodes_keep = set()
    for name, role in nodes.items():
        if name in active_agents and role == 'user:eleve':
            nodes_keep.add(name)

    for node_name in dict(adjancy).keys():
        if contains_active_student(node_name, adjancy, nodes, nodes_keep):
            nodes_keep.add(node_name)

    nodes_clean = {k: v for k, v in nodes.items() if k in nodes_keep}
    adjancy_clean = {k: v.intersection(nodes_keep) for k, v in adjancy.items()
                     if k in nodes_keep}
    # TODO: Could be interesting to keep the inactive users for plotting.

    return nodes_clean, adjancy_clean


def contains_active_student(node_name, adjancy, roles, keep):
    """
    Finds if there is a student in the children of `node_name`

    Arguments
    ---------
    node_name: str
        Name of the current node

    adjancy: dict(str: [str])
        Adjancy list of agents

    roles: dict(str: str)
        Role of the agents

    Return
    ------
    True or False
    """
    if node_name in keep:
        return True
    for child_name in adjancy[node_name]:
        if contains_active_student(child_name, adjancy, roles, keep):
            return True
    return False

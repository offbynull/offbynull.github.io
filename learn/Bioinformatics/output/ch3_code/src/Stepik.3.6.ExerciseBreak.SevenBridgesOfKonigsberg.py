#     U
# UM1   UM2   UR1
#     M       MR1    R
# DM1   DM2   DR1
#     D
nodes = {
    'D': ['DM1', 'DM2', 'DR1'],
    'U': ['UM1', 'UM2', 'UR1'],
    'R': ['DR1', 'UR1', 'MR1'],
    'M': ['DM1', 'DM2', 'UM1', 'UM2', 'MR1'],
    'DM1': ['D', 'M'],
    'DM2': ['D', 'M'],
    'UM1': ['U', 'M'],
    'UM2': ['U', 'M'],
    'UR1': ['U', 'R'],
    'MR1': ['M', 'R'],
    'DR1': ['D', 'R']
}

def walk(path, bridge_path, city_path):
    if len(bridge_path) == 7 and path[0] == path[-1]:  # crosses all bridges exactly once and ends up in the same city it started in?
        print(f'{path}')

    n = path[-1]
    for child_n in nodes[n]:
        is_bridge = len(child_n) == 3
        is_city = len(child_n) == 1
        if is_bridge and child_n in bridge_path:  # crossed the bridge before? don't allow
            continue
        if is_city and len(city_path) > 0 and city_path[-1] == child_n:  # went from a city onto a bridge but walked backwards back to the city? don't allow
            continue

        if is_city:
            city_path.append(child_n)
        elif is_bridge:
            bridge_path.append(child_n)
        path.append(child_n)
        walk(path, bridge_path, city_path)
        path.pop()
        if is_city:
            city_path.pop()
        if is_bridge:
            bridge_path.pop()


walk(['D'], [], ['D'])
walk(['U'], [], ['U'])
walk(['R'], [], ['R'])
walk(['M'], [], ['M'])
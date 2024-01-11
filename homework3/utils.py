import numpy as np
import pandas as pd


def create_problem_grid():
    cooking_chef_states_tuples = {}
    cooking_chef_tuples_states = {}
    count = 0
    for i in range(1, 9):
        for j in [x for x in range(1, 10) if x != 5]:
            cooking_chef_states_tuples[count] = (i, j)
            cooking_chef_tuples_states[(i, j)] = count
            count += 1
    return cooking_chef_states_tuples, cooking_chef_tuples_states


# Function to check the condition for extra space
def needs_extra_space(tuple_value):
    return tuple_value[1] == 4


def print_states(dict_view=False):
    cooking_chef_states_tuples, cooking_chef_tuples_states = create_problem_grid()
    # Generate the rows in a more concise way using slicing and a loop
    rows = [list(range(i, i + 8)) for i in range(56, -1, -8)]

    for row in rows:
        for i in row:
            if dict_view:
                print(f" {cooking_chef_states_tuples[i]} ", end="")
                if needs_extra_space(cooking_chef_states_tuples[i]):
                    print("        ", end="")
            else:
                print(f" {i:<2} ", end="")
                if needs_extra_space(cooking_chef_states_tuples[i]):
                    print("    ", end="")

        # Simplify the condition for adding extra newlines
        print("\n\n" if row == rows[3] else "")
    print()


# metodo che ritorna la conversione della struttura dati dict `mapping` in numpy array
def convert_to_numpy_array(mapping: dict, s: np.ndarray, a: np.ndarray):
    count = 0
    for i in sorted(list(mapping.keys())):
        if i != count:
            raise RuntimeError("Struttura non valida")
        count += 1
    array = np.zeros(shape=(len(s), len(a)), dtype=np.float64)
    for s, actions in mapping.items():
        prob = 1 / len(actions)
        for a in actions:
            array[s, a] = prob
    return array


# metodo che ritorna un DataFrame che corrisponde alla matrice
# delle transizioni P rispetto all'azione `action`.
#
# `action`: int, parametro che identifica l'azione da cui stampare
# una matrice che contiene tutte le coppie S x S' per l'azione
# specificata `action`
#
# return: pd.DataFrame, struttura dati che corrisponde alla matrice
# delle transizioni P rispetto all'azione specificata `action`
def print_transitions_matrix(p:np.ndarray, action=None):
    df = pd.DataFrame(p[action])

    df["Stati"] = df.index
    df["Stati"] = "s" + df["Stati"].astype(str)
    df.set_index("Stati", inplace=True)
    df.rename(columns=lambda x: f"s{x}", inplace=True)

    return df
from typing import List, Optional, Any
from itertools import combinations


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:

    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        """
        this method diagnose a patient using a decision tree and a list of symptoms.
        the method returns the correct illness after checking the correlating symptoms.
        :param symptoms: a list of symptoms the patient is showing. it does so recursively.
        :return: the disease of the patient
        """

        if self._is_leaf(self.root):
            return self.root.data

        if self.root.data in symptoms:  # the patient is showing the symptom in the decision tree
            if self.root.positive_child:
                return Diagnoser(self.root.positive_child).diagnose(symptoms)
        if self.root.negative_child:
            return Diagnoser(self.root.negative_child).diagnose(symptoms)
        else:
            return self.root.data

    def calculate_success_rate(self, records: List[Record]) -> float:
        """
        this method checks what is the percentage successful diagnoses in a record list
        :param records: alist of Record objects
        :return: the success rate
        """
        successes = 0
        if not records:  # throws an error if the records list is empty
            raise ValueError("The record list is empty")
        for record in records:
            if record.illness == self.diagnose(record.symptoms):
                successes += 1
        return successes / len(records)  # returns the percentage of successes out of all the records checked

    def _is_leaf(self, node: Node) -> bool:
        """
        checks if a node is a leaf, aka it has no children
        :param node: a node to be checked
        :return: True if the node is a leaf. False otherwise.
        """
        return (not node.positive_child) and (not node.negative_child)

    def _leaf_dictionary(self, root, leaf_dict=None):
        """
        this method returns a dictionary of all the leaf values in a tree and the number of their appearances
        :param root: the root Node of the binary tree
        :param leaf_dict: a dictionary of all the leaves values and the number of time their value appears in the tree
        :return: the complete leaf_dict
        """
        if self._is_leaf(root):
            if root.data in leaf_dict:
                leaf_dict[root.data] += 1
                return
            else:
                leaf_dict[root.data] = 1
                return
        self._leaf_dictionary(root.positive_child, leaf_dict)
        self._leaf_dictionary(root.negative_child, leaf_dict)
        return leaf_dict

    def all_illnesses(self) -> List[str]:
        """
        returns a sorted list of all the illnesses by their prevalence. this method uses the leaf_dictionary
        to create a dictionary of the values of all the leaves in the tree.
        :return: a sorted list of all the illnesses in the tree
        """

        illness_dict = self._leaf_dictionary(self.root, {})
        sorted_dict = {illness: val for illness, val in sorted(illness_dict.items(), reverse=True, key=lambda x: x[1])}
        return [illness for illness in sorted_dict if illness]

    def paths_to_illness(self, illness: Optional[str]) -> List[List[bool]]:
        """
        this method returns all the paths from the root to an illness (on a leaf). it uses backtracking.
        :param illness: the illness to be searched
        :return: a list of lists, each containing bools describing the choice path.
        """

        def backtrack_to_illness(illness: str, node: Node, all_paths_to_illness: list, current_path: list):
            """
            helper function for path_to_illness, it creates a list containing all the valid paths to an illness.
            It is a backtracking algorithm, each time a complete path is found it gets appended to the
            list of valid paths

            :param illness: the illness for which we search a path
            :param node: a specific node that s being checked each iteration
            :param all_paths_to_illness: a list containing ll the valid paths
            :param current_path: the current path that is being checked
            :return: all_paths_to_illness
            """

            if node.data == illness:
                all_paths_to_illness.append(current_path[:])  # appends the current path if a complete path was found
                return

            if self._is_leaf(node):  # returns an empty list for a leaf that doesn't contain the illness
                return []

            current_path.append(True)
            backtrack_to_illness(illness, node.positive_child, all_paths_to_illness, current_path)
            current_path.pop()  # disposing of a bad path

            current_path.append(False)
            backtrack_to_illness(illness, node.negative_child, all_paths_to_illness, current_path)
            current_path.pop()  # disposing of a bad path

            return all_paths_to_illness

        all_paths_to_illness = backtrack_to_illness(illness, self.root, [], [])

        if all_paths_to_illness == [[]]:
            return []
        return all_paths_to_illness

    def _identical_trees(self,tree1: Node ,tree2: Node) -> bool:

        if (not tree1) and (not tree2):  # both trees are empty
            return True

        if tree1 and tree2:  # both trees are not empty
            return (tree1.data == tree2.data) and self._identical_trees(tree1.positive_child,tree2.positive_child) and \
                   (self._identical_trees(tree1.negative_child, tree2.negative_child))

        return False  # one of the trees is empty the other is not.


    def minimize(self, remove_empty=False):

        def _minimize_helper(node, previous_node=None, remove_empty=False):

            if remove_empty:
                if previous_node:
                    if (previous_node.positive_child and not previous_node.negative_child) or \
                            (not previous_node.positive_child and previous_node.positive_child):  # has only one child
                        if previous_node.positive_child:
                            previous_node = previous_node.positive_child
                            return
                        if previous_node.negative_child:
                            previous_node = previous_node.negative_child
                            return

            if not self._is_leaf(node):
                if self._identical_trees(node.positive_child, node.negative_child):
                    previous_node = node
                _minimize_helper(node.positive_child, node, remove_empty)
                _minimize_helper(node.negative_child, node, remove_empty)

            return

        _minimize_helper(self.root, None, remove_empty)


    def printTree(self):
        """
        a function that prints the items in the tree according to their hierarchy.
        used for testing
        :return:
        """

        def _printTree(node, level=0):
            if node:
                _printTree(node.positive_child, level + 1)
                print('  ' * 5 * level + '->', node.data)
                _printTree(node.negative_child, level + 1)

        _printTree(self.root)


def illness_dictionary(records):
    """
    creates a dictionary for all the illnesses in the record list. each illness is paired with the number of times
    it appears in the record list
    :param records: a list or Record objects
    :return: a dictionary of illnesses and their appearances number
    """

    illness_dict = dict()
    for record in records:
        if record.illness in illness_dict:
            illness_dict[record.illness] += 1
        else:
            illness_dict[record.illness] = 1
    return illness_dict


def has_symptom(symptom: str, records: List[Record]) -> List[Record]:
    """
    creates a list of all the records that contain a certain symptom
    :param symptom: a symptom for an illness
    :param records: a list of Record objects
    :return: a list of all the records in which the symptom appears
    """
    return [record for record in records if symptom in record.symptoms]





def list_type_check(list_of_items: List[Any], item_type: Any):
    """
    checks if a list consist of an illegal object of a different type from the item type.
    it raises a ValueError if such object was found.
    :param list_of_items: list consisting of single type of items
    :param item_type: the type of the items in the list
    :return: None
    """

    for item in list_of_items:
        if not isinstance(item, item_type):
            raise TypeError(f"The {list_of_items} list contains an object that is not a {item_type}")


def build_root(root: Node, records: List[Record], symptoms: List[str]):
    if len(symptoms) == 0:  # returning a leaf
        # assigning the most common illness from the record list to the leaf
        if len(records) > 0:
            illness = max(illness_dictionary(records), key=illness_dictionary(records).get)
            root.data = illness
        else:
            root.data = None
        return root

    root.data = symptoms[0]
    positive_records = has_symptom(symptoms[0], records)
    root.positive_child = build_root(Node(None), positive_records, symptoms[1:])
    negative_records = [record for record in records if record not in positive_records]
    root.negative_child = build_root(Node(None), negative_records, symptoms[1:])

    return root

def build_tree(records: List[Record], symptoms: List[str]) -> Diagnoser:
    """
    building a naive Diagnoser tree given alist of records and a list of symptoms.
    the function uses the build_root function in order to create the root for the
    Diagnoser tree
    :param records:
    :param symptoms:
    :return:
    """
    list_type_check(records, Record)
    list_type_check(symptoms, str)

    return Diagnoser(build_root(Node(None), records, symptoms))


def all_symptoms_combinations(symptoms: List[str], length: int) -> List[List[str]]:
    """
    create a list of all the possible combinations of symptoms given a specific length
    :param symptoms: a list of symptoms
    :param length: the length of each combination in the list of possible combinations
    :return: a list of lists of symptoms
    """
    return [combination for combination in combinations(symptoms, length)]


def optimal_tree(records, symptoms, depth) -> Diagnoser:
    """
    creates a tree diagnoser object that has an optimal diagnose success rate. the depth of the tree
    is chosen.
    :param records: a list of record objects
    :param symptoms: a list of symptoms
    :param depth: the maximum depth of the tree
    :return: the tree with the best success rate out of all the possible trees.
    """

    # checking that the lists are valid
    list_type_check(records, Record)
    list_type_check(symptoms, str)

    if len(symptoms) > len(set(symptoms)):  # checks that the symptoms list doesn't contain repeating items
        raise ValueError("the symptom list contains the same symptom twice (or more)")

    if not (0 <= depth <= len(symptoms)):  # an invalid depth size
        raise ValueError("Illegal value for the depth parameter")

    if not depth:  # returning a tree containing a single node with the most common illness from the records
        return Diagnoser(Node(max(illness_dictionary(records), key=illness_dictionary(records).get)))


    symptom_combinations = all_symptoms_combinations(symptoms, depth)
    if () in symptom_combinations:  # returning an empty Diagnoser tree if the combinations list is empty
        return build_tree([], [])

    forest = [build_tree(records, symptom_comb) for symptom_comb in symptom_combinations]
    success_rate_dict = {tree: tree.calculate_success_rate(records) for tree in forest}
    return max(success_rate_dict, key=success_rate_dict.get)


if __name__ == "__main__":
    pass
    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           headache
    #   Yes /     \ No		Yes/	\No
    # covid-19   cold		Cold	Healthy

    # flu_leaf = Node("covid-19", None, None)
    # cold_leaf = Node("cold", None, None)
    # inner_vertex = Node("fever", flu_leaf, cold_leaf)
    # healthy_leaf = Node("healthy", None, None)
    # headache_vertex = Node("headache", cold_leaf, healthy_leaf)
    # root = Node("cough", inner_vertex, headache_vertex)

    #  diagnoser = Diagnoser(root)
    #  records = parse_data("small_data.txt")
    #  symptoms = ["fever", "cough", "fatigue", "headache", "nausea"]
    #  diagnoser = build_tree(records,symptoms)
    #  diagnoser.printTree(diagnoser.root)
    # # print(diagnoser.diagnose(["cough"]))
    #  illnesses = diagnoser.all_illnesses()
    #  print(diagnoser.paths_to_illness(None))
    #  for ill in illnesses:
    #      print(ill, diagnoser.paths_to_illness(ill))
    #
    #  # Simple test
    #  diagnosis = diagnoser.diagnose(["cough"])
    #  if diagnosis == "cold":
    #      print("Test passed")
    #  else:
    #      print("Test failed. Should have printed cold, printed: ", diagnosis)
    #
    #  # Add more tests for sections 2-7 here.
    #
    #
    #  print("most common illness is: ", max(illness_dictionary(records), key= illness_dictionary(records).get))
    #  print(diagnoser.calculate_success_rate(records))
    #  print(has_symptom("cough",records))
    #  print("\n\n\n",optimal_tree(records,symptoms,0).calculate_success_rate(records))
    #
    #  record1 = Record("influenza", ["cough", "fever"])
    #  record2 = Record("cold", ["cough"])
    #  records = [record1, record2]

    # flu_leaf = Node("influenza", None, None)
    # cold_leaf = Node("cold", None, None)
    # inner_vertex = Node("fever", flu_leaf, cold_leaf)
    # healthy_leaf = Node("healthy", None, None)
    # root = Node("cough", inner_vertex, healthy_leaf)
    #
    # diagnozer = Diagnoser(root)
    # diagnozer.printTree()
    # t1 = build_tree(records, ["fever"])
    # t1.printTree()
    # print()
    # t2 = optimal_tree(records, ["cough", "fever"],1)
    # t2.printTree()

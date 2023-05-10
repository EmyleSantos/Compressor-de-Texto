class Node(object):

    def __init__(self, label, code=None, value=None):
        self.label = label
        self.code = code
        self.value = value
        self.child_nodes = None

    # end __init__

    def add_child(self, node):
        if not self.child_nodes:
            self.child_nodes = [node]
        else:
            self.child_nodes.append(node)

    # end add_child

    def get_child(self, key):
        if not self.child_nodes:
            return None

        for i in range(len(self.child_nodes)):
            if key == self.child_nodes[i].label:
                return self.child_nodes[i]
        return None

    # end get_child


# end Node


class Trie(object):

    def insert(self, root, caracter, value):
        root.add_child(Node(caracter, root.value, value))
        return root

    # end insert

    # verifica se uma string esta na arvore e retorna seu ultimo nó em caso afirmativo
    def find_by_label(self, root, symbols):
        if not root:
            return None

        elif root.label == "":
            child = root.get_child(symbols[0])
            return self.find_by_label(child, symbols)

        elif root.label == symbols[0]:
            if len(symbols) > 1:
                child = root.get_child(symbols[1])
                return self.find_by_label(child, symbols[1:])
            else:
                return root

        else:
            #elif root.label != symbols[0]:
            return None

    # end find_by_label

    def find_by_code(self, root, code):
        if not root:
            return None

        if root.value == code:
            return root

        if root.child_nodes is not None:
            for child in root.child_nodes:
                if child.code < code:
                    node = self.find_by_code(child, code)
                    if node is not None:
                        return node
        else:
            return None

    # end find_by_label

    def get_text(self, root, prefix, output):
        if not root:
            return output

        if root.label == "":
            prefix = ""

        prefix += root.label

        if root.label != "" and root.code is not None:
            output.append([root.value, root.code, prefix])

        if root.child_nodes is not None:
            for node in root.child_nodes:
                self.get_text(node, prefix, output)

        return output

    # end get_text

    def get_nodes(self, root, output):
        if not root:
            return None

        if root.label != "" and root.code is not None:
            output.append([root.value, root.code, root.label])

        if root.child_nodes is not None:
            for node in root.child_nodes:
                self.get_nodes(node, output)

        return output

    # end get_nodes


# end Trie

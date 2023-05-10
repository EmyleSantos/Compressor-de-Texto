import numpy as np
import sys
from trie.py import Trie, Node


def make_tree(text):
    Tree = Trie()
    root = Node("", 0, 0)
    i = 0
    value = 1

    while i < len(text):
        node = Tree.find_by_label(root, text[i])

        if not node:
            root = Tree.insert(root, text[i], value)
            i += 1
        else:
            j = 0
            while node is not None and i + j < len(text):
                j += 1
                aux = Tree.find_by_label(root, text[i:i + j])
                if aux is None:
                    node = Tree.insert(node, text[i + j - 1], value)
                    i += j
                    break
                node = aux
            else:
                # os últimos j simbolos do texto não foram inseridos na Trie
                if i == len(text) - 1:
                    root = Tree.insert(root, text[-1], value)
                else:
                    node = Tree.find_by_label(root, text[i:-1])
                    node = Tree.insert(node, text[-1], value)
                break

        value += 1

    Tree.num_codes = value - 1
    return Tree, root


def compress(input_file_name, output_file_name):

    f = open(input_file_name, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    Tree, root = make_tree(text)

    output = Tree.get_nodes(root, [])
    output.sort()

    num_bits = int(np.ceil(np.log2(Tree.num_codes - 1)))

    text = '1'
    text += np.binary_repr(num_bits + 2, width=20)

    for i in range(len(output)):
        character_encoded = list(output[i][2].encode('utf-8'))

        size = np.binary_repr(len(character_encoded), width=2)
        bits = size

        # bits referentes ao código
        bits += np.binary_repr(output[i][1], width=num_bits)

        for j in character_encoded:
            bits += np.binary_repr(j, width=8)

        text += bits

    num_bytes = int(np.ceil(len(text) / 8))
    bits_to_bytes = int(text, 2).to_bytes(num_bytes, 'little')

    f = open(output_file_name, 'wb')
    f.write(bits_to_bytes)
    f.close()
# end decompress

def decompress(input_file_name, output_file_name):

    f = open(input_file_name, 'rb')
    text = f.read()  # lê os bytes do arquivo
    f.close()

    bits = np.binary_repr(int.from_bytes(text, 'little'))
    num_bits = int(bits[1:21], 2)

    Tree = Trie()
    root = Node("", 0, 0)

    i = 21
    value = 1

    while i < len(bits):

        size_char = int(bits[i:i + 2], 2)
        caracter_size = 8 * size_char

        code = int(bits[i + 2:i + num_bits], 2)

        caracter = int(bits[i + num_bits:i + num_bits + 8],
                       2).to_bytes(1, 'little')

        jump = 8
        for j in range(size_char - 1):
            b = bits[i + num_bits + jump:i + num_bits + 8 + jump]
            caracter += int(b, 2).to_bytes(1, 'little')
            jump += 8

        caracter = caracter.decode('utf-8')

        node = Tree.find_by_code(root, code)

        if node is not None:
            node = Tree.insert(node, caracter, value)

        i += num_bits + caracter_size
        value += 1

    output = Tree.get_text(root, "", [])
    output.sort()

    text = ""
    for i in range(len(output)):
        text += output[i][2]

    g = open(output_file_name, 'w')
    g.write(text)
    g.close()
# end decompress

if __name__ == "__main__":
    option = sys.argv[1]
    input_file = sys.argv[2]
    
    if option == '-c':
        try:
            op = sys.argv[3]
            output_file = sys.argv[4]
        except:
            output_file = input_file.replace('.txt', '.z78')
        compress(input_file, output_file)
    elif option == '-x':
        try:
            op = sys.argv[3]
            output_file = sys.argv[4]
        except:
            output_file = input_file.replace('.z78', '.txt')
        decompress(input_file, output_file)
    else:
        print("Erro. Argumento inválido:", option)
        exit()
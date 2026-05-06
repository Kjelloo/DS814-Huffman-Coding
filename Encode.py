# Afleveret af
#   Magnus Simoni Jahn (majah25) &
#   Kjell Schoke (kjsch25) &
#   Yasmina Mojib (yamoj25)

import sys

import PQHeap
from bitIO import BitWriter, BitReader
from Node import Node
from Element import Element

def count_frequency(file):
    frequencies = [0] * 256

    # Læs filen byte for byte og opdater frekvensen for hvert byte value
    with open(file, 'rb') as f:
        while True:
            byte = f.read(1)

            # Når byte object af længde nul er nået
            if len(byte) == 0:
                break

            byte_value = byte[0]
            frequencies[byte_value] += 1
    return frequencies

def build_huffman_tree(freq):
    pq = PQHeap.createEmptyPQ()

    # Opret element for de 256 byte værdier og indsæt dem i prioritetskøen
    for byte_value in range(256):
        node = Node(byte_value=byte_value)
        element = Element(key=freq[byte_value], data=node)
        PQHeap.insert(pq, element)

    # Kør Huffmans algoritme indtil roden af træet er nået
    while len(pq) > 1:
        # Tag de to mindste (dem med lavest hyppighed) elementer ud af pq'en
        x = PQHeap.extractMin(pq)
        y = PQHeap.extractMin(pq)

        # Indre knude
        parent_node = Node(byte_value=None, left=x.data, right=y.data)
        # Summere de to hyppigheder og sæt dem i element objektet for at blive gemt i pq'en
        parent_element = Element(key=x.key + y.key,data=parent_node)

        PQHeap.insert(pq, parent_element)

    # Returnere roden af Huffman træet
    return PQHeap.extractMin(pq).data

def fill_table(node, current, table):
    # Base case
    if node.byte_value is not None:
        table[node.byte_value] = current
        return

    # Rekursivt kald for venstre og højre barn, hvor vi tilføjer "0" for venstre og "1" for højre
    if node.left is not None:
        fill_table(node.left, current + "0", table)

    if node.right is not None:
        fill_table(node.right, current + "1", table)


def main():
    # Læs argumenterne når programmet køres. Her kunne man åbne filerne med det samme, dog venter vi at gøre det for RAM'ens skyld
    infile = sys.argv[1]
    outfile = sys.argv[2]

    # 1. Læs inputfilen og tæl hyppigheden af hvert byte
    byte_frequencies = count_frequency(infile)

    # 2. Kør Huffmans algoritme
    root = build_huffman_tree(byte_frequencies)

    # 3. Konverter Huffmans træ til en tabel
    codes = [""] * 256
    fill_table(root, "", codes)

    # 4. Skriv hyppigheden af hvert byte til output filen
    with open(outfile, 'wb') as output_file:
        with BitWriter(output_file) as writer:
            for freq in byte_frequencies:
                writer.writeint32bits(freq)

        # 5. Læs inputfilen igen og skriv den komprimerede data til output filen
            with open(infile, 'rb') as input_file:
                byte = input_file.read(1)

                # Læser inputfilen byte by byte og for hver byte skriver vi den tilsvarende code til output filen, bit by bit
                while len(byte) > 0:
                    code = codes[byte[0]]
                    for bit in code:
                        writer.writebit(int(bit))

                    byte = input_file.read(1)

if __name__ == '__main__':
    main()
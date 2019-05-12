from argparse import ArgumentParser
import os
# import sys

parser = ArgumentParser(description = "Split a text file into parts and label \
                        their content")
parser.add_argument("directory", help = "Directory containing the files to be split")
parser.add_argument("label", help = "Label to be added at the beginning of each part")
parser.add_argument("trunc_size", type = int, help = "Size (characters) of the \
                    resulting parts")

args = parser.parse_args()

os.chdir(args.directory)

part_len = args.trunc_size # Longueur souhaitée de chaque partie
eos = "." # Fin de phrase

for filename in os.listdir():
    # print("Travail sur ", filename)

    out_len = 0 # Nombre d'octets écrits
    part_idx = 0 # Indice de la partie de fichier obtenue

    with open(filename, 'r') as input:
        # print(" Ouvert", input.name)
        out_name_base = input.name # output_0, output_1, ...
        output = open(out_name_base + "_" + str(part_idx), 'w') # Ouvre une nouvelle partie
        output.write(args.label + "\n") # Labellise la partie

        input.readline() # Ligne du titre
        text = input.read()

        for sent in text.split(sep = eos):
            output.write(sent + eos)
            out_len += len(sent + eos)

            if out_len > part_len:
                output.close() # Partie fermée
                # print("     Partie", part_idx, "terminée")

                part_idx += 1
                out_len = 0
                output = open(out_name_base + "_" + str(part_idx), 'w') # Ouvre une nouvelle partie
                output.write(args.label + "\n")

    if output:
        # print(" Fermé : ", output.name)
        output.close() # Ferme la dernière partie

    if out_len < part_len/2: # Si le dernier fichier est "trop court"
        # print("Fusion pour ", input.name, ";", output.name, "sera copié puis supprimé")
        with open(out_name_base + "_" + str(part_idx - 1), 'a') as target:
            # print(" Ouvert : " + out_name_base + "_" + str(part_idx - 1))
            with open(out_name_base + "_" + str(part_idx), 'r') as lastPart:
                lastPart.readline() # Label précédemment ajouté, à ne pas copier
                target.write(lastPart.read()) # Concatène les deux dernières parties

        os.remove(out_name_base + "_" + str(part_idx))
        # print("     Supprimé : " + out_name_base + "_" + str(part_idx))
    # print(output.name, out_len)
    print("Split and labeled : ", input.name)

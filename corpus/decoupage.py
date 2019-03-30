import os

def split_and_label(src_dir, filename, label, part_size, dest_dir):
    eos = "." # Fin de phrase

    out_len = 0 # Nombre d'octets écrits
    part_idx = 0 # Indice de la partie de fichier obtenue

    with open(src_dir + "/" + filename, 'r') as input:
        # print(" Ouvert", input.name)
        output = open(dest_dir + "/" + filename + "_" + str(part_idx), 'w') # Ouvre une nouvelle partie
        output.write(label + "\n") # Labellise la partie

        input.readline() # Ligne du titre
        text = input.read()

        for sent in text.split(sep = eos):
            output.write(sent + eos)
            out_len += len(sent + eos)

            if out_len > part_size:
                output.close() # Partie fermée
                # print("     Partie", part_idx, "terminée")

                part_idx += 1
                out_len = 0
                output = open(dest_dir + "/" + filename + "_" + str(part_idx), 'w') # Ouvre une nouvelle partie
                output.write(label + "\n")

    if output:
        # print(" Fermé : ", output.name)
        output.close() # Ferme la dernière partie

    if out_len < part_size/2: # Si le dernier fichier est "trop court"
        # print("Fusion pour ", input.name, ";", output.name, "sera copié puis supprimé")
        with open(dest_dir + "/" + filename + "_" + str(part_idx - 1), 'a') as target:
            # print(" Ouvert : " + dest_name + "_" + str(part_idx - 1))
            with open(dest_dir + "/" + filename + "_" + str(part_idx), 'r') as lastPart:
                lastPart.readline() # Label précédemment ajouté, à ne pas copier
                target.write(lastPart.read()) # Concatène les deux dernières parties

        os.remove(dest_dir + "/" + filename + "_" + str(part_idx))
        # print("     Supprimé : " + dest_name + "_" + str(part_idx))
    # print(output.name, out_len)
    print("Split and labeled : ", filename)



if __name__ == '__main__':
    # parser = ArgumentParser(description = "Split a text file into parts and label \
    #                         their content")
    # parser.add_argument("directory", help = "Directory containing the files to be split")
    # parser.add_argument("label", help = "Label to be added at the beginning of each part")
    # parser.add_argument("trunc_size", type = int, help = "Size (characters) of the \
    #                     resulting parts")
    #
    # args = parser.parse_args()

    dest_root = "parties_annotees"
    os.mkdir(dest_root)

    src_arb = os.walk("textes_bruts")
    src_root, authors, _ = next(src_arb) # Soit cette ligne, soit la suivante
    # authors = next(src_arb)[1]

    for author in authors:
        os.mkdir(dest_root + "/" + author)

    idx = 0
    for src_path, src_dirs, src_files in src_arb:
        for filename in src_files:
            # dest_label = src_path.split("/")[1] # Nom du dossier
            dest_label = authors[idx]
            dest_dir = dest_root + "/" + authors[idx]
            split_and_label(src_path, filename, dest_label, 2000, dest_dir)
        idx += 1

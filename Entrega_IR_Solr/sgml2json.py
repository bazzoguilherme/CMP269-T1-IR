import glob, sys
import xmltodict, json

def main(files):
    for sgml_filename in files:
        print("> {} : ".format(sgml_filename), end='')
        # Define estrutura basica para json
        json_structure = []
        with open(sgml_filename, 'r', encoding='iso-8859-1') as sgml_file:
            sgml_corrected = sgml_file.read().replace('&', '&amp;').replace(' <', '&lt;').replace('< ', '&lt;').replace('<\n', '&lt;')

            # adiciona root para ler string como xml
            root_tag = "<root>{}</root>".format(sgml_corrected)
            processed_sgml = xmltodict.parse(root_tag)

            # itera entre documentos no arquivo para adicionar na estrutura json
            for document in processed_sgml['root']['DOC']:
                new_document = {}
                for key, value in document.items():
                    new_document[key.lower()] = value
                
                json_structure.append(new_document)

        with open(sgml_filename.replace(".sgml", ".json"), 'w', encoding='utf-8') as json_file:
            json.dump(json_structure, json_file, indent=4)
        
        print("✔")
    print("Todos documentos processados!\n")
          
    

if __name__ == "__main__":
    folder = sys.argv[1]
    files = glob.glob("{}/*.sgml".format(folder))

    main(files)
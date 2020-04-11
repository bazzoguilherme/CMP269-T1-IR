import xmltodict
import sys
import requests

query_url = "{}/solr/{}/select?df={}&fl={}&q={}&rows={}&wt={}"
host = "http://localhost:8983"
df = "_text_IR_"
fl = "docid+score"
rows = 100
wt = "json"

alunos = "GuilhermeBazzo_e_NicolauAlff"

def create_query_input(query_topico):
    final_query = ""
    final_query += query_topico["title"]
    final_query += " "
    final_query += query_topico["desc"]
    final_query += " "
    final_query += query_topico["narr"]

    return final_query.replace(":", " ")


def main(core_name, file_queries):
    queries = {}
    # Realiza leitura do arquivo de topicos para consulta
    with open(file_queries, "r", encoding="utf-8") as query_file:
        queries = xmltodict.parse("<root>{}</root>".format(query_file.read()))
    
    output_file = open("consultas_topicos.txt", "w", encoding="utf-8")
    
    # Realiza a consulta para cada topico 
    for query in queries["root"]["top"]:
        print("Executando consulta em tópico:", query["num"])
        response = requests.get(query_url.format(
            host,
            core_name,
            df,
            fl,
            create_query_input(query),
            rows,
            wt
        ))
        response_json = response.json()

        # Escreve no arquivo de saida os documentos recuperados
        index = 0
        for docs in response_json["response"]["docs"]:
            output_file.write("{}\t{}\t{}\t{}\t{:2.6f}\t{}\n".format(
                query["num"], 
                "Q0", 
                docs["docid"][0], 
                index, 
                docs["score"], 
                alunos
            ))

            index += 1
        
    output_file.close()


if __name__ == "__main__":
    core_name = sys.argv[1]
    file_queries = sys.argv[2]
    main(core_name, file_queries)
import requests, sys

URL_SOLR = "http://localhost:8983"

COLLECTION_NAME = sys.argv[1]

requests.post('{}/solr/{}/schema'.format(URL_SOLR, COLLECTION_NAME), json={
    "add-field": {
        "name": "_text_IR_",
        "type": "text_es",
        "stored": False,
        "indexed": True,
        "multiValued": True}
})

requests.post('{}/solr/{}/schema'.format(URL_SOLR, COLLECTION_NAME), json={
    'add-copy-field': {
        'dest': "_text_",
        'source': "*",
    },
})

requests.post('{}/solr/{}/schema'.format(URL_SOLR, COLLECTION_NAME), json={
    'add-copy-field': {
        'dest': "_text_IR_",
        'source': "*",
    },
})
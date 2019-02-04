from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json, re
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])

## Initialize doc search object and execute search, retrieving all results
query = '3d+printing'
print("Starting query for %s" % query)
doc_srch = ElsSearch(query, 'scopus')
doc_srch.execute(client, get_all = False)
print("doc_srch has", len(doc_srch.results), "results.")

dois = []
for doc in doc_srch.results:
    complete_doi = doc["dc:identifier"]
    num_doi = re.sub("[^0-9]", "", complete_doi)
    dois.append( num_doi )
    print(num_doi)

for scp_idx in dois:
    scp_doc = AbsDoc(scp_id = scp_idx)
    if scp_doc.read(client):
        print ("scp_doc.title: ", scp_doc.title)
        scp_doc.write()   
    else:
        print ("Read document failed.")
    


with open('data.json', 'w') as outfile:
    json.dump(doc_srch.results, outfile)
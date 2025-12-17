from Bio import Entrez

Entrez.email = "your_email@example.com"

def fetch_pubmed_leads(query, max_results=20):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

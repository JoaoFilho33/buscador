import requests 
import requests_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def busca_keyword(key, text):
    array = []

    for i in range(len(text)):
        if text[i:i+len(key)] == key:
            inicio = max(0, i - 15)
            fim = min(len(text), i+len(key) + 15)
            contexto = text[inicio:fim]
            array.append(contexto)

    return array

class localizador_de_links:
    def __init__(self, start_url, max_depth):
        self.visited_urls = [] # guarda as urls visitadas
        self.start_url = start_url
        self.max_depth = max_depth
        self.session = None
        self.references = {}


    def get_links(self, url):
        session = self.get_session()
        res = session.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        links = []
        for link in soup.find_all("a"):
            href = link.get('href')

            if href is not None:
                absolute_url = self.absolute_url(href, res.url)

                if absolute_url not in self.visited_urls:
                    links.append(absolute_url)
                    # trata o numero de referencias para a url
                if absolute_url not in self.references:
                    self.references[absolute_url] = 0

                self.references[absolute_url] += 1
                        
        return links

    def get_session(self): # faz com que armazene em cache as páginas da web que foram acessadas anteriormente 
        if not self.session:
            requests_cache.install_cache('cache')
            self.session = requests_cache.CachedSession() # ao obter a sessão http, todas as solicit. subseq. se está armazenada em cache
        return self.session

    def absolute_url(self, url, base_url):
        return urljoin(base_url, url)

    def search(self, url=None, depth=0):
        if not url:
            url = self.start_url
        if depth > self.max_depth:
            return [] # se atingir o depth max return lista vazia
      
        
        links = self.get_links(url)

        self.visited_urls.append(url) # added url atual as visitadas

        links_ordenados = []
        # sorted() ordena os links em ordem decrescente de acordo com a qtd de referência de cada um
        for link in sorted(links, key=lambda x: self.references[x], reverse=True):
            if link not in self.visited_urls:
                links_ordenados.append(link)
                links_ordenados.extend(self.search(link, depth+1))

        return links_ordenados


# url = "http://127.0.0.1:5500/buscador/html/main.html"
url = input("informe a url inicial: ")
key = input("Palavra-chave da busca: ")
depthStr = input("Profundidade da busca: ")
depth = int(depthStr)

findLinks = localizador_de_links(url, depth)
links = findLinks.search()

# for page in findLinks.visited_urls:
for page in findLinks.visited_urls:
    res = requests.get(page)
    soup = BeautifulSoup(res.text, 'html.parser')
    text = soup.get_text()
    ocorrencias = busca_keyword(key, text)

    print()
    print(f"\nLink: {page}")
    print("Contexto das ocorrencias: ")
    for ocorrencia in ocorrencias:
        print(f"- {ocorrencia}")
 
    print()
    print(f"Qtd de links referenciando essa página: {findLinks.references[page]}")
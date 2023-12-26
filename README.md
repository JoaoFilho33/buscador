# Mecanismo de Busca na Web

#### Este projeto consiste em um pequeno mecanismo de busca na web desenvolvido em Python, utilizando as bibliotecas Requests, Requests Cache, Beautiful Soup e urllib. O script é projetado para ser usado como um localizador de links, permitindo a busca por uma palavra-chave em páginas web, mantendo uma contagem de referências para cada URL e explorando links recursivamente até atingir uma profundidade especificada.


## Funcionalidades Principais

### Busca por Palavra-chave

A função busca_keyword é responsável por procurar uma palavra-chave em um texto, retornando trechos do texto contendo a palavra, juntamente com 15 caracteres antes e depois da palavra.

### Localizador de Links

A classe localizador_de_links é o núcleo do mecanismo de busca. Ela possui os seguintes métodos principais:

- __get_links(url):__ Obtém os links de uma página web, armazenando a quantidade de referências para cada URL.

- __get_session():__ Configura uma sessão HTTP com armazenamento em cache usando a biblioteca requests-cache.

- __absolute_url(url, base_url):__ Retorna uma URL absoluta dada uma URL relativa e uma URL base.

- __search(url=None, depth=0):__ Realiza uma busca recursiva em links, respeitando a profundidade especificada.

### Uso

O script recebe a URL inicial, a palavra-chave de busca e a profundidade desejada como entrada do usuário. Ele então realiza a busca, exibe o contexto das ocorrências da palavra-chave em cada página visitada e apresenta a quantidade de links referenciando cada página.

``` python
url = input("Informe a URL inicial: ")
key = input("Palavra-chave da busca: ")
depthStr = input("Profundidade da busca: ")
depth = int(depthStr)

findLinks = localizador_de_links(url, depth)
links = findLinks.search()

for page in findLinks.visited_urls:
    res = requests.get(page)
    soup = BeautifulSoup(res.text, 'html.parser')
    text = soup.get_text()
    ocorrencias = busca_keyword(key, text)

    print(f"\nLink: {page}")
    print("Contexto das Ocorrências: ")
    for ocorrencia in ocorrencias:
        print(f"- {ocorrencia}")
 
    print(f"Qtd de Links Referenciando essa Página: {findLinks.references[page]}")
```

### Instalação e Dependências

Antes de executar o script, certifique-se de instalar as dependências usando o seguinte comando:

```
pip install requests beautifulsoup4 requests-cache
```
Observação: A biblioteca requests-cache será utilizada para armazenar em cache as páginas web acessadas anteriormente, otimizando as requisições subsequentes.


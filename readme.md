# Bible match

Ferramenta para detecção de referências bíblicas em textos livres

## Objetivos

Essa ferramenta serve para analisar o campo de comentários de podcast bíblicos, e 
tentar encontrar referências de trechos bíblicos.

A ferramenta recebe um arquivo JSON de entrada, contendo os comentários, e retorna
um JSON com as referências encontradas.

A ferramenta pode acessar um arquivo local, ou acessar uma URL contendo o JSON


## Requirementos
* Python 3.9

## Como utilizar

### Configurações

Em primeiro lugar, clone o repositório

Certifique-se que a versão do python correta esteja instalada, com
```shell
python --version
```
ou 
```shell
python3 --version
```

Caso queria usar a funcionalidade de acessar uma URL, é recomendado a utilização de um ambiente virtual:

```shell
# linux
python3 -m venv venv
source ven/bin/activate

# windows
python -m venv venv
.\venv\Scripts\activate
```

Além disso, para instalar as bibliotecas necessárias, utilize o *pip* após ativar o ambiente virtual

```shell
# apos ativar o ambiente virtual
# linux
python3 -m pip3 install -r requirements.txt

# windows
python -m pip install -r requirements.txt
```

Para sair do ambiente virtual após utilizar a ferramenta, digite ```deactivate```

### Arquivo de entrada
O arquivo de entrada pode estar tanto em um arquivo JSON local, quando em uma URL. O arquivo deve estar no seguinte formato:

```json
{
  "id_podcast_1": "Mateus 1:2-4",
  "id_podcast_2": "Genesis 10, Levitico 3:10",
  "id_podcast_3": "João",
  "id_podcast_4": "Salmos 30-31",
  "id_podcast_5": "texto qualquer"
}
```

### Arquivo de saída
O arquivo de saída contem uma lista para cada podcast, com as referências encontradas. A referência
é uma string no formato ```XXX000```, em que ```XXX``` identifica o livro da bíblia, e ```000``` o capítulo da referência.

Caso o livro não possua capítulos, ou não foi encontrada alguma refência ao capítulo lido, o capítulo será ```000```

A seguir estão os identificadores utilizados para cada livro:

```text
GEN = Gênesis
EXO = Êxodo
LEV = Levítico
NUM = Números
DEU = Deuteronômio
JOS = Josué
JUI = Juízes
RUT = Rute
1SA = 1 Samuel
2SA = 2 Samuel
1RE = 1 Reis
2RE = 2 Reis
1CR = 1 Crônicas
2CR = 2 Crônicas
ESD = Esdras
NEE = Neemias
EST = Ester
JOB = Jó
SAL = Salmos
PRO = Provérbios
ECL = Eclesiastes
CAN = Cantares / Cânticos
ISA = Isaías
JER = Jeremias
LAM = Lamentações (de Jeremias)
EZE = Ezequiel
DAN = Daniel
OSE = Oséias
JOE = Joel
AMO = Amós
OBA = Obadias
JON = Jonas
MIQ = Miquéias
NAU = Naum
HAB = Habacuque
SOF = Sofonias
AGE = Ageus
ZAC = Zacarias
MAL = Malaquias
MAT = Mateus
MAR = Marcos
LUC = Lucas
JOA = João
ATO = Atos
ROM = Romanos
1CO = 1 Coríntios
2CO = 2 Coríntios
GAL = Gálatas
EFE = Efésios
FIL = Filipenses
COL = Colossenses
1TE = 1 Tessalonicenses
2TE = 2 Tessalonicenses
1TI = 1 Timóteo
2TI = 2 Timóteo
TIT = Tito
FLM = Filemon
HEB = Hebreus
TIA = Tiago
1PE = 1 Pedro
2PE = 2 Pedro
1JO = 1 João
2JO = 2 João
3JO = 3 João
JUD = Judas
APO = Apocalipse
```

### Execução
Execute o arquivo ```main.py``` . Ele possui algumas opções, que podem ser visualizadas com a opção ```-h```:

```text
> python main.py -h
usage: main.py [-h] [-s] [-u URL] [-l LOCAL] [-o OUTPUT] [-c]

Processa comentarios contendo referencias biblicas

optional arguments:
  -h, --help            show this help message and exit
  -s, --silent          executa sem exibir nenhum comando no terminal
  -u URL, --url URL     url para acessar o json
  -l LOCAL, --local LOCAL
                        especifica um arquivo json local para acessar. Ignorado se URL for especificada
  -o OUTPUT, --output OUTPUT
                        saída contendo os resultados
  -c, --with_comment    salva tambem os comentarios no output
```

## Configurações Avançadas

Para detectar as referências bíblicas, são usadas expressões regulares. Elas foram construídas individualmente.
Caso queira editar cada expressão regular individualmente, edite o arquivo ```re.json```

# document-search

Deze repository bevat de code voor een gebruikersvriendelijke zoekapplicatie voor documenten.

Features:
- efficiente search-backend (elasticsearch)
- overzichtelijke zoekinterface
- documenten toevoegen/beheren
- ondersteuning voor een breed scala aan documenttypes 

## Vereisten
1. Elasticsearch: https://www.elastic.co/downloads/past-releases/elasticsearch-6-7-1
 (Versie 6.*)
2. Zorg dat Java geïnstalleerd is. Indien dat niet zo is, ga naar https://www.oracle.com/technetwork/java/javase/downloads/index.html. Zorg hierna dat de omgevingsvariabele "JAVA_HOME" gedefinieerd is.
3. Elasticsearch ingest-attachment plugin: https://www.elastic.co/guide/en/elasticsearch/plugins/6.7/ingest-attachment.html (hoeft niet eerst gedownload te worden)
4. Python 3.6+: https://www.python.org/download/releases/

## Installatie
Voor stap-voor-stap uitgelegde handleiding: Zie "Elasticsearch installeren.docx". Deze stappen zijn alleen nodig bij de eerste initialisatie op een server of lokale pc. Na het voor het eerst te hebben gedraaid wordt het eenvoudiger (zie "Gebruik").

## Gebruik
Na een eerste initiatisatie te hebben gedaan, hoeft er niet veel meer gedaan te worden elke keer dat de tool moet worden opgestart:
- Start Elasticsearch
    - Open een commandprompt (opdrachtprompt in het Nederlands)
    - Navigeer naar de bin-folder in de elasticsearch-map (C:\Program Files\elasticsearch-6.7.1\bin)
    - Run `elasticsearch.bat`
- Start server
    - Open een nieuwe commandprompt
    - Navigeer naar de map waarin je de bestanden van deze repository hebt "gecloned"
    - Run `python manage.py runserver`

## Reset
- Door het volgende commando uit te voeren worden de documenten tabel en elasticsearch index gereset.
`python manage.py runscript reset`



# scan-fakenews-marker
Code pondu à l'arrache pour prélever des marqueurs d'un site de fakenews (enquetedujour.fr) signalé par les amis de Streepress. 
#link https://www.streetpress.com/sujet/1751622076-streetpress-campagne-ingerence-russe-ukraine-fake-news-media-enquete-journalistes-usurpation-identite-brigitte-macron-transidentite-complotisme

Ce site usurpe les journalistes de streetpress pour signer des articles.
Voici les marqueurs:

| Marqueur                        | Exemple / Détail                      | Potentiel de détection |
| ------------------------------- | ------------------------------------- | ---------------------- |
| Thème Fox WordPress             | fox-xxx.css, classes `*56`            | Fort                   |
| Rank Math SEO                   | Balises meta/OG générées Rank Math    | Moyen                  |
|scripts de tracking              | UA ou GA4, Hotjar, Yandex, etc
| Structure images                | `/uploads/YYYY/MM/` fichiers courts   | Moyen/Fort             |
| Auteur page/photo spécifique    | `/author/nom/` et `/uploads/YYYY/MM/` | Moyen                  |
| Fonts & classes CSS spécifiques | “Roboto”, “Zilla Slab”, `authorbox56` | Moyen                  |
| Temps de lecture meta Twitter   | “1 minute” etc.                       | Moyen                  |
| Nom de l'image                  | “Fbe-1.jpeg” est typique des fichiers téléchargés ou renommés automatiquement, souvent issu de banques d’images | Moyen |
| Alt des images | Si null ou uploads_wordpress, pas commun pour un site d'information | FORT |


Objectif du code, scanner d'autres sites suspect afin de detecter une potentiel ferme à désinformation.

## Install
`pip install -r requirements.txt` or `pip install beautifulsoup4 requests`

## Execution:
`python3 fakenews-marker.py https://fuckingwebsite.fr/article/`

## TODO
- format de sortie différent (JSON, CSV) 
- scan de plusieurs fichiers html d’un dossier
- whois du domaine pour marqueur creation_date (si inferieur à 6 mois de la présente date, Potentiel FORT)
- Si vous avez d'autres marqueurs, welcome.

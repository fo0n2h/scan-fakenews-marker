# scan-fakenews-marker
Code pondu à l'arrache pour prélever des marqueurs d'un site de fakenews (enquetedujour.fr) signalé par les amis de Streepress.
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
| Nom de l'image                  | “Fbe-1.jpeg” est typique des fichiers téléchargés ou renommés automatiquement, souvent issu de banques d’images


Objectif du code, scanner d'autres sites suspect afin de detecter une potentiel ferme à désinformation.

#INSTALL
pip install -r requirements.txt
python3 fakenews-marker.py https://fuckingwebsite.fr/xxxxxxx.html

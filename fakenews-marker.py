import sys
import os
import re
from bs4 import BeautifulSoup

def load_html(input_path):
    # Détermine si input_path est une URL ou un fichier local
    if input_path.startswith('http://') or input_path.startswith('https://'):
        try:
            import requests
            resp = requests.get(input_path, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
            html_content = resp.text
            print(f"[INFO] HTML récupéré depuis l'URL : {input_path}")
        except Exception as e:
            print(f"[ERREUR] Impossible de télécharger la page : {e}")
            sys.exit(1)
    else:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            print(f"[INFO] HTML chargé depuis le fichier : {input_path}")
        except Exception as e:
            print(f"[ERREUR] Impossible de lire le fichier : {e}")
            sys.exit(1)
    return html_content

def scan_fake_news_markers(html_content):
    results = {
        'theme_fox': False,
        'fox_css_files': [],
        'css_56_classes': [],
        'rank_math_seo': False,
        'images': [],
        'image_markers': [],
        'author_info': {},
        'twitter_reading_time': None,
        'fonts_detected': set(),
        'trackers': [],
    }
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Cherche les fichiers CSS fox-*
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if 'fox-' in href:
            results['theme_fox'] = True
            results['fox_css_files'].append(href)

    # 2. Cherche les classes CSS qui finissent par "56"
    all_classes = set()
    for tag in soup.find_all(True):
        class_list = tag.get('class', [])
        for c in class_list:
            if c.endswith('56'):
                all_classes.add(c)
    results['css_56_classes'] = list(all_classes)

    # 3. Rank Math SEO
    if soup.find(string=re.compile('Rank Math')):
        results['rank_math_seo'] = True

    # 4. Images utilisées (et structure des noms)
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            marker = {}
            marker['src'] = src
            marker['filename'] = os.path.basename(src)
            marker['folder'] = os.path.dirname(src)
            marker['alt'] = img.get('alt', '')
            marker['marker'] = None
            # Détecte structure wp-content/uploads/YYYY/MM/
            if re.search(r'/wp-content/uploads/\d{4}/\d{2}/', src):
                marker['marker'] = 'uploads_wordpress'
            # Détecte nommage court (moins de 12 caractères)
            if len(marker['filename'].split('.')[0]) <= 12:
                marker['marker'] = (marker['marker'] or '') + '|short_filename'
            results['images'].append(marker)
            results['image_markers'].append(marker['marker'])

    # 5. Auteur WordPress
    author_meta = soup.find('meta', attrs={'name': 'twitter:data1'})
    author_info = {}
    if author_meta:
        author_info['twitter_author'] = author_meta.get('content')
    # Cherche la page author WordPress
    author_links = []
    for a in soup.find_all('a', href=True):
        if '/author/' in a['href']:
            author_links.append(a['href'])
    author_info['author_links'] = author_links
    results['author_info'] = author_info

    # 6. Temps de lecture dans Twitter Card
    reading_time = None
    for meta in soup.find_all('meta', attrs={'name': 'twitter:label2'}):
        if meta.get('content', '').lower().startswith('temps de lecture'):
            reading_time_meta = soup.find('meta', attrs={'name': 'twitter:data2'})
            if reading_time_meta:
                reading_time = reading_time_meta.get('content')
    results['twitter_reading_time'] = reading_time

    # 7. Fonts détectées
    fonts = set()
    style_tags = soup.find_all('style')
    for style in style_tags:
        fonts.update(re.findall(r'font-family\s*:\s*["\']?([a-zA-Z0-9 ,\-]+)', style.text))
    for link in soup.find_all('link', href=True):
        if 'fonts.googleapis.com' in link['href']:
            fonts.add('Google Fonts')
    results['fonts_detected'] = list(fonts)

    # 8. Recherche de scripts de tracking
    trackers = []
    tracking_patterns = {
        'Google Analytics (UA)': r'UA-\d{4,10}-\d+',
        'Google Analytics 4 (GA4)': r'G-[A-Z0-9]{8,}',
        'Google Tag Manager': r'GTM-[A-Z0-9]+',
        'Matomo/Piwik': r'(matomo|piwik)',
        'Facebook Pixel': r'fbq\(.+?track|facebook\.com/tr',
        'Hotjar': r'hotjar',
        'Yandex Metrika': r'metrika|mc\.yandex',
    }

    # Recherche dans le texte brut (certains codes inline ne passent pas par des balises script)
    for tracker_name, pattern in tracking_patterns.items():
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            trackers.append({'tracker': tracker_name, 'found': list(set(matches))})

    # Recherche dans les balises <script src=...>
    for script in soup.find_all('script', src=True):
        src = script['src']
        for tracker_name, pattern in tracking_patterns.items():
            if re.search(pattern, src, re.IGNORECASE):
                trackers.append({'tracker': tracker_name, 'found': [src]})

    results['trackers'] = trackers

    print("==== Marqueurs détectés ====")
    print(f"[FOX theme] : {results['theme_fox']}")
    if results['fox_css_files']:
        print(f"  -> Fichiers CSS Fox : {results['fox_css_files']}")
    if results['css_56_classes']:
        print(f"  -> Classes CSS '56' : {results['css_56_classes']}")
    print(f"[Rank Math SEO] : {results['rank_math_seo']}")
    print(f"[Images] :")
    for img in results['images']:
        print(f"  - {img['src']} (Alt: {img['alt']}, Marqueur: {img['marker']})")
    print(f"[Auteur] : {results['author_info']}")
    print(f"[Temps de lecture Twitter Card] : {results['twitter_reading_time']}")
    print(f"[Fonts détectées] : {results['fonts_detected']}")
    print(f"[Trackers détectés] :")
    if not trackers:
        print("  Aucun tracker trouvé.")
    for tracker in trackers:
        print(f"  - {tracker['tracker']} : {tracker['found']}")
    print("===========================")

    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scan_fakenews_marker.py [fichier_html|url]")
        sys.exit(1)
    input_path = sys.argv[1]
    html_content = load_html(input_path)
    scan_fake_news_markers(html_content)


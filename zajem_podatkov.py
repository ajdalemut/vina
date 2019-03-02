import re
import orodja as orod


vzorec_url_vina = re.compile(
    r'https://winelibrary.com/wines/'
    r'(?P<novi_url>.+?)">.*?'
    ,
    flags = re.DOTALL
)

vzorec_vina = re.compile(
    r'<title>(?P<ime>.+?) \| Wine Library</title>.*?'
    r'price:amount" content="(?P<cena>\d+?\.\d\d)"/>.*?'
    r'>Item #</td>.+?>(?P<id>\d{0,6})</td>.*?'
    r'>Country</td>.+?country%5B%5D=(?P<drzava>.+?)">.*?'
    r'>Color</td>.+?">(?P<barva>Red|White|Rose)</a></td>.*?'
    r'>Taste</td>.+?"data">(?P<okusi>.*)</td>.*?'
    r'>Nose</td>.+?"data">(?P<vonji>.*)</td>.*?'
    ,
    flags=re.DOTALL
)

vzorec_regije = re.compile(
    r'>Region</td>.+?&amp;region%5B%5D=(?P<regija>.+?)">.*?'
    ,
    flags=re.DOTALL
)

vzorec_letnika = re.compile(
    r'>Vintage</td>.+?">(?P<letnik>\d{4})</a></td>.*?'
    ,
    flags=re.DOTALL
)

vzorec_alkohola = re.compile(
    r'>ABV</td>.+?"data">(?P<alkohol>\d\d\.\d)%</td>.*?'
    ,
    flags=re.DOTALL
)

vzorec_zaprtja = re.compile(
    r'>Closure</td>.+?"data">(?P<zaprtje>Cork|Screwtop)</td>.*?'
    ,
    flags=re.DOTALL
)

vzorec_ocene = re.compile(
    r'itemprop=\'ratingValue\'>(?P<ocena>\d{1,3})</span>.*?'
    ,
    flags=re.DOTALL
)

def izloci_podatke_vina(niz):
    '''Iz danega niza izloči podatke vina in jih uredi.'''
    vino = vzorec_vina.search(niz).groupdict()
    vino['okusi'] =  vino['okusi'].replace('\n','')
    vino['vonji'] =  vino['vonji'].replace('\n','')
    vino['cena'] = float(vino['cena'])
    vino['drzava'] = vino['drzava'].replace('+', ' ')
    # niz vonjev in okusov spremenimo v sezname
    vino['vonji'] = vino['vonji'].split(', ')
    vino['okusi'] = vino['okusi'].split(', ')
    # zabeležimo regijo, če je omenjena in ni kar država sama
    regija = vzorec_regije.search(niz)
    if regija and regija['regija'] != vino['drzava']:
        vino['regija'] = regija['regija'].replace('+', ' ')
    else:
        vino['regija'] = None
    #zabeležimo letnik, če je omenjen
    letnik = vzorec_letnika.search(niz)
    if letnik :
        vino['letnik'] = int(letnik['letnik'])
    else:
        vino['letnik'] = None
    #zabeležimo oceno, če je omenjena
    ocena = vzorec_ocene.search(niz)
    if ocena:
        vino['ocena'] = float(ocena['ocena'])
    else:
        vino['ocena'] = None
    #zabeležimo alkohol, če je omenjen
    alkohol = vzorec_alkohola.search(niz)
    if alkohol:
        vino['alkohol'] = float(alkohol['alkohol'])
    else:
        vino['alkohol'] = None
    #zabeležimo zaprtje, če so omenjeno
    zaprtje = vzorec_zaprtja.search(niz)
    if zaprtje:
        vino['zaprtje'] = zaprtje['zaprtje']
    else:
        vino['zaprtje'] = None
    return vino

def vina_na_strani(st_strani):
    '''Najprej nalozi stran s seznamom izdelkov, nato za vsak izdelek poišče url do podrobnih podatkov in naloži še tiste urlje. '''
    url = (
        'https://winelibrary.com/search?'
        'color%5B%5D=Red&'
        'color%5B%5D=White&'
        'color%5B%5D=Rose&'
        'page={}&'
        'size%5B%5D=750ML'
    ).format(st_strani)
    ime_datoteke1 = 'zajeti-podatki/vina-{}.html'.format(st_strani)
    orod.shrani_spletno_stran(url, ime_datoteke1)
    vsebina = orod.vsebina_datoteke(ime_datoteke1)
    i = 1
    for url_vina in vzorec_url_vina.finditer(vsebina):
        ime_datoteke2 = 'zajeti-podrobni-podatki/vina-podorobno-{}.html'.format(st_strani*100 + i)
        podatek = url_vina.groupdict()
        url1 = 'https://winelibrary.com/wines/' + podatek['novi_url'].strip()
        orod.shrani_spletno_stran(url1, ime_datoteke2)
        nova_vsebina = orod.vsebina_datoteke(ime_datoteke2)
        i += 1
        yield izloci_podatke_vina(nova_vsebina)

def izloci_gnezdene_podatke(vina):
    vonji, okusi = [], []
    for vino in vina:
        for vonj in vino['vonji']:
            vonji.append({'vino': vino['id'], 'vonj': vonj})
        for okus in vino['okusi']:
            okusi.append({'vino': vino['id'], 'okus': okus})
        del vino['vonji']
        del vino['okusi']
    return vonji, okusi

vina = []
for stran in range(1, 78):
    for vino in vina_na_strani(stran):
        vina.append(vino)
vina.sort(key = lambda vino: vino['id'])
orod.zapisi_json(vina, 'obdelani-podatki/vina.json')
vonji, okusi = izloci_gnezdene_podatke(vina)
orod.zapisi_csv(vina, ['id', 'ime', 'barva', 'letnik', 'drzava', 'regija','cena', 'alkohol', 'zaprtje', 'ocena' ], 'obdelani-podatki/vina.csv')
orod.zapisi_csv(vonji, ['vino', 'vonj'], 'obdelani-podatki/vonji.csv')
orod.zapisi_csv(okusi, ['vino', 'okus'], 'obdelani-podatki/okusi.csv')
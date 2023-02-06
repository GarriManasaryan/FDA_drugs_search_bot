from metapub import PubMedFetcher
import urllib.request
from urllib.error import HTTPError

fetch = PubMedFetcher()

def doi_referencer(doi):
    BASE_URL = 'http://dx.doi.org/'
    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/x-bibtex')

    try:
        with urllib.request.urlopen(req) as f:
            bibtex = f.read().decode()

        doi_dict = {}
        for i in bibtex.split('\n\t'):
            if 'author' in i:
                first_author = i.replace('author = {', '').replace('},', '').split(' and ')[0].split(' ')
                second_name = first_author[-1].capitalize()
                first_name = first_author[0]
                doi_dict['author'] = second_name + ' ' + first_name[0] + ', et al.'

            if 'title' in i:
                title = i.replace('title = {', '').replace('},', '')
                if title[-1] == '.':
                    doi_dict['title'] = title
                else:
                    doi_dict['title'] = title + '.'

            if 'year' in i:
                doi_dict['year'] = i.replace('year = ', '').replace(',', '') + ';'

            if 'volume' in i:
                doi_dict['volume'] = i.replace('volume = {', '').replace('},', '')

            if 'pages' in i:
                pages = i.replace('pages = {', '').replace('},', '').replace('--', '-')
                try:
                    if pages.split('-')[0] == pages.split('-')[1]:
                        doi_dict['pages'] = pages.split('-')[0]
                    else:
                        doi_dict['pages'] = pages
                except:
                    doi_dict['pages'] = pages

        if doi_dict.get('volume') and doi_dict.get('pages'):
            doi_dict['volume_with_pages'] = doi_dict.get('volume') + ':' + doi_dict.get('pages') + "."

        if not doi_dict.get('volume') and doi_dict.get('pages'):
            doi_dict['volume_with_pages'] = doi_dict.get('pages') + "."

        if doi_dict.get('volume') and not doi_dict.get('pages'):
            doi_dict['volume_with_pages'] = doi_dict.get('volume') + "."

        if not doi_dict.get('volume') and not doi_dict.get('pages'):
            doi_dict['volume_with_pages'] = 'NOT_FOUND'

        if doi_dict.get('volume_with_pages') == 'NOT_FOUND':
            doi_dict['year'] = doi_dict.get('year').replace(';', '')

        doi_dict['doi'] = doi
        citation = 'DOI: ' + doi_dict.get('doi') + ' ' + ' '.join(list(filter(lambda x: x!= 'NOT_FOUND' , [doi_dict.get('author', 'NOT_FOUND'), doi_dict.get('title', 'NOT_FOUND'), doi_dict.get('year', 'NOT_FOUND'), doi_dict.get('volume_with_pages', 'NOT_FOUND') ])))

        return citation.replace('{', '').replace('}', '').replace('$\\up', '').replace('$', '')

    except:
        return f'DOI: {doi}'

def single_citation_main(pmid_id):
    article = pmid_id
    pmid = fetch.article_by_pmid(pmid_id)

    if (len(pmid_id)==8) or (len(pmid_id)==7):
        year = pmid.year + ';'

        if pmid.volume and pmid.pages:
            volume_with_pages = pmid.volume + ':' + pmid.pages + "."

        if not pmid.volume and pmid.pages:
            volume_with_pages = pmid.pages + "."

        if pmid.volume and not pmid.pages:
            volume_with_pages = pmid.volume + "."

        if not pmid.volume and not pmid.pages:
            volume_with_pages = 'NOT_FOUND'

        # volume_with_pages = 'NOT_FOUND'
        if volume_with_pages == 'NOT_FOUND':
            year = year.replace(';', '')

        citation = f'PMID: {pmid_id} ' + ' '.join(['., '.join(pmid.authors[:3]) + '. et al.', pmid.title, year, volume_with_pages if volume_with_pages != 'NOT_FOUND' else ''])

    elif '10.' in article:
        if 'https://' in article:
            doi_article = article.replace('https://doi.org/', '').replace('http://dx.doi.org/', '')

        elif 'doi: 10.' in article.lower():
            try:
                doi_article = list(filter(lambda x: '10.' in x ,  article.split(' ')))[0]
            except:
                doi_article = None

        elif 'doi:10.' in article.lower():
            doi_article = article[4:]

        else:
            doi_article = article

        try:
            citation = doi_referencer(doi_article)
        except:
            citation = 'Reference not found (either invalid pmid-doi or some sort of error, idk...)'

    else:
        citation = 'Reference not found (either invalid pmid-doi or some sort of error)'

    return citation.replace('<sup>', '').replace('</sup>', '')

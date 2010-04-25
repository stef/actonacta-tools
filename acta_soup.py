#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup, HTMLParseError
from StringIO import StringIO as io
from wikitools import wiki
from wikitools import category
from password import USER, PASSWORD

LANGS=['bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv', 'en']

def getPage(url,lang):
    page = urllib2.urlopen(url % (lang.upper(),lang.upper()))
    try:
        soup = BeautifulSoup(page)
    except HTMLParseError, e:
        print "Unable to fetch", lang, "version of", url

    titleBoxes = soup.findAll('tr', attrs={'class':'doc_title'})
    titleBlock = titleBoxes.pop() # The last box is the one we want
    headline = titleBlock.find('td', attrs={"align":"left", "valign":"top"})
    headLineText = headline.next.next.next.next
    headlineText = headLineText.strip()

    pageContents = u''
    pageContents += unicode(headlineText) + u"\n"
    for piece in soup.find('tr', attrs={'class':'contents'}).next:
        pageContents += unicode(piece).strip()

    return (headlineText, pageContents)

for lang in LANGS:
    # get the content to be loaded
    title,content=getPage("http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//TEXT+TA+P7-TA-2010-0058+0+DOC+XML+V0//%s&language=%s",lang)
    # add intertiki multilanguage header
    interwikiHeader=['[['+lng+':]]' for lng in LANGS if not lng==lang]
    content=' '.join(interwikiHeader)+'\n\n'+content

    print title.encode('utf8')
    print content.encode('utf8')

    # connect to the site to be imported into
    #site = wiki.Wiki("http://"+lang+".act-on-acta.eu/api.php")
    #site.login(USER, password=PASSWORD)

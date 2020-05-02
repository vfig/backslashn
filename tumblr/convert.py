#!/usr/bin/python

BASE_PATH = './backslashn-backup-2019-06-14/'
OUTPUT_PATH = './converted/'

from datetime import datetime
import os, errno
import xml.etree.ElementTree as ET
tree = ET.parse(BASE_PATH + 'posts/posts.xml')
root = tree.getroot()
xml_posts = root.find('posts').findall('post')

SKIP = {
    '180367539', '183069105', '185428516', '187888221', '200330883', '247696414', '293664248', '484112400',
    '489798861', '505601626', '508904851', '510239009', '518923883', '521460838', '523137224', '524265146',
    '527879525', '617075564', '648169564', '649792410', '681013260', '681286454', '697310122', '701886376',
    '703959015', '707729377', '709581385', '745487860', '803587530', '848980652', '871503073', '941830852',
    '949332383', '1042495329', '1064306392', '1128202550', '1155679268', '1221413877', '1326894093',
    '1509153046', '2512213483', '2626437215', '2626663159', '2682092645', '2742405224', '2751241261',
    '3763057383', '3919149217', '4463223253', '4603104477', '5187332167', '5459473864', '5605088765',
    '5961579024', '5965035843', '6332659044', '6587649419', '6766984575', '7669124799', '8061857324',
    '9558444267', '10098080519', '11157343128', '11271092651', '11350412193', '13173497372', '13723873499',
    '15354979341', '30026142212', '31874563662', '37712343299', '47359005484', '64109802298', '65040198207',
    '65040251052', '69370203498', '220781721'
}

# import code; code.interact("blergh", raw_input, locals())

class Post(object):
    def __init__(self, p):
        self.id = p.attrib.get('id', u'missing-id')
        self.slug = p.attrib.get('slug', u'missing-slug')
        self.date = unicode(p.attrib.get('date-gmt', u'0'))
        self.draft = (str(p.attrib.get('state', 'published')) == 'draft')
        # Regular post
        title_el = p.find('regular-title')
        body_el = p.find('regular-body')
        # Link
        link_text_el = p.find('link-text')
        link_url_el = p.find('link-url')
        link_description_el = p.find('link-description')
        # Quote
        quote_text_el = p.find('quote-text')
        quote_source_el = p.find('quote-source')

        # Okay, extract the data
        if body_el is not None:
            self.body = body_el.text
            if title_el is not None:
                self.title = unicode(title_el.text)
            else:
                self.title = u"(untitled post -- needs edit)"
        elif link_text_el is not None and link_url_el is not None:
            self.title = unicode(link_text_el.text)
            link_html = (u"<a href=\"%s\">%s</a>\n\n" % (unicode(link_url_el.text), unicode(link_text_el.text)))
            self.body = link_html + unicode(link_description_el.text)
        elif quote_text_el is not None and quote_source_el is not None:
            self.title = u"(quote -- needs edit)"
            quote_html = u"<blockquote>%s</blockquote>" % unicode(quote_text_el.text)
            self.body = quote_html + "\n\n" + unicode(quote_source_el.text)
        else:
            self.title = u"(unknown type)"
            self.body = u""

    def prolog(self):
        parts = []
        parts.append(u"---")
        if self.title:
            parts.append(u"title: \"%s\"" % (self.title.replace('"', '\\"')))
        parts.append(u"date: %s" % (datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S %Z").strftime("%Y-%m-%dT%H:%M:%SZ")))
        parts.append(u"toc: false")
        parts.append(u"draft: %s" % ("true" if self.draft else "false"))
        parts.append(u"---")
        return u"\n".join(parts)

    def __unicode__(self):
        return self.prolog() + u"\n\n" + self.body + u"\n"

posts = []
for p in xml_posts:
    posts.append(Post(p))

for p in posts:
    if p.id in SKIP: continue

    POST_PATH = OUTPUT_PATH + p.id + '/'
    MEDIA_PATH = POST_PATH + p.slug + '/'
    try:
        os.makedirs(MEDIA_PATH)
    except os.error as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    md = POST_PATH + p.slug + '.md'
    print md
    with file(md, 'w') as f:
        text = unicode(p)
        f.write(text.encode('utf8'))

# Missing: media link handling (images and video... don't think I have any audio?)
# Missing: trying to run this through hugo to check the results

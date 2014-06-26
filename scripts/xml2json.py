from xml.parsers.expat import ParserCreate

class Xml2Json:
    LIST_TAGS = ['COMMANDS']
    
    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()
        
    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert self._data.strip() == ''
        self._stack.append([(tag, attrs)])
        self._data = ''

    def end(self, tag):
        last_pair = self._stack.pop()
        last_tag = last_pair[0][0]
        last_attrs = last_pair[0][1]
        assert last_tag == tag
        if len(last_pair) == 1: #leaf
            data = (self._data, last_attrs)
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_pair[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_pair[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:(data, last_attrs)}
        self._data = ''

    def data(self, data):
        self._data = data


# >>> Xml2Json('<doc><tag><subtag>data</subtag><t>data1</t><t>data2</t></tag></doc>').result
# {u'doc': {u'tag': {u'subtag': u'data', u't': [u'data1', u'data2']}}}

# Syntax:
#   <tag attr1="v1" attr2="v2"><subtag>Text</subtag></tag>
#   converts to
#   {u'tag': ({u'subtag': (u'Text', {})}, {u'attr2': u'v2', u'attr1': u'v1'})}

# >>> text = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><principal xmlns="http://www.dasish.eu/ns/addit" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" URI="http://lux17.mpi.nl/ds/webannotator-basic/api/principals/914f9429-2299-4dba-8c18-11d2891c7b85" xsi:schemaLocation="http://lux17.mpi.nl/schemacat/schemas/s15/files/dwan.xsd"><displayName>Unit Test</displayName><eMail>indrek.jentson@ut.ee</eMail></principal>'
# >>> Xml2Json(text).result
# {u'principal': ({u'displayName': (u'Unit Test', {}), u'eMail': (u'indrek.jentson@ut.ee', {})}, {u'xmlns:xsi': u'http://www.w3.org/2001/XMLSchema-instance', u'xmlns': u'http://www.dasish.eu/ns/addit', u'xsi:schemaLocation': u'http://lux17.mpi.nl/schemacat/schemas/s15/files/dwan.xsd', u'URI': u'http://lux17.mpi.nl/ds/webannotator-basic/api/principals/914f9429-2299-4dba-8c18-11d2891c7b85'})}

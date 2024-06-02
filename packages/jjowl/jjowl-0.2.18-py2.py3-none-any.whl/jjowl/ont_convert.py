""" VERY EXPERIMENTAL :  module for opinied command line processing of OWL ontologies

# Synopsis

    jjtmd2ttl [option] file.t.md ...
      ## convert markdown with yaml metadate into turtle (seealso pandoc)

    jjtable2ttl [option] file.csv ...
      -F '#'            - Fiels separator (def: '::')
      -f ','            - sub field separatos (def: '[;,]')
      -h 'headerLine'   - set a "header line" (def: first line)
         Ex:  jjtable2ttl -F : -h 'Id::uid::gid::name::' /etc/passwd
      ## convert csv  metadate in turtle 

    jjyaml2ttl [option] file.yaml ...
       ... FIXME options descriptions missing
      ## converts multi-yaml dictionaries into turtle

    jjtax2ttl [option] file.tax ...
      -r 'isSonOf'      - subclass relation (def: 'rdfs:subClassOf')
      ## convert indented Class hierarchy in turtle

# Description
"""

from jjcli import *
#from unidecode import unidecode
import json
import yaml
from copy import deepcopy, copy
#import owlrl
#from   owlrl import convert_graph, RDFXML, TURTLE, JSON, AUTO, RDFA
#import rdflib
#from   rdflib.namespace import RDF, OWL, RDFS, SKOS, FOAF

##=======

## -----------------------------------------------------------------
## === utils importing "pseudo ontology elems"
##   parse tmd   ( meta(yaml) + body(markdown) )
##   tmd → turtle
##   t2iri(s)          """ term 2 IRIref """
##   t2iri_or_lit(s)
##   t2lit(s rel=p,)
##   docs2ttl(d, opt)       """ python structure to ttl

'''
FIXME:
 rdf:
    type          => s:iri o:iri.Class
    a             => s:iri o:iri.Class
    comment
 owl:
    inverseOf :            s:iri.rel → s:iri.rel
    Class
    Thing     :   iri.Class
    sameAs
    ObjectProperty :    if x 'a' ObjectProperty   /\ _x_ => s:iri o:iri
    DatatypeProperty  : if x 'a' DatatypeProperty /\ _x_ => s:iri o:literal
 rdfs:
    label :       s:iri       o:literal
    range :       s:iri.prop  o:iri.Class
    domain:       s:iri.prop  o:iri.Class
    subClassOf :  s:iri.Class o:iri.Class        
'''

###-----------------------------------------
### parse markdown with initial YAML-metadata  ( jjmd2ttl )
###-----------------------------------------

REL={'url': 'url'}  ## FIXME convensions

def md2py(c):
    """ files(markdown with initial yaml metadata) → docs = [ doc ] 
    inputfile=
       ---
       yaml-dict
       ---
       bodytext

    outputDoc=
       if bodytext not empty:
          doc["__body-format__"] = "markdown"
          doc[yaml[body] or "body"] = bodytext
       if -v:
          doc["__file__"] = inputfilename
"""
    docs =[]
    for txt in c.slurp():
        doc = {}
        ex = match(r'\s*---(.*?)---(.*)',txt,flags=re.S)
        if not ex:
            warn("### Erro: no formato de", c.filename())
            continue
        meta,text =(sub(r'\t','    ',ex[1]) , ex[2])
        try:
            doc = yaml.safe_load(meta)
        except Exception as e:
            warn("### Erro: nos metadados de", c.filename(),e)
            continue
        if not isinstance(doc,dict):
            warn("### Erro: nos metadados de", c.filename(),doc)
            continue
        if '-v' in c.opt:
            doc["__file__"] = c.filename()
        if search(r'\S',text):
            if "format" in doc:   
                bformat = doc.pop("format")
            else:
                bformat = "markdown"
            doc["__body-format__"] = bformat

            if "body" in doc:   
                bname = doc.pop("body")
            else:
                bname = "body"
            doc[f"{bname}^^{bformat}"] = text

        docs.append(doc)
    return docs

def main_tmd2ttl():            ## main -- tmd2ttl
    '''
NAME
    jjtmd2ttl - converts markdown with inicia YAML metadata into turtle
     -p properties-table (FIXME: ignored for the moment)

SYNOPSIS

Description
   inputfile=
    ---
    yaml-dict
    ---
    bodytext
'''
    c = clfilter(opt="do:",doc=main_tmd2ttl.__doc__)
    ds = md2py(c)
    print(docs2ttl(ds,c.opt))

#def quotes(s):
#    if not search(r'["\n]', str(s)):
#        return f'"{s.strip()}"
#    if search(r'[!?()"\'\n+,;/]',str(s)):
#        s1 = sub(r"\n",r" \n",s1)
#        return f'"""{s1} """'

###-----------------------------------------
### general IRI and lit
###-----------------------------------------

def t2lit(s,rel=None, ty=None):
    """ term 2 literal """
    if ty is not None: 
        typestr = f'^^:{ty}'
    elif rel in REL:
        typestr = f'^^:{REL[rel]}'
    else:
        typestr = ""

    if isinstance(s ,(dict,list,tuple)):
        return f'"""FIXME: {s}"""'
    if isinstance(s ,int):
        return str(s)
    if search(r'[!?()\'+,;/]',str(s)) and not search(r'["\r\n]', str(s)):
        return f'"{s.strip()}"{typestr}'
    if search(r'[!?()\'+,;/"\n\r]',str(s)):
        s1 = str(s).strip()
        if r := search(r'^!!(\w+)',s1):     ### !!id .... → """..."""^^:id
            s1 = sub(r'^!!\w+',r'',s1)
            return f'"""{s1} """^^:{str(r[1])}'
        else:
            s1 = sub(r"\n",r" \n",s1)
            return f'"""{s1} """{typestr}'

    return f'"{s.strip()}"{typestr}'

def t2iri(s, maybe=False):
    """ term 2 IRIref → IRI or "FIXME-..."None """
    if isinstance(s ,(dict,list,tuple)):
        warn("??? t2iri:",s)
        return f'"""FIXME: {s}"""'
    if maybe and match( r'\d', str(s)):
        return f'"""{str(s)}"""'
    if maybe and match( r'\d+$', str(s)):
        return f'"{str(s)}"'
    if s in {'type','a',} : return f'a'
    if s in {'inverseOf','Class','Thing','sameAs', 'ObjectProperty',
            'DatatypeProperty','Nothing'} :
        return f'owl:{s}'
    if s in {'range','domain','subClassOf'} :
        return f'rdfs:{s}'
    if search(r'^(owl|rdfs?|foaf|skos):\w+$',str(s)):
        return s

    if search(r'[!?()"\'\n+,;/ºª]',str(s)):
        aux = sub(r'[!?()"\'\n+,ºª;/ \r\t\n:_]+',r'_',s.strip()) 
        aux = aux.strip("_.,")
        if maybe: 
            return None
        else:
            return f":{aux}"

    iri = sub(r'[ \r\t\n:_]+',r'_',str(s).strip())
    iri = sub(r'\.$','',iri)
    return ":"+iri

def t2iri_or_lit(s,rel=None, ty=None):
    aux = t2iri(s,maybe=True)
    if aux is not None: 
        return aux
    else: 
        return t2lit(s,rel=rel,ty=ty)

###----------------------------------
### generate ttl
###----------------------------------

def getid(d, opt={}): ### { @id : vi, ...dict-tail } → {vi : ...dict-tail }
    if  not isinstance(d, dict):  return None
    subj = opt.get("-s")
    if   "id" in d:          return d.get("id")
    elif "ID" in d:          return d.get("ID")
    elif "@id" in d:         return d.get("@id")
    elif "name" in d:        return d.get("name")
    elif "@name" in d:       return d.get("@name")
    elif "title" in d:       return d.get("title")
    elif subj and subj in d: return d.get(subj)
    else:                    return None

def docs2ttl(d, opt={}):
    """ docs → turtle triples 
      (s,p,o)  or
      [s,p,o] → :s :p :o.      
           or more exactly dict2ttl({ s : {p : o}})

      [s, dict({pi:oi})] → :s :p1 :o1 ... :s :pi :oi .
           or more exactly dict2ttl({ s : dict(...)})

      list → join( "\n", [docst2ttl(v) v ∈ list] )

      dict → dict2ttl(dict)
    """

    if isinstance(d,list):
        if len(d)==3 and not isinstance(d[0],(list,dict,tuple)) :
            return dict2ttl({d[0]: {d[1]: d[2]}}, opt)
        elif ( len(d)==2 and
                not isinstance(d[0],(list,dict,tuple)) and
                isinstance(d[1],dict) ) :
            return dict2ttl({d[0]: d[1]}, opt)
        else:
            return str.join("\n",[docs2ttl(x,opt) for x in d])
    if isinstance(d,dict):
        return dict2ttl(d, opt)
    if isinstance(d,tuple):
        if len(d)==3:
            return dict2ttl({d[0]: {d[1]: d[2]}}, opt)
        else:
            warn("????",d)

def dict2ttl(d:dict,opt={}):
    """ dict doc → turtle triples 
    
  explicit subject:(@id | @name | id | ID | name| title) in dict
     { @id : vi, ...dict-tail } →⇒   dict2ttl {vi : ...dict-tail }
     Ex: { "@id" : "João", 
                 "parent" : [ "D", "M"], 
                 "a" : "Person" }
       → (:João :parent :D)
         (:João :parent :M)
         (:João a :Person)

     { Manel : { pred : obj }}    
       → (:Manel :pred :ob)
     { Manel : { pred : setObs }} 
       → {(:Manel :pred :ob) | ob ∈ setObs}

     Ex: { "Manel": { "parent" : [ "D", "M"], "son": ["A","L"] }, 
                "Joana": { "a": "Person"} }
       → (:Manel :parent :D) 
         (:Manel :parent :M) 
         (:Manel :son :A) 
         (:Manel :son :L) 
         (:Joana a :Person)

     { "ont": val }  ⇒  doc2ttl(val)
     Ex:  { "@id": "Rui", "a": "Person", "ont": [ (a2,a3,a4),(a3,a4,{a4,a5,a6})]  },
       → (:rui a :Person)
         (:a2 :a3 :a4)
         (:a3 :a4 :a4)
         (:a3 :a4 :a5)
         (:a3 :a4 :a6)
"""
    r = ""
    rd = deepcopy(d)
    subj = opt.get("-s")
    ### { @id : vi, ...dict-tail } → {vi : ...dict-tail }
    if   "id" in d:          s = rd.pop("id");    rd = {s: rd}
    elif "ID" in d:          s = rd.pop("ID");    rd = {s: rd}
    elif "@id" in d:         s = rd.pop("@id");   rd = {s: rd}
    elif "name" in d:        s = rd.pop("name");  rd = {s: rd}
    elif "@name" in d:       s = rd.pop("@name"); rd = {s: rd}
    elif subj and subj in d: s = rd.pop(subj); rd = {s: rd}
#    else:                    s = f"FIXME2-{d.keys()}"; rd = {s: rd}

    for s,dd in rd.items():
        if match(r'@?ont(ology|ologia)?$',s,flags=re.I):
            r += docs2ttl(dd, opt)
            continue

        if not isinstance(dd,dict):
            warn("Error: expecting a dictionary, got a ",rd)
            dd = {"__DEBUG__": dd}

        for p,o in dd.items():
            if match(r'@?ont(ology|ologia)?$',p,flags=re.I):
                r += docs2ttl(o, opt)
            elif isinstance(o,(list,set)):
                for oo in o:
                    if isinstance(oo,dict):
                        r += dict2ttl({s: {p: oo}}, opt)
                    else:
                        r += tripttl(s,p,oo)
            elif isinstance(o,dict):
                for k in o:
                    r += tripttl(s,p,k)
                r += dict2ttl(o, opt)
            else:
                r += tripttl(s,p,o)
    return r

def tripttl(s, p, o, force=None, oty=None ):
    s1 = t2iri(s) 
    if pp := search(r'(.*)\^\^:?(.+)', p):
        oty = pp[2]
        p1 = t2iri(pp[1]) 
        force="lit"
    else:
        p1 = t2iri(p) 
       
    if   force is  None: o1 = t2iri_or_lit(o, rel=p, ty=oty)
    elif force == "lit": o1 = t2lit(o, rel=p, ty=oty)
    elif force == "iri": o1 = t2iri(o)
    return f'{s1} {p1} {o1} .\n'

###-----------------------------------------
### parse table (jjtable2ttl)
###-----------------------------------------


def parse_head(h: str, opt ):
    fs  = opt.get('-F','::')    ## fiel separator (def: "::")
    fs2 = ':'
    idclass,*ftits = split(fr'\s*{fs}\s*',h.strip())
    for i,f in enumerate(ftits):
        a = match(fr'(.+){fs2}(.+)',f)
        if a :
            ftits[i] = {"rel": a[1], "class": a[2]}
        else:
            ftits[i] = {"rel":f}
    return (idclass,ftits)

def parse_tup(t:str,idclass,ftits,opt ):
    fs  = opt.get('-F','::')
    fs2 = opt.get('-f','[;,|]')
    ont =[]
    id,*fields = split(fr'\s*{fs}\s*',t.strip())
    doc = {}
    for i,f in enumerate(fields):
        if not search(r'\S',f): 
            continue
        if i >= len(ftits):
            warn('To many fields ',id,fields)
            continue
        else:
            finf = ftits[i]
        if not search(r'\S',finf["rel"]): 
            continue
        a = [ x for x in split(fr'\s*{fs2}\s*',f) if search(r'\S',x) ]
        doc[finf["rel"]] = a
        if "class" in finf :
            for campo in a :
                ont.append( (campo, "type", finf["class"]))
    if ont:
        doc["ont"] = ont
    doc["@id"]= id
    doc["type"]= doc["type"]+[idclass] if "type" in doc else idclass
    return doc

def table2py(c):
    """ files(headerline + CSV(fs="::",fs2="[;,|]") → docs = [ doc ] """
    headopt = c.opt.get("-h")  ## ex: table2tt -h 'Person :: pai:Person :: f'
    docs =[]
    for txt in c.text():
        tabs = split(r'\s*@TAB\s*', txt)
        for tab in tabs:
            if not search(r'\w',tab):
                continue

            if headopt:
                head = headopt
                tups = [x for x in split(r'\s*\n\s*',tab) if match(r'\w',x)]
            else:
                head,*tups = [x for x in split(r'\s*\n\s*',tab) if match(r'\w',x)]

            idclass,ftits= parse_head(head,c.opt)
            for line in tups:
                doc= parse_tup(line,idclass,ftits,c.opt)
                if '-v' in c.opt:
                    doc["__file__"] = c.filename()
                docs.append(doc)

    return docs

def main_table2ttl():
    """
NAME
   jjtable2ttl - converts a "::" field separated table in turtle

SYNOPIS
   jjtable2tt [option] files > out.ttl
     Options:
       -F "="    field setarator "=" (def: "::")
       -f ":"    subfield separator ":" (def: [,;|])
       -h "Person :: son:Person :: year" define an external header

Example
   FIXME: incomplete
"""
    c = clfilter(opt="h:do:F:f:v", doc=main_table2ttl.__doc__) 
    ds = table2py(c)
    print(docs2ttl(ds,c.opt))

###-----------------------------------------
### parse a multi-yaml file: (jjyaml2ttl)
###-----------------------------------------

def yamls2py(c,files=None):
    """ files( ("---" yaml)+ ) → docs = [ doc ] """
    docs =[]
    
    for txt in c.slurp(files):
        isa_serie = "-c" in c.opt
        txt = sub(r'\t','    ',txt)  ## repl tabs (they are invalid in yaml)
        txt = sub(r'(\n\w+:)(\w)',r'\1 \2',txt)  ## (abc:def → abc: def)
        count = 0
        the_1 = None

        for txtd in re.split(r'\n---\s',txt):
            try:
                doc = yaml.safe_load(txtd)
            except Exception as e:
                warn("### Erro yaml de", c.filename(),e)
                continue
            count += 1  
            if not doc:
                continue
            if not isinstance(doc,dict):
                warn("### Erro invalid format:", c.filename(),doc, txtd )
                continue
            if the_1 is None :
                if isa_serie or doc.get("type") in {"serie", "list"}: ##.FIXME
                    isa_serie = True
                    the_1 = doc
                    parent = getid(the_1, c.opt)
                the_1 = doc
            else:
                if isa_serie:
                    if parent:
                        doc["pof"] = parent
                    doc["__index__"] = count

            if "-v" in c.opt:
                doc["__file__"] = f"{c.filename()}--{count}"
            docs.append(doc)
    return docs
    '''
        try:
            elems = yaml.safe_load_all(txt)
        except Exception as e:
            warn("### Erro yaml de", c.filename(),e)
            continue
        if not elems:
            continue
        count = 0
        for doc in elems: 
            count += 1  
            if not doc:
                continue
            if "-v" in c.opt:
                doc["__file__"] = f"{c.filename()}--{count}"
            if not isinstance(doc,dict):
                warn("### Erro invalid format:", c.filename(),doc)
                continue
            docs.append(doc)
    return docs
    '''

def main_yaml2ttl():
    """
NAME
   jjyaml2ttl - prints a turtle ontology from a (multi-doc)YAML

SYNOPSIS
   jjyaml2ttl [options] files
     -v       verbose

     -s nnn   nnn is the subject field id. (def: @id | @name | id | name)
     -c       multi-doc (first doc is the container; others are the parts)
             for i, x in enumerate(docs[1:])
                 subj(x) :pof subj(first doc)
                 subj(x) :_index_  i

     -p properties-table (FIXME: ignored for the moment)


Description
   yamldocs → turtle triples
   1) if YAMLdoc is tuple or list with the following shape:

      (s,p,o)  or [s,p,o] → :s :p :o.
           or more exactly⇒ dict2ttl({ s : {p : o}})

      [s, dict({pi:oi})] → :s :p1 :o1 ... :s :pi :oi .
           or more exactly⇒ dict2ttl({ s : dict(...)})

      list ⇒  join( "\n", [doc2ttl(v) v ∈ list] )

      dict ⇒  dict2ttl(dict)

   2) if YAMLdoc is a dict: dict → turtle triples 
    
      if doc has a explicit subject name: 
         ( @id | @name | id | ID | name) in dict
      
         { @id : vi, dict-tail } ⇒ dict2ttl {vi : dict-tail }
      Ex1:  { "@id" : "João", 
              "parent" : [ "D", "M"], 
              "a" : "Person" }
       → (:João :parent :D)
         (:João :parent :M)
         (:João a :Person)

      Ex2: {Manel : { pred : obj }}    
       → (:Manel :pred :ob)

      Ex3: {Manel : { pred : setObs }} 
      → { (:Manel :pred :ob) | ob ∈ setObs}
 
      Ex4: {Manel: {parent :[D, M], son: [A,L] }, 
            Joana: {a: Person} }
      → (:Manel :parent :D) 
        (:Manel :parent :M) 
        (:Manel :son :A) 
        (:Manel :son :L) 
        (:Joana a :Person)

      If doc has a "ont"|"ontology" key
      • { "ont": val }  ⇒  doc2ttl(val)
      Ex5: { "@id": "Rui", "a": "Person", "ont": [ (a2,a3,a4),(a3,a4,{a4,a5,a6})]  },
       → (:rui a :Person)
         (:a2 :a3 :a4)
         (:a3 :a4 :a4)
         (:a3 :a4 :a5)
         (:a3 :a4 :a6)
"""
    c = clfilter(opt ="do:F:f:vp:cs:",doc=main_yaml2ttl.__doc__)     
    ds = yamls2py(c)
    print(docs2ttl(ds, c.opt))

###-----------------------------------------
### Taxonomy
###-----------------------------------------

def FIXME_taxstr2py(c, rel="rdfs:subClassOf"):
    """ str ( ????  ) → docs = [ doc ] """
    top_name = "owl:Thing"
    inda = 0
    tabind = [-1]
    ant = [top_name]    

    for line in c.splitlines():
        if not search(r'\w',line): continue 

        if m := match(r'\s*#', line):
            print(line)
            continue
        if m := match(r'([ .-]*)(\S.*)', line):
            term = m[2] 
            ind = len(m[1])
        if ind <= inda :
            while len(tabind) and ind <= tabind[-1]:
                tabind.pop()
                ant.pop()
        tabind.append(ind)
        print( tripttl(term, rel, ant[-1], "iri" ),end="")
        ant.append(term) 
        inda = ind

def tax2py(c, rel="rdfs:subClassOf",files=None):
    """ files( ????  ) → docs = [ doc ] """
    if "-r" in c.opt:
        rel = c.opt["-r"]

    top_name = c.opt.get("-t", ":Thing")
    inda = 0
    tabind = [-1]
    ant = [top_name]    

    for line in c.input(files):
        if not search(r'\w',line): continue 

        if m := match(r'\s*#', line):
            print(line)
            continue
        if m := match(r'([ .-]*)(\S.*)', line):
            term = m[2] 
            ind = len(m[1])
        if ind <= inda :
            while len(tabind) and ind <= tabind[-1]:
                tabind.pop()
                ant.pop()
        tabind.append(ind)
        print( tripttl(term, rel, ant[-1], "iri" ),end="")
        ant.append(term) 
        inda = ind

def main_tax2ttl():
    """
NAME
    jjtax2ttl - converter indented taxonomy to turtle classes

SYNOPSIS
    jjtax2ttl [option] file.tax ...
      -r 'isSonOf'   - name of the subclass relation (def: 'rdfs:subClassOf')

Description
    Converts indented Class hierarchy in turtle. 
    Example 

     science
       physics
          dynamics
    #     statics       ...comment: removed for the moment 
       math
          algebra
          trignometry
     doc on literature

"""

    c = clfilter(opt ="do:r:t:v",doc=main_tax2ttl.__doc__)    
    tax2py(c)
#    ds = tax2py(c)
#    print(docs2ttl(ds, c.opt))

#!/usr/bin/python3
""" VERY EXPERIMENTAL :  module for opinied command line processing of OWL ontologies

# Synopsis

    owlcat  a.ttl b.owl c.ttl > all.ttl
      -t                - input in Turtle (def: based on extension)
      -f xml            - define output Format
      -n                - skip inference of new triples (def: infer)
      -o file
      ## concatenate → infer new triples → removeprefix

    owlclass a.ttl      
      -t                - input in Turtle (def: based on extension)
      -r                - keep transitive Redundances
      ## show class taxonomy

    owlgrep pattern a.ttl
      -t                - input in turtle (def: based on extension)
      -k                - just the IRI (default: term and adjacents)
       pattern :
         intanceRE
         classRE::instanceRE
      ## grep indivituals, class, or class:indi; ouput their triples

    owllabel2term a.ttl > new.ttl   
      -s nameSpace                  - default #
      ## rename IRIRef from rfds:label

    owlexpandpp a.ttl   - expand and pretty print
      -t                - input in turtle (def: based on extension)
      ##

    owlxdxf  a.ttl      
      -n dict_name      - title of the generated dictionary
      -t                - input in turtle (def: based on extension)
      -o out.xdxf       - redirects output (default stdout)
      ## Build a XDXF linked dictionary (seealso goldendict)

    jjtmd2ttl [option] file.t.md ...
      ## convert markdown with yaml metadate in turtle (seealso pandoc)

    jjyaml2ttl [option] file.t.yaml ...
      ## convert multi-yaml in turtle 

    jjtable2ttl [option] file.csv ...
      -F '#'            - Fiels separator (def: '::')
      -f ','            - sub field separatos (def: '[;,]')
      -h 'headerLine'   - set a "header line" (def: first line)
         Ex:   table2ttl -F : -h 'Id::uid::gid::name::' /etc/passwd
      ## convert csv  metadate in turtle 

    jjtax2ttl [option] file.tax ...
      -r 'isSonOf'      - subclass relation (def: 'rdfs:subClassOf')
      ## convert indented Class hierarky in turtle 

As a module:

    import jjowl
    ... FIXME

# Description
"""

__version__ = "0.2.3"

from jjcli import *
from jjowl.reindent import *
import os
from unidecode import unidecode
import json
import yaml
import owlrl
from   owlrl import convert_graph   ## , RDFXML, TURTLE, JSON, AUTO, RDFA
import rdflib
from   rdflib.namespace import RDF, OWL, RDFS, SKOS, FOAF, Namespace


def OFF_best_name_d(g : rdflib.Graph) -> dict :
   """ FIXME: IRIRef -> str based on RDFS.label, id, ??? """
   bestname={}
   for n in g.all_nodes():
       if islit(n): continue
       if name := g.preferredLabel(n) :
           bestname[s]=name[0].strip()
       else:
           txt = term.n3(g.namespace_manager)
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           bestname[s]=txt.strip()
   return bestname
#   for s,p,o in g.triples((None,RDFS.label,None)):
#   return


def get_invs(g: rdflib.Graph) -> dict :
   """Dictionary of inverse relations (based on inverseOf and SymetricProperty"""
   inv = {OWL.sameAs: OWL.sameAs}
   for s,p,o in g.triples((None,OWL.inverseOf,None)):
       inv[s]=o
       inv[o]=s
   for s,p,o in g.triples((None,RDF.type, OWL.SymmetricProperty)):
       inv[s]=s
   return inv

def reduce_graph(g,fixuri=None,fixlit=None)-> rdflib.Graph:
   def fix(item):
        if islit(item) and fixlit:
            return rdflib.term.Literal(fixlit(str(item)))
        if isinstance(item, rdflib.term.URIRef) and fixuri:
            return rdflib.term.URIRef(fixuri(str(item)))
        return item

   fixed = rdflib.Graph()
   fixed.bind('owl', OWL)
   fixed.bind('rdf', RDF)
   fixed.bind('rdfs', RDFS)
   fixed.bind('skos', SKOS)
   fixed.bind('foaf', FOAF)

   fixed += [ (fix(s), fix(p), fix(o)) for s,p,o in g]
   return fixed

def concatload(files:list, opt: dict) -> rdflib.Graph :
   ns = opt.get("-s",'#')
   g = rdflib.Graph(base=ns)
   g.bind("",rdflib.Namespace(ns))
   g.namespace_manager.bind('owl', OWL)
   g.bind('rdf', RDF)
   g.bind('rdfs', RDFS)
   g.bind('skos', SKOS)
   g.bind('foaf', FOAF)
   for f in files:
      if ".n3" in f or ".ttl" in f or "-t" in opt:
         try:
             g.parse(f,format='n3')    ## more flexible than turtle
         except Exception as e:
             warn("#### Error in ", f,e)
      else:
         try:
             g.parse(f)                ## format='xml'
         except Exception as e:
             warn("#### Error in ", f,e)
   return g

def concat(files:list, opt: dict) -> rdflib.Graph :
   ns=opt.get("-s",'#')
   g=concatload(files, opt)
   def fixu(t):
      if str(RDF) in t or str(OWL) in t or str(RDFS) in t :
          return t
      else:
          return  sub(r'(http|file).*[#/]',ns,t)

   g2=reduce_graph(g, fixuri=fixu)
   g2.bind("",ns)
   return g2

def termcmp(t):
   return  unidecode(sub(r'.*[#/]','',t).lower())

def islit(t):
   return isinstance(t,rdflib.term.Literal)

###----------------------
### main entry points
###----------------------

def mcat():           # main for owlcat
   '''
    # Synopsis

    owlcat  a.ttl b.owl c.ttl > all.ttl
      -t          - input in Turtle (def: based on extension)
      -f xml      - define output Format (def: turtle)
      -n          - skip inference of new triples (def: infer)
      -o file
      -s namepace    - namespace for ":"    (def: #)

    # description

      ## concatenate → infer new triples → removeprefix
   '''

   c=clfilter(opt="i:f:no:s:t" , doc=mcat.__doc__)
   g=owlproc(c.args,c.opt)
   g.serial()

def mlabel2term():    # main for owllabel
   '''
   '''
   c=clfilter(opt="f:kpcno:s:t", doc=mlabel2term.__doc__)
   g=owlproc(c.args,c.opt)
   g.rename_label2term()
   g.serial()

def mgrep():          # main for owlgrep
   '''
   # Name: owlgrep

    owlgrep pattern a.ttl
      -t                - input in turtle (def: based on extension)
      -k                - just the IRI (default: term and adjacents)
       pattern :
         intanceRE
         classRE::instanceRE

    # Description

     grep inputpattern: individuals, class, or class:indi; 
          ouput: their triples
   '''
   c=clfilter(opt="f:kpco:s:t", doc=mgrep.__doc__)
   pat=c.args.pop(0)
   g=owlproc(c.args,c.opt)
   if v:= match(r'(.+?)::(.+)',pat):
       g.grep2(v[1],v[2])
   else:
       g.grep(pat)

def mexpandpp():       # main for owlexpand
   c=clfilter(opt="kpco:s:t")
   g=owlproc(c.args,c.opt)
   g.pprint()

def mxdxf():           # main for owlxdxf
   '''
   '''
   c=clfilter(opt="b:no:s:t", doc=mxdxf.__doc__)
   if "-b" not in c.opt:
       basedir = os.path.dirname(os.path.realpath(c.args[0]))
       c.opt["-b"]=basedir
   g=owlproc(c.args,c.opt)
   g.xdxf()

def mhtml():           # main for owlhtml
   '''
   '''
   c=clfilter(opt="b:no:s:t", doc=mhtml.__doc__)
   if "-b" not in c.opt:
       basedir = os.path.dirname(os.path.realpath(c.args[0]))
       c.opt["-b"]=basedir
   g=owlproc(c.args,c.opt)
   g.html()

def mclass():          # main for owlclass
   '''
    owlclass a.ttl      
      -t                - input in Turtle (def: based on extension)
      -r                - keep transitive Redundances
      ## show class taxonomy
   '''
   c=clfilter(opt="no:rs:t", doc=mclass.__doc__)
   g=owlproc(c.args,c.opt)
   g.pptopdown(OWL.Thing)

def mprops():          # main for owlprop
   '''
   '''
   c=clfilter(opt="no:rs:t", doc=mprops.__doc__)
   g=owlproc(c.args,c.opt)
   g.ppprops()

###-----------------
### owlproc
###-----------------

class owlproc:
   """ Class for process owl ontologies
      .opt
      .g
      .inv
      .instances :  tipo -> [indiv]
      .subcl   : class -> {class}
      .supcl   : class -> {class}
      .supcltc : class -> {class}

   """
   def __init__(self,ontos,
                     opt={},
                     ):
       self.opt=opt
       if "-s" not in self.opt:    ## default name space
           self.ns='#'
       else:
           self.ns=self.opt["-s"]

       self.g=concat(ontos,opt)
       if "-n" not in self.opt:
           self._infer()
       self.inv=get_invs(self.g)
       self._get_subclass()
       self._instances()
       self.IT = Namespace(self.ns)

   def serial(self,fmt="turtle"): ## serializer to fmt (def:turtle)
       if "-f" in self.opt :
           fmt = self.opt["-f"]
       print(self.g.serialize(format=fmt))

   def _pp(self,term) -> str:
       """ returns a Prety printed a URIRef or Literal """
       return term.n3(self.g.namespace_manager)

   def _instances(self):
       self.instances={}
       for s,p,o in self.g.triples((None,RDF.type, None)):
           self.instances[o]=self.instances.get(o,[]) + [s]

   def _infer(self):
       owlrl.DeductiveClosure(owlrl.OWLRL_Extension_Trimming ).expand(self.g)

###------------------
### owl-props
###------------------

   def ppprops(self):
      predbag={}
      predtyp={}
      for s in self.g.subjects(predicate=RDF.type,object=OWL.ObjectProperty): 
          predbag[s]=0
          predtyp[s]="ObjectProperty"
      for s in self.g.subjects(predicate=RDF.type,object=OWL.DatatypeProperty): 
          predbag[s]=0
          predtyp[s]="DatatypeProperty"
      for p in self.g.predicates():
          predbag[p]=predbag.get(p,0)+1 
      for p in predbag.keys():
          for s,o in self.g.subject_objects(p):   ## ↓ p o
              if islit(o):
                 predtyp[p]="DatatypeProperty"
              else:
                 predtyp[p]="ObjectProperty"
              break
      for p,n in sorted(predbag.items()):
          print(f'{self._pp(p)} a {predtyp[p]} . # {n} ')


###---------------------
### XDXF
###---------------------
#  p.xdxf()               // ONT → xdxf-file
#  p._xpp(term) → str     // a xdxf Pretyprinted URIRef
#  p._term_inf_xdxf(n,f): // ONT , 

   def xdxf(self):
      if "-o" in self.opt:
          f = open(self.opt["-o"],"w",encoding="utf-8")
      else:
          f = sys.stdout
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      if "-n" in self.opt:
          title=self.opt["-n"]
      else:
          title="Dicionário"

      print( reindent( f"""
          <?xml version="1.0" encoding="UTF-8" ?>
          <xdxf lang_from="POR" lang_to="DE" format="logical" revision="033">
              <meta_info>
                  <title>{title}</title>
                  <full_title>{title}</full_title>
                  <file_ver>001</file_ver>
                  <creation_date></creation_date>
              </meta_info>
          <lexicon>
         """), file=f)

      for n in sorted(self.g.all_nodes(), key=termcmp):
          if islit(n): continue
          if n in [OWL.Thing, OWL.Nothing, RDFS.Class] : continue
          self._term_inf_xdxf(n,f)  ## FIXME
      print("</lexicon>\n</xdxf>",file=f)
      if "-o" in self.opt:
          f.close()

   def _term_inf_xdxf(self,n,f):
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      print("",file=f)
      print(f'<ar><k>{self._xpp(n)}</k><def>',file=f) ####  AR
      cls = self._simplify_classes(self.g.objects(subject=n,predicate=RDF.type),
                                 strat="bu")
      for c in cls:                                     ## class
          print( f"<kref>{self._xpp(c)}</kref>",
                 file=f)
      for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o
          if p in ignore_pred: continue
          ppstr=self._pp(p)
          opstr=self._pp(o)
          pstr=self._xpp(p)
          ostr=self._xpp(o)
          if ppstr in {':img','IMG',':jpg',':png'}:
              print(f"   <def><img width='500px' src={opstr}/></def>",
                    file=f)
          elif ppstr in {':pdf',':url',':midi'}:
              if "-b" in self.opt:
                  aux = opstr.strip('"')
                  basedir = self.opt["-b"]
                  url = f'"file:///{basedir}/{aux}"'
              print(f"   <def><iref href={url}>{pstr} ↗</iref></def>",
                    file=f)
          elif islit(o):
              print(f"   <def>{pstr}: {ostr}</def>",
                    file=f)
          else:
              print(f"   <def>{pstr}: <kref>{ostr}</kref></def>",
                    file=f)

      for s,p in sorted(self.g.subject_predicates(n)):   ## s p ↓
          if p in ignore_pred  or p in self.inv: continue
          print(f"   <def><kref>{self._xpp(s)}</kref>  {self._xpp(p)} *</def>",
                file=f)
      if n in self.instances:
          for i in sorted(self.instances[n],key=termcmp):
              print(f" <def><kref>{self._xpp(i)}</kref></def>",
                    file=f)
      print(f'</def></ar>', file=f)                    ####  /AR


   def _xpp(self,term) -> str:
       """ returns a xdxf Prety printed URIRef """
       txt = self._pp(term)
       txt = sub(r'\\"','"',txt)
       if islit(term):
           txt = sub(r'[<>&]','§',txt)
           txt = sub(r'§(/?)(sup|def|br|kref|b|i|iref|img)\b(.*?)§',r'<\1\2\3>',txt)
           txt = txt.strip("""'" \t\n""")
           if '"""' in txt  or "'''" in txt:
               return "<deftext>"+ txt + "</deftext>"
           elif match(r'(.+)\.(jpe?g|png|pdf|svg)$', txt):
               return txt
           else:
               return txt
       else:
           txt = txt.strip("""'" \t\n""")
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           txt = sub(r'[<>&]','§',txt)
           txt = sub(r'§(/?)(sup|def|br|kref|b|i|iref|img)\b(.*?)§',r'<\1\2\3>',txt)
           return txt

###---------------------
### grep
###---------------------

   def grep(self,pat):
       for n in sorted(self.g.all_nodes(), key=termcmp):
           if islit(n): continue
           if n in [OWL.Thing, OWL.Nothing, RDFS.Class] : continue
           npp = self._pp(n)
           if search( pat, npp, flags=re.I):
               if "-k" in self.opt:
                   print(npp)
               else:
                   self._pterm_inf(n)

   def grep2(self,patc,pati):
       for s,o in self.g.subject_objects(RDF.type):
           opp = self._pp(o)
           if search( patc, opp, flags=re.I):
               spp = self._pp(s)
               if search( pati, spp, flags=re.I):
                   if "-k" in self.opt:
                       print(f'{opp}::{spp}')
                   else:
                       self._pterm_inf(s)

###---------------------
### classes of the ontology
###---------------------

   def _get_subclass(self):
      self.subcl   = {}
      self.supcl= {OWL.Thing: set()}
      self.supcltc = {}
      for s,p,o in self.g.triples((None,RDF.type,None)):
          self.subcl.setdefault(o,set())
          self.supcl.setdefault(o,set())
      for s,p,o in self.g.triples((None,RDFS.subClassOf,None)): # s < o
          self.subcl.setdefault(s,set())
          self.subcl.setdefault(o,set())
          self.supcl.setdefault(s,set())
          self.supcl.setdefault(o,set())
          self.supcl[s].add(o)
          self.subcl[o].add(s) 

      roots= set()
      for x,s in self.supcl.items():
          if x == OWL.Thing: continue
          if s == set():
              roots.add(x)
              self.supcl[x].add(OWL.Thing)
          if s == { OWL.Thing }:
              roots.add(x)
      self.subcl[OWL.Thing] = roots

      self.mksupcltc(OWL.Thing)
      self._simplify_subcl()
      self._simplify_supcl()

   def mksupcltc(self, top, vis={}, acu=set() ):
       if top in vis: return
       vis[top] = 1
       self.supcltc[top] = acu | self.supcl[top]
       for child in self.subcl.get(top,[]):
           self.mksupcltc( child, vis, acu=self.supcltc[top] )

   def pptopdown(self,top,vis={},indent=0,max=1000):
       if max <= 0  : return
       if top in vis: return
       vis[top]=1
       print( f'{"  " * indent}{self._pp(top)}' )
       scls=self.subcl.get(top,[])
#       if "-r" not in self.opt:
#           scls=self._simplify_classes(self.subcl.get(top,[]))
       for a in sorted(scls,key=termcmp):
           self.pptopdown(a,vis,indent+2,max-1)

   def _topdown(self,top,vis={},max=1000):
       if max == 1  : return self._pp(top)
       if max <= 0  : return None
       if top in vis: return None
       vis[top]=1
       scls=self.subcl.get(top, set())
#       scls=self._simplify_classes(scls)
       childs=[]
       if childs is []: 
           return (self._pp(top), )
       else:
           for a in sorted(scls,key=termcmp):
               childs.append(self._topdown(a,vis,max-1))
           return (self._pp(top), childs)

   def _simplify_subcl(self):
       for c1, c2s in self.subcl.items():
           aux = c2s - { OWL.NamedIndividual, OWL.Nothing, RDFS.Class}
           for x in aux.copy():
               ys = self.supcltc.get(x,set())
               if len(ys & aux) > 0 :
                   aux.remove(x)
           self.subcl[c1]=aux

   def _simplify_supcl(self):
       for c1, c2s in self.supcl.items():
           aux = c2s - { OWL.NamedIndividual, OWL.Nothing, RDFS.Class}
           for x in aux.copy():
               ys = self.supcltc.get(x,set())
               aux -= ys
           self.supcl[c1]=aux

   def _simplify_classes(self, cls:list, strat="td") -> list:
       """ FIXME: remove redundant class from a class list"""
       aux = set(cls) - {OWL.Thing, OWL.NamedIndividual, OWL.Nothing, RDFS.Class}
       for x in aux.copy():
           ys = self.supcltc.get(x,set())
           if strat == "td":
               if len(ys & aux) > 0 :
                   aux.remove(x)
           else:    ## "bu"
               aux -= ys
       return aux

###----------------
### label to 
###----------------

   def rename_label2term(self) -> rdflib.Graph :
       newname = {}

       for s,o in self.g.subject_objects(RDFS.label):
           base = sub(r'(.*[#/]).*',r'\1',str(s))
           newid = sub(r' ','_', str(o).strip())
           newname[str(s)] = base + newid

       for s,o in self.g.subject_objects(SKOS.prefLabel):
           base = sub(r'(.*[#/]).*',r'\1',str(s))
           newid = sub(r' ','_', str(o).strip())
           newname[str(s)] = base + newid

       def rename(t):
          if str(RDF) in t or str(OWL) in t or str(RDFS) in t or str(SKOS) in t:
              return t
          else:
              taux = newname.get(t,t)
              return sub(r'(http|file).*[#/]',self.ns,taux)
       g2=reduce_graph(self.g, fixuri=rename)
       g2.bind("",self.ns)
       self.g = g2

   def _pterm_inf(self,n,opt={}):
       ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
          OWL.equivalentProperty }

       print("====")
       print(self._pp(n))
       cls = self._simplify_classes(self.g.objects(subject=n,predicate=RDF.type),
                                  strat="bu")
       for c in cls:
           print("   ", self._pp(c))

       prevpred=""
       for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o
           p_pp = self._pp(p)
           if p_pp != prevpred: 
               print( "       ", p_pp)
               prevpred = p_pp
           print( "           ", self._pp(o))

#       for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o
#           if p in ignore_pred: continue
#           print( "       ", self._pp(p), self._pp(o))

       for s,p in sorted(self.g.subject_predicates(n)):   ## s p ↓
           if p in ignore_pred: continue
           if p in self.inv: continue
           print( "       ", self._pp(s), self._pp(p), "*")

   def pprint(self):
       for n in sorted(self.g.all_nodes(), key=termcmp):
           if islit(n): continue
           if n in [OWL.Thing, OWL.Nothing, RDFS.Class] : continue
           self._pterm_inf(n)

###---------------------
### HTML
###---------------------

   def html(self):
      if "-o" in self.opt:
          f = open(self.opt["-o"],"w",encoding="utf-8")
      else:
          f = sys.stdout
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      if "-n" in self.opt:
          title=self.opt["-n"]
      else:
          title="Dicionário"

      print(f"""<html><head> <title>{title}</title>""",
          reindent("""
              <meta charset="UTF-8"/>
              <style>
                 section {
                   background-color: #ffffff;
                   margin: 10px;
                   border: solid 1px #999999;
                   padding: 5px;
                   clear:both;
                 }

                 b[lang] { color: red; }

                 img { object-fit: contain; }

                 /* img.r { float: right; }
                 img.r::after { content: ""; clear: both; display: table;
                 } */

                 a { color: #000099; text-decoration: none; }
                 a:hover { color: #0000ff; text-decoration: underline;  }
                 
                 ul { list-style-type: none; }
                 li.lingua strong { color: #009900;}
                 li.lingua a { font-style: italic; /* text-transform: lowercase; */ }
                 li.lingua { margin-bottom: 2px; } 

                 li.rel strong  { color: #999900; }
                 li.text strong { color: #009999; }
                 li.text        { padding-top: 10px; padding-bottom: 10px; }
              </style>
              <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
              </head>
              <body>

              <input type="text" id="myInput" onkeyup="myFunction()" 
                     placeholder="Search for names.." title="Type in a name"/>

              """), file=f)

      for n in sorted(self.g.all_nodes(), key=termcmp):
          if islit(n): continue
          if n in [OWL.Thing, OWL.Nothing, RDFS.Class] : continue
          self._term_inf_html(n,f)  ## FIXME

      print(reindent("""
          <script>
             function myFunction() {
                var input, filter, sections, term, i, txtValue;
                input = document.getElementById("myInput");
                filter = input.value.toUpperCase();
                sections = document.getElementsByTagName("section");
                for (i = 0; i < sections.length; i++) {
                   term = sections[i].getElementsByTagName("strong")[0];
                   if (term) {
                      txtValue = term.textContent || term.innerText;
                      if (txtValue.toUpperCase().indexOf(filter) > -1) {
                         sections[i].style.display = "";
                      } else {
                         sections[i].style.display = "none";
                      }
                   }
                }
             }
             
             function ensurevisid(a) {
                sec = document.getElementById(a);
                if(sec){ sec.style.display=""; }
             }
             
             marks = document.getElementsByClassName("markdown");
             for (i = 0; i < marks.length; i++) {
                marks[i].innerHTML = marked.parse( marks[i].innerHTML );
             }
 
          </script>
          </body>\n</html>
          """), file=f)
      if "-o" in self.opt:
          f.close()


   def _term_inf_html(self,n,f):
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      print(reindent(f"""
          <section id='{self._hpp(n)}'>
          <strong>{self._hpp(n)}</strong>
          <ul>

          """), file=f)
      cls = self._simplify_classes(self.g.objects(subject=n,predicate=RDF.type),
                                 strat="bu")
#      cls = self.supcl.get(n,set())
      print("<li>",file=f)
      for c in cls:                                     ## class
          print( f"<a href='#{self._hpp(c)}'>{self._hpp(c)}</a>", file=f)
      print("</li>",file=f)

      print("<ol>",file=f)
      for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o
          if p in ignore_pred: continue
          ppstr = self._pp(p)
          opstr = self._pp(o)
          pstr = self._hpp(p)
          ostr = self._hpp(o)
          if ppstr in {':img','IMG',':jpg',':png'}:
              print(f"   <li><img width='500px' src={opstr}/></li>",
                    file=f)
          elif ppstr in {':pdf',':url',':midi'}:
              if "-b" in self.opt:
                  aux = opstr.strip('"')
              print(f"   <li><a href='{aux}'>{pstr} ↗</a></li>",
                    file=f)
          elif islit(o):
              print(f"   <li>{pstr}: {ostr}</li>",
                    file=f)
          else:
              print(f"   <li>{pstr}: <a href='#{ostr}'>{ostr}</a></li>",
                    file=f)

      print("</ol>",file=f)
      for s,p in sorted(self.g.subject_predicates(n)):   ## s p ↓
          if p in ignore_pred  or p in self.inv: continue
          print(f"   <li><a href='#{self._hpp(s)}'>{self._hpp(s)}</a>  {self._hpp(p)} *</li>",
                file=f)
      if n in self.instances:
          print("<li>Instances <ol>",file=f)
          for i in sorted(self.instances[n],key=termcmp):
              print(f" <li><a href='#{self._hpp(i)}'>{self._hpp(i)}</a></li>",
                    file=f)
          print("</ol></li>",file=f)
      print(f'</ul></section>', file=f)                    ####  /AR


   def _hpp(self,term) -> str:
       """ returns a html-Pretty-printed URIRef """
       txt = self._pp(term)
       txt = sub(r'\\"','"',txt)
       if islit(term):
           txt = sub(r'[<>&]','§',txt)
           txt = sub(r'§(/?)(sup|def|br|a|b|i|p|iref|img)\b(.*?)§',r'<\1\2\3>',txt,flags=re.I)
           txt = txt.strip("""'" \t\n""")
           if '"""' in txt  or "'''" in txt:
               return "<div>"+ txt + "</div>"
           elif match(r'(.+)\.(jpe?g|png|pdf|svg)$', txt):
               return txt
           else:
               return txt
       else:
           txt = txt.strip("""'" \t\n""")
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           txt = sub(r'[<>&]','§',txt)
           txt = sub(r'§(/?)(sup|def|br|a|b|i|p|iref|img)\b(.*?)§',r'<\1\2\3>',txt)
           return txt


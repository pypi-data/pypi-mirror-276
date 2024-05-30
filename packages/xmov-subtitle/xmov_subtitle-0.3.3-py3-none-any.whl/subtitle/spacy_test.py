
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_md')
doc = nlp( "great product, very easy to use and great graphics." )
displacy.serve(doc, style='dep')
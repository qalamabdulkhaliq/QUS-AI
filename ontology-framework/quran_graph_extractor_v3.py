import re
import json
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL
import time
import urllib.parse

class QuranRootExtractorV3:
    def __init__(self, corpus_path):
        self.corpus_path = Path(corpus_path)
        self.g = Graph()
        
        # Namespaces
        self.QURAN = Namespace("http://ontology.quran/")
        self.ROOT = Namespace("http://ontology.quran/root/")
        self.LEMMA = Namespace("http://ontology.quran/lemma/")
        self.ALIGN = Namespace("http://ontology.alignment/core#")
        
        self.g.bind("quran", self.QURAN)
        self.g.bind("root", self.ROOT)
        self.g.bind("lemma", self.LEMMA)
        self.g.bind("align", self.ALIGN)

    def clean_uri_segment(self, val):
        # URL encode to handle Buckwalter characters like {, }, ^, <, >
        return urllib.parse.quote(val)

    def parse_features(self, feature_str):
        features = {}
        parts = feature_str.split('|')
        for part in parts:
            if ':' in part:
                key, val = part.split(':', 1)
                features[key] = val
            else:
                features[part] = True
        return features

    def process(self):
        print(f"Processing Root Ontology v3 from {self.corpus_path.name}...")
        start_time = time.time()
        
        source_uri = self.QURAN["surah0_SOURCE"]
        self.g.add((source_uri, RDF.type, self.ALIGN.NecessaryBeing))
        
        count = 0
        with open(self.corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('('):
                    parts = line.split('\t')
                    if len(parts) < 4:
                        continue
                        
                    loc_str = parts[0].strip('()')
                    form = parts[1]
                    tag = parts[2]
                    feature_str = parts[3].strip()
                    
                    s, v, w, seg = loc_str.split(':')
                    
                    segment_id = f"s{s}v{v}w{w}seg{seg}"
                    segment_uri = self.QURAN[segment_id]
                    
                    self.g.add((segment_uri, RDF.type, self.ALIGN.ContingentBeing))
                    self.g.add((segment_uri, self.QURAN.form, Literal(form)))
                    self.g.add((segment_uri, self.QURAN.pos, Literal(tag)))
                    
                    self.g.add((source_uri, self.QURAN.creates, segment_uri))
                    
                    features = self.parse_features(feature_str)
                    
                    if 'ROOT' in features:
                        root_val = features['ROOT']
                        safe_root = self.clean_uri_segment(root_val)
                        root_uri = self.ROOT[safe_root]
                        self.g.add((segment_uri, self.QURAN.hasRoot, root_uri))
                        self.g.add((root_uri, RDF.type, self.QURAN.ArabicRoot))
                        self.g.add((root_uri, RDFS.label, Literal(root_val)))
                        
                    if 'LEM' in features:
                        lem_val = features['LEM']
                        safe_lem = self.clean_uri_segment(lem_val)
                        lem_uri = self.LEMMA[safe_lem]
                        self.g.add((segment_uri, self.QURAN.hasLemma, lem_uri))
                        self.g.add((lem_uri, RDF.type, self.QURAN.Lemma))
                        self.g.add((lem_uri, RDFS.label, Literal(lem_val)))
                        
                    count += 1
                    if count % 20000 == 0:
                        print(f"Processed {count} segments...")
        
        print(f"Extraction complete. Total segments: {count}")
        print(f"Serializing to Turtle...")
        
        output_path = self.corpus_path.parent / "quran_root_ontology_v3.ttl"
        self.g.serialize(destination=str(output_path), format="turtle")
        print(f"✓ Saved to {output_path}")
        print(f"Total time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    corpus_file = r"C:\Users\amlan\OneDrive\Desktop\QUS-AI Islamic Alignment\quranic-corpus-morphology-0.4.txt"
    extractor = QuranRootExtractorV3(corpus_file)
    extractor.process()
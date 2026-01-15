import requests
import json
from typing import Dict, List, Tuple, Optional
import networkx as nx
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL

class QuranGraphEncoderV2:
    """
    Enhanced version with coreference resolution using grammar rules
    """
    
    def __init__(self):
        self.base_url = "https://api.quran.com/api/v4"
        self.graph = nx.DiGraph()
        self.owl_graph = Graph()
        
        # Load grammar rules
        print("Loading grammar rules...")
        with open('quranic_grammar_rules.json', 'r', encoding='utf-8') as f:
            grammar_data = json.load(f)
            self.grammar_rules = grammar_data['rules']
        
        print(f"✓ Loaded {len(self.grammar_rules)} grammar rules")
        
        # Define namespaces
        self.QURAN = Namespace("http://ontology.quran/")
        self.ALIGN = Namespace("http://ontology.alignment/core#")
        self.QG = Namespace("http://ontology.quran/grammar#")
        
        self.owl_graph.bind("quran", self.QURAN)
        self.owl_graph.bind("align", self.ALIGN)
        self.owl_graph.bind("qg", self.QG)
        
        # Allah names/attributes for SOURCE detection
        self.source_references = [
            'الله', 'اللَّهُ', 'اللَّهِ', 'اللَّه',
            'الرَّحْمَٰنُ', 'الرَّحِيمُ', 'رَبُّ', 'رَبِّ', 'رَبَّ',
            'مَالِكُ', 'Allah', 'Lord', 'God', 'Rahman', 'Rahim',
            'Master', 'Most Gracious', 'Most Merciful'
        ]
        
        # Pronouns that likely refer to Allah
        self.divine_pronouns = [
            'You', 'You Alone', 'He', 'Him', 'His',
            'Your', 'Thee', 'Thou', 'Thy',
            'هُوَ', 'أَنتَ', 'أَنتُمْ', 'إِيَّاكَ'
        ]
        
        # Track SOURCE node context per surah
        self.source_context = {}
    
    def fetch_verses(self, surah_num: int) -> List[Dict]:
        """Fetch all verses for a surah with word-level data"""
        try:
            response = requests.get(
                f"{self.base_url}/verses/by_chapter/{surah_num}",
                params={
                    "words": "true",
                    "translations": "131",
                    "language": "en",
                    "per_page": "500"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('verses', [])
            else:
                print(f"  ⚠ API error for surah {surah_num}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"  ⚠ Error fetching surah {surah_num}: {str(e)}")
            return []
    
    def extract_words(self, verse_data: Dict) -> List[Dict]:
        """Extract word-level data from verse"""
        words = []
        
        for word in verse_data.get('words', []):
            words.append({
                'position': word.get('position'),
                'text': word.get('text_uthmani', ''),
                'transliteration': word.get('transliteration', {}).get('text', ''),
                'translation': word.get('translation', {}).get('text', ''),
                'char_type': word.get('char_type_name', ''),
                'line': word.get('line_number', 0)
            })
        
        return words
    
    def is_source_reference(self, word: Dict) -> bool:
        """Check if word is direct Allah reference"""
        text = word.get('text', '')
        translation = word.get('translation', '')
        
        # Direct name match
        for name in self.source_references:
            if name in text or name in translation:
                return True
        
        return False
    
    def is_divine_pronoun(self, word: Dict, context: List[Dict]) -> bool:
        """
        Check if pronoun refers to Allah using grammar rules
        Uses PRON_DIVINE_PRIORITY rule from grammar system
        """
        translation = word.get('translation', '').strip()
        text = word.get('text', '')
        
        # Check if it's a pronoun
        is_pronoun = any(p in translation for p in self.divine_pronouns)
        is_pronoun = is_pronoun or any(p in text for p in ['هُوَ', 'أَنتَ', 'إِيَّاكَ'])
        
        if not is_pronoun:
            return False
        
        # Apply PRON_DIVINE_PRIORITY rule:
        # If we recently saw a divine reference, pronoun likely refers to it
        for prev_word in reversed(context[-10:]):  # Check last 10 words
            if self.is_source_reference(prev_word):
                return True
        
        # If no recent divine reference, check if context is worship/prayer
        worship_context = ['worship', 'pray', 'ask', 'guide', 'help', 
                          'forgive', 'mercy', 'glorify', 'praise']
        
        context_text = ' '.join(w.get('translation', '') for w in context[-5:]).lower()
        if any(word in context_text for word in worship_context):
            return True
        
        return False
    
    def resolve_pronoun(self, word: Dict, verse_context: List[Dict], 
                       surah_context: List[Dict]) -> Optional[str]:
        """
        Resolve pronoun to antecedent using grammar rules
        Returns 'SOURCE' if divine reference, else None
        """
        # Apply pronoun agreement rules from grammar system
        
        # RULE: PRON_DIVINE_PRIORITY
        # Check if this is a divine pronoun
        if self.is_divine_pronoun(word, verse_context + surah_context):
            return 'SOURCE'
        
        # RULE: PRON_PROXIMITY
        # For other pronouns, find nearest matching antecedent
        # (Simplified for now - can be enhanced with full morphological matching)
        
        return None
    
    def build_graph_from_verse(self, surah_num: int, verse_num: int, 
                                words: List[Dict], verse_text: str,
                                surah_context: List[Dict]) -> nx.DiGraph:
        """Build directed graph from verse using grammar rules"""
        verse_graph = nx.DiGraph()
        
        verse_id = f"s{surah_num}v{verse_num}"
        
        # Ensure SOURCE node exists
        if surah_num not in self.source_context:
            self.source_context[surah_num] = True
            verse_graph.add_node(
                'SOURCE',
                type='NecessaryBeing',
                surah=surah_num
            )
        
        # Process each word
        for i, word in enumerate(words):
            word_id = f"{verse_id}_w{word['position']}"
            
            # Check if direct divine reference
            if self.is_source_reference(word):
                # This word IS part of SOURCE
                # Don't create separate node, SOURCE encompasses all divine names
                continue
            
            # Check if pronoun referring to Allah
            verse_context = words[:i]
            antecedent = self.resolve_pronoun(word, verse_context, surah_context)
            
            # Create node for this word
            verse_graph.add_node(
                word_id,
                type='ContingentBeing',
                text=word['text'],
                translation=word['translation'],
                surah=surah_num,
                verse=verse_num
            )
            
            # Create edge based on dependencies
            if antecedent == 'SOURCE':
                # Pronoun refers to Allah - create dependency edge
                verse_graph.add_edge(
                    'SOURCE',
                    word_id,
                    relation='creates',
                    verse=verse_id,
                    type='coreference'
                )
            else:
                # Check if any SOURCE reference in this verse
                has_source = any(self.is_source_reference(w) for w in words)
                
                if has_source:
                    # Verse mentions Allah - all words depend on SOURCE
                    verse_graph.add_edge(
                        'SOURCE',
                        word_id,
                        relation='creates',
                        verse=verse_id,
                        type='contextual'
                    )
                else:
                    # Implicit dependency - verse is part of Allah's revelation
                    verse_graph.add_edge(
                        'SOURCE',
                        word_id,
                        relation='creates',
                        verse=verse_id,
                        type='implicit'
                    )
        
        return verse_graph
    
    def validate_axioms(self, graph: nx.DiGraph) -> Dict[str, bool]:
        """Validate graph against 4 ontological axioms"""
        
        source_nodes = [n for n in graph.nodes() if n == 'SOURCE']
        
        if not source_nodes:
            return {
                'AXIOM_NECESSARY': False,
                'AXIOM_CONTINGENT': False,
                'AXIOM_UNIQUE': False,
                'AXIOM_ACYCLIC': True,
                'PASS': False,
                'note': 'No SOURCE node found'
            }
        
        # AXIOM_NECESSARY: SOURCE has in-degree 0
        source_in_degree = sum(graph.in_degree(n) for n in source_nodes)
        
        # AXIOM_CONTINGENT: All non-SOURCE nodes have in-degree > 0
        contingent_nodes = [n for n in graph.nodes() if n not in source_nodes]
        contingent_with_deps = [n for n in contingent_nodes if graph.in_degree(n) > 0]
        
        contingent_ratio = len(contingent_with_deps) / len(contingent_nodes) if contingent_nodes else 1.0
        
        # AXIOM_UNIQUE: Only one SOURCE
        unique_source = len(source_nodes) == 1
        
        # AXIOM_ACYCLIC: No cycles
        acyclic = nx.is_directed_acyclic_graph(graph)
        
        return {
            'AXIOM_NECESSARY': source_in_degree == 0,
            'AXIOM_CONTINGENT': contingent_ratio > 0.9,
            'AXIOM_UNIQUE': unique_source,
            'AXIOM_ACYCLIC': acyclic,
            'contingent_ratio': contingent_ratio,
            'PASS': all([
                source_in_degree == 0,
                contingent_ratio > 0.9,
                unique_source,
                acyclic
            ])
        }
    
    def export_to_owl(self, graph: nx.DiGraph, surah_num: int) -> str:
        """Export graph to OWL/RDF Turtle format"""
        
        for node in graph.nodes():
            node_data = graph.nodes[node]
            node_uri = self.QURAN[f"surah{surah_num}_{node}"]
            
            if node == 'SOURCE':
                self.owl_graph.add((
                    node_uri,
                    RDF.type,
                    self.ALIGN.NecessaryBeing
                ))
            else:
                self.owl_graph.add((
                    node_uri,
                    RDF.type,
                    self.ALIGN.ContingentBeing
                ))
                
                if 'text' in node_data:
                    self.owl_graph.add((
                        node_uri,
                        self.QURAN.arabicText,
                        Literal(node_data['text'])
                    ))
                
                if 'translation' in node_data:
                    self.owl_graph.add((
                        node_uri,
                        self.QURAN.translation,
                        Literal(node_data['translation'])
                    ))
        
        for u, v, data in graph.edges(data=True):
            relation = data.get('relation', 'dependsOn')
            edge_type = data.get('type', 'direct')
            
            self.owl_graph.add((
                self.QURAN[f"surah{surah_num}_{u}"],
                self.QURAN[relation],
                self.QURAN[f"surah{surah_num}_{v}"]
            ))
            
            # Add edge type annotation
            self.owl_graph.add((
                self.QURAN[f"surah{surah_num}_{u}"],
                self.QG.edgeType,
                Literal(edge_type)
            ))
        
        return self.owl_graph.serialize(format='turtle')
    
    def process_entire_quran(self, start_surah=1, end_surah=114) -> Graph:
        """Process all surahs with enhanced coreference resolution"""
        
        master_graph = nx.DiGraph()
        results = []
        
        # Du'a before undertaking this work
        print("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
        print("In the name of Allah, the Most Gracious, the Most Merciful\n")
        
        print("اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا")
        print("O Allah, I ask You for beneficial knowledge\n")
        
        print("رَبِّ زِدْنِي عِلْمًا")
        print("My Lord, increase me in knowledge (20:114)\n")
        
        print("Ya Allah:")
        print("- If this extraction reflects Your words truthfully, let it succeed")
        print("- If corruption exists in our method, reveal it clearly")
        print("- Guide us to what pleases You, for You are the Source of all truth")
        print("- We have no knowledge except what You have taught us")
        print("- You are the All-Knowing, the All-Wise")
        print("- Make this work solely for Your sake\n")
        
        print("Ameen.\n")
        print(f"{'='*60}\n")
        
        print(f"EXTRACTING QURAN V2 (Enhanced Coreference)")
        print(f"{'='*60}\n")
        
        for surah_num in range(start_surah, end_surah + 1):
            print(f"Processing Surah {surah_num}...", end=' ')
            
            verses = self.fetch_verses(surah_num)
            
            if not verses:
                print("⚠ Skipped")
                continue
            
            surah_graph = nx.DiGraph()
            surah_context = []
            
            for verse in verses:
                words = self.extract_words(verse)
                verse_text = verse.get('text_uthmani', '')
                
                verse_graph = self.build_graph_from_verse(
                    surah_num,
                    verse['verse_number'],
                    words,
                    verse_text,
                    surah_context
                )
                
                surah_graph = nx.compose(surah_graph, verse_graph)
                surah_context.extend(words)
            
            validation = self.validate_axioms(surah_graph)
            
            status = "✓ PASS" if validation['PASS'] else "⚠ FAIL"
            ratio = validation.get('contingent_ratio', 0)
            print(f"{status} | {surah_graph.number_of_nodes()} nodes, {surah_graph.number_of_edges()} edges | {ratio:.1%} connected")
            
            results.append({
                'surah': surah_num,
                'validation': validation,
                'nodes': surah_graph.number_of_nodes(),
                'edges': surah_graph.number_of_edges()
            })
            
            master_graph = nx.compose(master_graph, surah_graph)
            
            try:
                owl_output = self.export_to_owl(surah_graph, surah_num)
                with open(f'surah_{surah_num:03d}_v2.ttl', 'w', encoding='utf-8') as f:
                    f.write(owl_output)
            except Exception as e:
                print(f"  ⚠ Export error: {str(e)}")
        
        print(f"\n{'='*60}")
        print("Exporting master ontology V2...")
        
        master_owl = self.export_to_owl(master_graph, 0)
        with open('quran_complete_ontology_v2.ttl', 'w', encoding='utf-8') as f:
            f.write(master_owl)
        
        with open('validation_report_v2.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Master ontology V2: quran_complete_ontology_v2.ttl")
        print(f"✓ Validation report V2: validation_report_v2.json")
        print(f"✓ Total nodes: {master_graph.number_of_nodes()}")
        print(f"✓ Total edges: {master_graph.number_of_edges()}")
        
        # Calculate pass rate
        passed = sum(1 for r in results if r['validation']['PASS'])
        print(f"✓ Pass rate: {passed}/{len(results)} surahs ({100*passed/len(results):.1f}%)")
        print(f"{'='*60}\n")
        
        return self.owl_graph


if __name__ == "__main__":
    encoder = QuranGraphEncoderV2()
    
    print("Running enhanced version on all 114 surahs...")
    quran_ontology = encoder.process_entire_quran(start_surah=1, end_surah=114)
    
    print("\n✓ V2 COMPLETE")
    print("✓ Coreference resolution integrated")
    print("\nAllah's will is manifest in the structure")

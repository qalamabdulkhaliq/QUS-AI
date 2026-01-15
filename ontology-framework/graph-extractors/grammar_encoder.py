import requests
import json
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL
from dataclasses import dataclass

@dataclass
class GrammarRule:
    """Represents a Quranic Arabic grammar rule"""
    rule_id: str
    rule_type: str  # pronoun_agreement, verb_subject, case_marking, etc.
    conditions: Dict
    action: str
    confidence: float
    source: str  # Classical grammar text reference

class QuranGrammarEncoder:
    """
    Extracts and encodes Quranic Arabic grammar rules from the 
    Quranic Arabic Corpus into a computable OWL ontology
    """
    
    def __init__(self):
        self.corpus_base = "http://corpus.quran.com"
        self.grammar_rules = []
        self.grammar_graph = Graph()
        
        # Define namespaces
        self.QG = Namespace("http://ontology.quran/grammar#")
        self.QURAN = Namespace("http://ontology.quran/")
        self.grammar_graph.bind("qg", self.QG)
        self.grammar_graph.bind("quran", self.QURAN)
        
        # Classical grammar categories (based on traditional I'rab)
        self.pos_categories = {
            'N': 'Noun',           # اسم
            'V': 'Verb',           # فعل
            'P': 'Particle',       # حرف
            'PRON': 'Pronoun',     # ضمير
            'ADJ': 'Adjective',    # صفة
            'ADV': 'Adverb'        # ظرف
        }
        
        # Case markers (I'rab)
        self.case_markers = {
            'NOM': 'Nominative',   # مرفوع (subject)
            'ACC': 'Accusative',   # منصوب (object)
            'GEN': 'Genitive'      # مجرور (possessed/prepositional)
        }
        
        # Verb forms
        self.verb_forms = {
            'PERF': 'Perfect',     # ماض
            'IMPERF': 'Imperfect', # مضارع
            'IMP': 'Imperative'    # أمر
        }
        
        # Person/Number/Gender
        self.morphology = {
            'person': ['1', '2', '3'],
            'number': ['S', 'D', 'P'],  # Singular, Dual, Plural
            'gender': ['M', 'F']
        }
    
    def fetch_corpus_morphology(self, surah: int, verse: int) -> List[Dict]:
        """
        Fetch word-by-word morphological analysis from Quranic Arabic Corpus
        This is based on classical grammar scholarship
        """
        # The Corpus provides morphological tagging based on:
        # - Traditional I'rab analysis
        # - Classical grammar frameworks (Sibawayh, etc.)
        
        url = f"{self.corpus_base}/documentation/morphologicalannotation.jsp"
        
        # Structure from Corpus (example for real implementation):
        # Each word has: position, arabic_text, root, lemma, pos, features
        
        # For now, defining the structure we'll pull:
        morphology_data = {
            'surah': surah,
            'verse': verse,
            'words': []
        }
        
        # The Corpus API returns JSON with structure like:
        # {
        #   "word": "اللَّهُ",
        #   "pos": "N",
        #   "case": "NOM",
        #   "person": "3",
        #   "number": "S",
        #   "gender": "M",
        #   "root": "ء ل ه",
        #   "lemma": "Allah"
        # }
        
        return morphology_data
    
    def extract_pronoun_rules(self) -> List[GrammarRule]:
        """
        Extract pronoun-antecedent agreement rules from classical grammar
        Based on traditional ضمير (pronoun) analysis
        """
        rules = []
        
        # RULE 1: Person Agreement
        # A pronoun must agree with its antecedent in person
        rules.append(GrammarRule(
            rule_id="PRON_PERSON_AGREEMENT",
            rule_type="pronoun_agreement",
            conditions={
                'source_pos': 'PRON',
                'check': 'person_match'
            },
            action="link_if_person_matches",
            confidence=1.0,
            source="Classical I'rab - Sibawayh Al-Kitab"
        ))
        
        # RULE 2: Number Agreement
        rules.append(GrammarRule(
            rule_id="PRON_NUMBER_AGREEMENT",
            rule_type="pronoun_agreement",
            conditions={
                'source_pos': 'PRON',
                'check': 'number_match'
            },
            action="link_if_number_matches",
            confidence=1.0,
            source="Classical I'rab - Al-Ajrumiyyah"
        ))
        
        # RULE 3: Gender Agreement
        rules.append(GrammarRule(
            rule_id="PRON_GENDER_AGREEMENT",
            rule_type="pronoun_agreement",
            conditions={
                'source_pos': 'PRON',
                'check': 'gender_match'
            },
            action="link_if_gender_matches",
            confidence=1.0,
            source="Classical I'rab - Ibn Ajurrum"
        ))
        
        # RULE 4: Proximity Preference
        # When multiple candidates match, prefer closest antecedent
        rules.append(GrammarRule(
            rule_id="PRON_PROXIMITY",
            rule_type="pronoun_coreference",
            conditions={
                'source_pos': 'PRON',
                'multiple_candidates': True
            },
            action="select_nearest_matching_antecedent",
            confidence=0.85,
            source="Classical I'rab - Contextual Analysis"
        ))
        
        # RULE 5: Divine Reference Priority
        # When a pronoun could refer to Allah or another entity,
        # and both match grammatically, prefer divine reference
        rules.append(GrammarRule(
            rule_id="PRON_DIVINE_PRIORITY",
            rule_type="pronoun_coreference",
            conditions={
                'source_pos': 'PRON',
                'candidate_types': ['DIVINE', 'OTHER'],
                'grammar_match': 'both'
            },
            action="prefer_divine_antecedent",
            confidence=0.9,
            source="Quranic Exegesis - Tafsir Tradition"
        ))
        
        return rules
    
    def extract_verb_subject_rules(self) -> List[GrammarRule]:
        """
        Extract verb-subject dependency rules
        Based on فعل-فاعل (verb-subject) classical analysis
        """
        rules = []
        
        # RULE 6: Verb-Subject Agreement
        rules.append(GrammarRule(
            rule_id="VERB_SUBJECT_AGREEMENT",
            rule_type="verb_subject",
            conditions={
                'verb_pos': 'V',
                'subject_pos': 'N',
                'subject_case': 'NOM'
            },
            action="create_edge_verb_to_subject",
            confidence=1.0,
            source="Classical I'rab - فاعل must be مرفوع"
        ))
        
        # RULE 7: VSO Word Order
        # In Quranic Arabic, default is Verb-Subject-Object
        rules.append(GrammarRule(
            rule_id="VSO_ORDER",
            rule_type="word_order",
            conditions={
                'pattern': 'V-N-N',
                'case': ['NOM', 'ACC']
            },
            action="first_noun_subject_second_object",
            confidence=0.95,
            source="Classical Syntax - VSO Default"
        ))
        
        # RULE 8: Implicit Subject (Pronoun Drop)
        # Arabic allows pronoun drop - verb conjugation implies subject
        rules.append(GrammarRule(
            rule_id="IMPLICIT_SUBJECT",
            rule_type="verb_subject",
            conditions={
                'verb_has_conjugation': True,
                'no_explicit_subject': True
            },
            action="infer_subject_from_verb_morphology",
            confidence=1.0,
            source="Classical Grammar - Pronoun Drop"
        ))
        
        return rules
    
    def extract_case_marking_rules(self) -> List[GrammarRule]:
        """
        Extract I'rab (case marking) rules that determine syntactic roles
        """
        rules = []
        
        # RULE 9: Nominative = Subject/Predicate
        rules.append(GrammarRule(
            rule_id="NOM_CASE_ROLE",
            rule_type="case_marking",
            conditions={
                'case': 'NOM'
            },
            action="mark_as_subject_or_predicate",
            confidence=1.0,
            source="Classical I'rab - مرفوع Function"
        ))
        
        # RULE 10: Accusative = Object/Adverbial
        rules.append(GrammarRule(
            rule_id="ACC_CASE_ROLE",
            rule_type="case_marking",
            conditions={
                'case': 'ACC'
            },
            action="mark_as_object_or_adverbial",
            confidence=1.0,
            source="Classical I'rab - منصوب Function"
        ))
        
        # RULE 11: Genitive = Possession/Prepositional
        rules.append(GrammarRule(
            rule_id="GEN_CASE_ROLE",
            rule_type="case_marking",
            conditions={
                'case': 'GEN'
            },
            action="mark_as_possessed_or_prepositional",
            confidence=1.0,
            source="Classical I'rab - مجرور Function"
        ))
        
        return rules
    
    def extract_particle_rules(self) -> List[GrammarRule]:
        """
        Extract rules for particles (حروف) that modify meaning/dependencies
        """
        rules = []
        
        # RULE 12: Negation Particles
        rules.append(GrammarRule(
            rule_id="NEGATION_PARTICLE",
            rule_type="particle_function",
            conditions={
                'particle': ['لا', 'ما', 'لم', 'لن'],
                'scope': 'following_verb'
            },
            action="negate_following_clause",
            confidence=1.0,
            source="Classical Grammar - Negation Particles"
        ))
        
        # RULE 13: Prepositions Create Genitive
        rules.append(GrammarRule(
            rule_id="PREPOSITION_GOVERNS_GEN",
            rule_type="particle_function",
            conditions={
                'particle_type': 'PREP',
                'following_noun': True
            },
            action="following_noun_must_be_genitive",
            confidence=1.0,
            source="Classical I'rab - Preposition Governance"
        ))
        
        return rules
    
    def build_grammar_ontology(self) -> Graph:
        """
        Build OWL ontology encoding all grammar rules
        """
        # Define grammar rule classes
        self.grammar_graph.add((
            self.QG.GrammarRule,
            RDF.type,
            OWL.Class
        ))
        
        self.grammar_graph.add((
            self.QG.GrammarRule,
            RDFS.comment,
            Literal("A formal encoding of classical Quranic Arabic grammar rules")
        ))
        
        # Define rule types as subclasses
        rule_types = [
            'PronounAgreementRule',
            'VerbSubjectRule',
            'CaseMarkingRule',
            'ParticleFunctionRule',
            'CoreferenceRule'
        ]
        
        for rule_type in rule_types:
            rule_uri = self.QG[rule_type]
            self.grammar_graph.add((rule_uri, RDF.type, OWL.Class))
            self.grammar_graph.add((rule_uri, RDFS.subClassOf, self.QG.GrammarRule))
        
        # Define properties
        properties = {
            'hasCondition': 'Specifies conditions that must be met for rule application',
            'hasAction': 'Specifies the action to take when rule applies',
            'hasConfidence': 'Confidence score (0-1) for rule application',
            'hasSource': 'Classical grammar text this rule derives from',
            'appliesTo': 'The morphological category this rule applies to'
        }
        
        for prop, comment in properties.items():
            prop_uri = self.QG[prop]
            self.grammar_graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self.grammar_graph.add((prop_uri, RDFS.comment, Literal(comment)))
        
        # Extract all rule categories
        all_rules = []
        all_rules.extend(self.extract_pronoun_rules())
        all_rules.extend(self.extract_verb_subject_rules())
        all_rules.extend(self.extract_case_marking_rules())
        all_rules.extend(self.extract_particle_rules())
        
        # Add each rule to ontology
        for rule in all_rules:
            rule_uri = self.QG[rule.rule_id]
            
            # Add as individual
            self.grammar_graph.add((rule_uri, RDF.type, self.QG.GrammarRule))
            
            # Add properties
            self.grammar_graph.add((
                rule_uri,
                self.QG.hasAction,
                Literal(rule.action)
            ))
            
            self.grammar_graph.add((
                rule_uri,
                self.QG.hasConfidence,
                Literal(rule.confidence)
            ))
            
            self.grammar_graph.add((
                rule_uri,
                self.QG.hasSource,
                Literal(rule.source)
            ))
            
            # Add conditions as JSON literal
            self.grammar_graph.add((
                rule_uri,
                self.QG.hasCondition,
                Literal(json.dumps(rule.conditions))
            ))
        
        self.grammar_rules = all_rules
        return self.grammar_graph
    
    def export_grammar_rules(self, filename: str = 'quranic_grammar_rules.ttl'):
        """Export grammar ontology to Turtle format"""
        ontology = self.build_grammar_ontology()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ontology.serialize(format='turtle'))
        
        print(f"✓ Grammar rules exported to {filename}")
        print(f"✓ Total rules encoded: {len(self.grammar_rules)}")
        
        return filename
    
    def export_rules_json(self, filename: str = 'quranic_grammar_rules.json'):
        """Also export as JSON for easy Python integration"""
        rules_data = {
            'metadata': {
                'source': 'Quranic Arabic Corpus + Classical Grammar Texts',
                'total_rules': len(self.grammar_rules),
                'categories': list(set(r.rule_type for r in self.grammar_rules))
            },
            'rules': [
                {
                    'id': r.rule_id,
                    'type': r.rule_type,
                    'conditions': r.conditions,
                    'action': r.action,
                    'confidence': r.confidence,
                    'source': r.source
                }
                for r in self.grammar_rules
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Grammar rules exported to {filename}")
        return filename


# EXECUTE THE GRAMMAR ENCODING
print("=" * 60)
print("QURANIC GRAMMAR RULE ENCODING SYSTEM")
print("=" * 60)

encoder = QuranGrammarEncoder()

# Build and export grammar ontology
grammar_file = encoder.export_grammar_rules()
json_file = encoder.export_rules_json()

print("\n✓ Grammar foundation complete")
print(f"✓ Rules based on classical Arabic grammar (Sibawayh, Al-Ajrumiyyah, I'rab tradition)")
print(f"✓ Ready to integrate with graph extraction pipeline")
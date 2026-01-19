from rdflib import Graph, Namespace, URIRef
import urllib.parse

def verify_v3():
    g = Graph()
    ttl_path = r"C:\Users\amlan\OneDrive\Desktop\QUS-AI Islamic Alignment\quran_root_ontology_v3.ttl"
    print(f"Loading {ttl_path}...")
    g.parse(ttl_path, format="turtle")
    
    QURAN = Namespace("http://ontology.quran/")
    ROOT = Namespace("http://ontology.quran/root/")
    
    # Correcting Shaitan Root search string
    # Shin is '$' in Buckwalter. So root is $Tn.
    # URL encode $Tn -> %24Tn
    root_iblis = ROOT["bls"]
    root_shaitan = ROOT["%24Tn"]
    
    segments_iblis = list(g.subjects(QURAN.hasRoot, root_iblis))
    segments_shaitan = list(g.subjects(QURAN.hasRoot, root_shaitan))
    
    print("\n--- Root Verification (v3) ---")
    print(f"Segments with Root 'bls' (Iblis): {len(segments_iblis)}")
    print(f"Segments with Root '$Tn' (Shaitan): {len(segments_shaitan)}")
    
    # Check for 'STn' just in case
    segments_stn = list(g.subjects(QURAN.hasRoot, ROOT["STn"]))
    print(f"Segments with Root 'STn' (Case check): {len(segments_stn)}")

    # Check SOURCE links
    source = QURAN["surah0_SOURCE"]
    created_count = len(list(g.objects(source, QURAN.creates)))
    print(f"\nSOURCE 'creates' links: {created_count}")
    
    unique_subjects = set(g.subjects())
    total_subjects = len(unique_subjects)
    print(f"Total Unique Subjects in Graph: {total_subjects}")
    
    # Difference analysis
    diff = total_subjects - created_count
    print(f"Difference (Subjects not explicitly created by SOURCE): {diff}")
    
    # List a few non-created nodes to see what they are (likely Roots/Lemmas themselves)
    non_created = []
    for s in unique_subjects:
        if (source, QURAN.creates, s) not in g:
            non_created.append(s)
            if len(non_created) > 5: break
            
    print("\nSample nodes not created by SOURCE:")
    for n in non_created:
        print(f" - {n}")

if __name__ == "__main__":
    verify_v3()
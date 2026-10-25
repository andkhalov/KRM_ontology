#!/usr/bin/env python3
"""Check the KRM ontology with the HermiT OWL 2 DL reasoner (owlready2 + Java).

The script merges the 11 modules, drops owl:imports (the merged graph is already complete),
declares the external PROV-O terms it uses, loads the result into owlready2 and runs HermiT:

1. consistency: no unsatisfiable classes (nothing is inferred to be owl:Nothing);
2. classification on a two-variant mini A-Box: the defined class krm:ValidatedArtefact must be
   inferred for the variant with a passed validation (V001) and not for the failed one (V002).

Run:  python check_hermit.py      (requires Java in PATH and the owlready2 package)
"""
import os
import sys
import tempfile

import owlready2
import rdflib
from rdflib.namespace import OWL, RDF

HERE = os.path.dirname(os.path.abspath(__file__))
KRM = "http://example.org/krm#"
KID = "http://example.org/krm/id/"
PROV = "http://www.w3.org/ns/prov#"
MODULES = ["krm-core.ttl", "actors.ttl", "kim.ttl", "planning.ttl", "assessment.ttl",
           "process.ttl", "inferences.ttl", "definitions.ttl", "extensions.ttl",
           "campaign.ttl", "datasets.ttl"]


def merged_graph(with_abox=True):
    g = rdflib.Graph()
    for m in MODULES:
        g.parse(os.path.join(HERE, m), format="turtle")
    g.remove((None, OWL.imports, None))  # everything is merged; imports are not needed (and work offline)
    for c in ("Entity", "Activity", "Agent", "SoftwareAgent"):
        g.add((rdflib.URIRef(PROV + c), RDF.type, OWL.Class))
    for p in ("wasGeneratedBy", "used", "wasAssociatedWith"):
        g.add((rdflib.URIRef(PROV + p), RDF.type, OWL.ObjectProperty))
    g.add((rdflib.URIRef(PROV + "endedAtTime"), RDF.type, OWL.DatatypeProperty))
    if with_abox:
        K, ID = rdflib.Namespace(KRM), rdflib.Namespace(KID)
        g.add((ID.V001, RDF.type, K.TaskVariant))
        g.add((ID.val1, RDF.type, K.Validation))
        g.add((ID.val1, K.validationOf, ID.V001))
        g.add((ID.val1, K.passed, rdflib.Literal(True)))
        g.add((ID.V002, RDF.type, K.TaskVariant))
        g.add((ID.val2, RDF.type, K.Validation))
        g.add((ID.val2, K.validationOf, ID.V002))
        g.add((ID.val2, K.passed, rdflib.Literal(False)))
    return g


def main():
    g = merged_graph(with_abox=True)
    with tempfile.NamedTemporaryFile(suffix=".owl", delete=False) as tmp:
        path = tmp.name
    g.serialize(path, format="xml")
    world = owlready2.World()
    onto = world.get_ontology("file://" + os.path.abspath(path)).load()
    ok = True
    try:
        with onto:
            owlready2.sync_reasoner_hermit(world, infer_property_values=True, debug=0)
    except owlready2.OwlReadyInconsistentOntologyError as e:
        print("HermiT: the ontology is INCONSISTENT:", str(e)[:400])
        sys.exit(2)
    finally:
        os.unlink(path)
    unsat = list(world.inconsistent_classes())
    print("HermiT consistency:", "OK" if not unsat else f"unsatisfiable classes {[c.iri for c in unsat]}")
    ok &= not unsat

    va = onto.search_one(iri=KRM + "ValidatedArtefact")
    inst = sorted(i.name for i in va.instances()) if va else []
    print("ValidatedArtefact inferred for V001 (passed) and not for V002 (failed):", inst,
          "OK" if inst == ["V001"] else "FAILED")
    ok &= inst == ["V001"]
    print("\nResult:", "all checks passed" if ok else "problems found")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()

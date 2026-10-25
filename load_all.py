#!/usr/bin/env python3
"""Load the whole KRM ontology into one rdflib graph and, optionally, validate it with SHACL.

rdflib does not follow owl:imports, so the modules are parsed explicitly here. Protégé and the
OWL API resolve the imports of krm_ontology.ttl through catalog-v001.xml instead.

Usage:
    python load_all.py             # load the 11 modules and the examples, print triple counts
    python load_all.py --shapes    # also validate schema + examples against shapes/*.ttl (pyshacl)

With --shapes the script prints the validation results grouped by severity and shape and exits
with code 1 if there is at least one sh:Violation. Warnings are readiness signals: an incomplete
assessment campaign (such as the examples) is expected to produce them.
"""
import collections
import glob
import os
import sys

import rdflib
from rdflib.namespace import RDF, SH

HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = ["krm-core.ttl", "actors.ttl", "kim.ttl", "planning.ttl",
           "assessment.ttl", "process.ttl", "inferences.ttl", "definitions.ttl",
           "extensions.ttl", "campaign.ttl", "datasets.ttl"]  # import order
EXAMPLES = sorted(glob.glob(os.path.join(HERE, "examples", "*.ttl")))
SHAPES = sorted(glob.glob(os.path.join(HERE, "shapes", "*.ttl")))


def load(with_examples=True):
    g = rdflib.Graph()
    for m in MODULES:
        g.parse(os.path.join(HERE, m), format="turtle")
    if with_examples:
        for e in EXAMPLES:
            g.parse(e, format="turtle")
    return g


def validate(g):
    import pyshacl

    shapes = rdflib.Graph()
    for s in SHAPES:
        shapes.parse(s, format="turtle")
    _, results, _ = pyshacl.validate(g, shacl_graph=shapes, inference="none")
    by_severity, by_shape = collections.Counter(), collections.Counter()
    for r in results.subjects(RDF.type, SH.ValidationResult):
        severity = str(results.value(r, SH.resultSeverity)).split("#")[-1]
        shape = results.value(r, SH.sourceShape)
        name = str(shape).split("#")[-1] if isinstance(shape, rdflib.URIRef) else "(anonymous property shape)"
        by_severity[severity] += 1
        by_shape[(severity, name)] += 1
    return by_severity, by_shape


if __name__ == "__main__":
    schema = load(with_examples=False)
    g = load()
    print(f"Modules: {len(MODULES)}, examples: {len(EXAMPLES)}; "
          f"triples: {len(schema)} (schema), {len(g)} (schema + examples)")
    if "--shapes" in sys.argv:
        by_severity, by_shape = validate(g)
        summary = ", ".join(f"{k}: {v}" for k, v in sorted(by_severity.items())) or "no results"
        print(f"SHACL, {len(SHAPES)} shape files: {summary}")
        for (severity, name), n in sorted(by_shape.items()):
            print(f"  {severity:9s} {n:3d}  {name}")
        sys.exit(1 if by_severity.get("Violation") else 0)

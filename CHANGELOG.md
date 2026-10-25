# Changelog

All notable changes to the KRM Ontology are documented in this file. Versions follow
[Semantic Versioning](https://semver.org/): a major version changes when IRIs or the meaning of existing terms
change.

## KRM Ontology v1.0.0 — 2026-10-26

First public release of the **KRM Ontology** — an OWL 2 ontology of the competency-role model (KRM) for artificial
intelligence specialists and of the competency-assessment cycle built on it.

### What it is

- **11 modules** behind one entry point, `krm_ontology.ttl`: core (KRM tree down to the competence-indicator-level
  unit, CIL), actors, kim (assessment materials), planning, assessment, process (provenance on PROV-O), inferences
  (OWL 2 RL property chains and inverses), definitions (OWL 2 DL defined classes and closed enumerations),
  extensions, campaign, datasets.
- **81 classes, 127 object properties, 87 datatype properties, 22 SKOS concept schemes**; all terms of the `krm:`
  namespace have Russian and English labels.
- **6 SHACL files with 39 node shapes**: tasks and task variants, completeness of the generation cascade, readiness
  gates of test variants, consistency and feasibility of an assessment, program profiles, expert profiles, datasets.
- **3 example A-Boxes** (KRM fragment; actors and assessment materials; an assessment campaign end to end).
- **Validation scripts**: `load_all.py` (rdflib + pyshacl) and `check_hermit.py` (HermiT through owlready2), run in
  GitHub Actions on every push.

### Validation of this release

- Turtle: 2,793 schema triples; 3,114 together with the examples.
- SHACL on schema + examples: 0 violations, 13 warnings (readiness gates of the deliberately minimal examples).
- HermiT: consistent; `krm:ValidatedArtefact` is inferred only for a variant with a passed validation.

### Main modelling decisions

- The task type is one value of a closed list of four (single choice, multiple choice, open text answer, code); the
  answer form and the checking contour are derived by defined classes, not stored.
- Readiness of a task variant is the derived class `krm:ReadyVariant` (passed validation and expert acceptance)
  instead of a stored flag.
- Ancestors in the KRM tree and in the generation cascade are reached through the transitive properties
  `krm:broaderTransitive` and `krm:derivedFrom` rather than through separate shortcut chains.
- Task content (statements, options, code, test data) stays outside the graph and is referenced by
  `krm:contentRef`.

### Fixed before the release

- `krm:RationaleShape`: the severity is now declared on the node shape, so a written task without an answer rationale
  is reported as a warning (a readiness signal), as intended, and not as a violation.

## Citation

```bibtex
@misc{krm_ontology_2026,
  author    = {Khalov, Andrey P. and Kustov, Denis V. and Ataeva, Olga M. and Tuchkova, Natalia P.},
  title     = {{KRM Ontology}: An {OWL} 2 Ontology of the Competency-Role Model and Competency Assessment for {AI} Specialists},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {(DOI minted by Zenodo on release)},
  url       = {https://github.com/andkhalov/KRM_ontology}
}
```

## Authors

- **Andrey P. Khalov** — Moscow Institute of Physics and Technology (MIPT), Dolgoprudny, Russia; Federal Research
  Center "Computer Science and Control" of the Russian Academy of Sciences, Moscow, Russia ·
  ORCID [0009-0005-4584-8245](https://orcid.org/0009-0005-4584-8245) · `khalov.a@phystech.edu`
- **Denis V. Kustov** — MIPT · ORCID [0000-0002-8389-6388](https://orcid.org/0000-0002-8389-6388) · `kustov.dv@ya.ru`
- **Olga M. Ataeva** — FRC CSC RAS · ORCID [0000-0003-0367-5575](https://orcid.org/0000-0003-0367-5575) ·
  `oataeva@frccsc.ru`
- **Natalia P. Tuchkova** — FRC CSC RAS · ORCID [0000-0001-5357-9640](https://orcid.org/0000-0001-5357-9640) ·
  `ntuchkova@frccsc.ru`

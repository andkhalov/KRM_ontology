# KRM Ontology

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![validate](https://github.com/andkhalov/KRM_ontology/actions/workflows/validate.yml/badge.svg)](https://github.com/andkhalov/KRM_ontology/actions/workflows/validate.yml)
<!-- DOI badge: added after the first Zenodo release -->

An OWL 2 ontology of the **competency-role model (KRM)** for artificial intelligence specialists and of the
competency-assessment process built on it: from the competency tree down to the individual test variant of a
student. SHACL shapes that come with the ontology express data constraints and readiness gates.

| | |
|---|---|
| Version | 1.0.0 (2026-10-26) |
| Format | Turtle; entry point `krm_ontology.ttl` imports 11 modules |
| Reasoning | core modules and `inferences.ttl` use OWL 2 RL constructs; `definitions.ttl` adds OWL 2 DL defined classes |
| Size | 81 classes, 127 object properties, 87 datatype properties, 22 SKOS concept schemes; 2,793 triples |
| Constraints | 6 SHACL files, 39 node shapes |
| Languages | all classes, properties and enumeration members of the `krm:` namespace have labels in Russian and English |
| License | [MIT](LICENSE) |

## Contents

- [What is modelled](#what-is-modelled)
- [Modules](#modules)
- [Design decisions](#design-decisions)
- [Getting started](#getting-started)
- [Validation](#validation)
- [Namespaces and identifiers](#namespaces-and-identifiers)
- [Examples](#examples)
- [Repository layout](#repository-layout)
- [How to cite](#how-to-cite)
- [License](#license)
- [Authors](#authors)

## What is modelled

The KRM describes the professional competencies of AI specialists by roles. Its atomic unit of assessment is the
**CIL** (competence–indicator–level unit; *КИУ* in Russian): a competence indicator at one mastery level — basic,
intermediate or advanced (B, S, P). Universities choose CILs for their educational programs and declare, for each of
them, the tools of professional activity (programming languages, libraries, environments) and the subjects of
knowledge (subject areas, data types, task classes) that their students work with. Tasks are written for the chosen
CILs, adapted to the declared tools and subjects, and assembled into a unique test variant for every student.

The ontology covers this whole chain:

- **the KRM itself** — competence types (domains), blocks, directions, competences, indicators, mastery levels and
  CILs; professional roles and role requirements; topics, information sources, case examples, labor functions;
- **actors** — universities, fields of study, educational programs, disciplines, students, experts and expert
  profiles; the program testing profile (chosen CILs with declared tools and subjects of knowledge);
- **assessment materials** — general and specific descriptors, tasks of four types, task variants, test cases,
  reference solutions, rubrics and answer rationales;
- **planning** — CIL demand, test variants, generation work items and their statuses;
- **assessment** — attempts, answers, node scores and their recomposition up the KRM tree, achievement thresholds,
  individual profiles, appeals, federal indicators;
- **process and provenance** (on top of PROV-O) — generation activities, system agents, validations, expert
  acceptance, KRM versions and assessment cycles;
- **the assessment campaign** — the assessment as a whole, its test-variant assembly policy with task-type quotas,
  campaign statuses and time window;
- **datasets** used as study objects in tasks — datasets, features and perspectives.

The repository contains the schema (T-Box) and the shapes. The content of the KRM (its competences and CILs) and
campaign data are not part of this release; three small example A-Boxes show how the modules fit together. The
schema is aligned with KRM version 2.0 (December 2025).

The central structure is the generation cascade:

```text
CIL ─▶ general descriptor (1:1) ─▶ specific descriptors (1–3) ─▶ task (one per descriptor and task type)
    ─▶ task variants (adapted to a program's tools and subjects) ─▶ test variant (one per student)
```

The four upward edges `krm:fromKIU`, `krm:specializes`, `krm:forDescriptor` and `krm:ofTemplate` are
sub-properties of the transitive `krm:derivedFrom` (inverse `krm:derives`), so every artefact reaches its CIL by one
property. A test variant lists its task variants with `krm:includesVariant`.

## Modules

| Module | File | Scope |
|---|---|---|
| core | `krm-core.ttl` | KRM tree from competence types to CILs; roles and role requirements; topics, sources, case examples, labor functions |
| actors | `actors.ttl` | universities, fields of study, educational programs, disciplines, students, experts; program testing profiles with tool and subject declarations |
| kim | `kim.ttl` | assessment materials: general and specific descriptors, tasks and task types, task variants, test cases, reference solutions, rubrics, programming languages and libraries |
| planning | `planning.ttl` | CIL demand, test variants, generation work items |
| assessment | `assessment.ttl` | attempts, answers, node scores and recomposition, thresholds, individual profiles, appeals, federal indicators |
| process | `process.ttl` | provenance on PROV-O: generated artefacts, generation activities, system agents, validations, expert acceptance, KRM versions, cycles |
| inferences | `inferences.ttl` | inverse properties and property chains (student × CIL matrix, test-variant coverage and others) |
| definitions | `definitions.ttl` | closed enumerations and defined classes (open/closed task, automatically/expert-checked task, executable task, variant ready for sitting, neutral/context-bound descriptor and others) |
| extensions | `extensions.ttl` | level outcomes (know / can do), abbreviations, industries |
| campaign | `campaign.ttl` | the assessment as a whole: assembly policy, task-type quotas, statuses, time window |
| datasets | `datasets.ttl` | datasets as study objects, their features and perspectives |

Module IRIs are `http://example.org/krm` for the core and `http://example.org/krm/<module>` for the others; the
umbrella ontology is `http://example.org/krm/ontology`.

## Design decisions

1. **Keyed identifiers.** A code is the canonical key of an entity. Published entities do not change within a KRM
   version: an edit produces a new IRI and a new version.
2. **Four task types.** The task type is one value of a closed list (`krm:taskType`: single choice, multiple choice,
   open text answer, code). The answer form (open or closed) and the checking contour (automatic or expert) are not
   stored: defined classes in `definitions.ttl` derive them from the type.
3. **Structure in the graph, content outside it.** The graph holds structure and metadata: type, difficulty, time,
   language, links, limits, weights, number of tests, provenance, acceptance. The text of a task — statement,
   answer options, images, reference code, test data, rubric texts — is stored outside the graph and referenced by
   `krm:contentRef`. Formulations of the KRM and of descriptors stay in the graph as the context for writing tasks.
4. **Two levels of descriptors.** A general descriptor corresponds one-to-one to a CIL; one to three specific
   descriptors refine it; tasks are attached to specific descriptors.
5. **Layered reasoning.** The core modules and `inferences.ttl` stay within OWL 2 RL (inverse properties, property
   chains, transitive properties), so a rule-based triplestore can materialize them. `definitions.ttl` adds the OWL 2
   DL layer — defined classes and closed enumerations — for a DL reasoner such as HermiT or Pellet; where no DL
   reasoner is available, these definitions can be materialized with SPARQL rules.
6. **Derived readiness.** Whether a task variant is ready for sitting is not a stored flag: `krm:ReadyVariant`
   follows from a passed validation and an expert acceptance.
7. **Constraints in SHACL.** Cardinalities, conditional requirements (a code task needs a language, at least one test
   case and a reference solution), completeness of the cascade, consistency and feasibility conditions of an
   assessment, dataset limits. Readiness gates have severity `sh:Warning`: an assessment that is still being filled is
   expected to produce them.
8. **Enumerations as SKOS.** Statuses, levels, task types and other fixed lists are SKOS concept schemes with
   bilingual labels; the Russian `skos:prefLabel` is the primary one.
9. **Datasets are described once** — metadata and a reference to the stored artefact, not the data itself — and are
   reused by many tasks through perspectives (`krm:DatasetPerspective`).

## Getting started

### Protégé

Open `krm_ontology.ttl`. The OASIS catalog `catalog-v001.xml` in the same folder maps every module IRI to its local
file, so `owl:imports` resolve offline. Start HermiT to classify the defined classes.

### Python

```bash
git clone https://github.com/andkhalov/KRM_ontology.git
cd KRM_ontology
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

python load_all.py              # parse the 11 modules and the examples
python load_all.py --shapes     # validate schema + examples with the SHACL shapes
```

rdflib does not follow `owl:imports`, so `load_all.py` parses the modules explicitly; `load_all.load()` returns the
merged graph for your own code.

### SPARQL

List the task types:

```sparql
PREFIX krm:  <http://example.org/krm#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?type ?label WHERE {
  ?type skos:inScheme krm:taskTypes ; skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
}
```

Walk the cascade from a task variant to its CIL without a reasoner:

```sparql
PREFIX krm: <http://example.org/krm#>

SELECT ?variant ?cil WHERE {
  ?variant a krm:TaskVariant ;
           krm:ofTemplate/krm:forDescriptor/krm:specializes/krm:fromKIU ?cil .
}
```

With RDFS and OWL 2 RL reasoning the same question is simply `?variant krm:derivedFrom ?cil . ?cil a krm:KIU`.

## Validation

| Check | Command | Result for this release |
|---|---|---|
| Turtle syntax of all files | `python load_all.py` | 2,793 schema triples, 3,114 with the examples |
| SHACL on schema + examples | `python load_all.py --shapes` | 0 violations, 13 warnings |
| OWL 2 DL consistency and classification | `python check_hermit.py` | consistent; `krm:ValidatedArtefact` is inferred for a variant with a passed validation only |

The examples are deliberately minimal, so readiness gates report warnings: task-type quotas, time budget and prior
level of the test variant, demand coverage, answer rationale, and the number of tasks and task variants per
descriptor. `load_all.py --shapes` exits with code 1 only if
there is a violation. `check_hermit.py` needs Java and `pip install owlready2`; it merges the modules, declares the
PROV-O terms it uses and runs HermiT through owlready2. Both checks run in GitHub Actions on every push
(`.github/workflows/validate.yml`). Tested with Python 3.11, rdflib 7.6, pyshacl 0.40, owlready2 0.51 and Java 17.

The shape files:

| File | What it checks |
|---|---|
| `shapes/task-shapes.ttl` | tasks, task variants and test cases: required fields, type-specific requirements (code, open text), language mode, authoring, answer rationale |
| `shapes/cascade-shapes.ttl` | completeness of the cascade (descriptors per CIL, tasks and variants per descriptor) and readiness gates of test variants (coverage, uniqueness, quotas, time budget, practice share, prior level) |
| `shapes/consistency-shapes.ttl` | necessary conditions for an assessment to be consistent and feasible: coverage and time budget per student, demand covered by the plan, assembly-policy quotas |
| `shapes/program-shapes.ttl` | students, their programs and testing profiles; test variants use only the tools and languages declared for the program |
| `shapes/expert-shapes.ttl` | expert profiles |
| `shapes/dataset-shapes.ttl` | dataset metadata, perspectives and size limits |

The shapes are not imported by the umbrella ontology: they are a separate validation layer.

## Namespaces and identifiers

| Prefix | Namespace | Used for |
|---|---|---|
| `krm:` | `http://example.org/krm#` | classes, properties, enumeration members |
| `kid:` | `http://example.org/krm/id/` | instances |

IRIs under `example.org` are not dereferenceable. Entities carry their codes in `krm:code`, and instance IRIs are
derived from the codes: the CIL `MF-1_MF-1.1_Б` becomes `kid:KIU_MF-1_MF-1.1_B` (the Cyrillic level letters Б, С, П
are written as B, S, P). Codes of derived artefacts extend the code of the CIL: general descriptor `…_G`, specific
descriptor `…_D01`, task `…_D01_Z01`, task variant `…_D01_Z01_V001`. Task content is addressed by references such as
`content://task/<code>`.

## Examples

| File | What it shows |
|---|---|
| `examples/krm-core-example.ttl` | a fragment of the KRM tree (block, direction, competence, indicator, CIL) with a topic, source, case example, role, role requirement and labor function |
| `examples/actors-kim-example.ttl` | a fictitious university and program with a testing profile, a student, an expert, general and specific descriptors, a code task with a test case and a reference solution, a task variant with expert acceptance, a test variant |
| `examples/scenario-example.ttl` | an assessment campaign end to end: cycle and KRM version, assessment, assembly policy with quotas, demand and work item, dataset with features and a perspective, generation activity and validation, attempt, answer, scores, threshold, individual profile, appeal, federal indicator |

The examples build on each other and are loaded together by `load_all.py`.

## Repository layout

```text
krm_ontology.ttl        umbrella ontology (entry point), imports the 11 modules
krm-core.ttl … datasets.ttl   the modules
catalog-v001.xml        OASIS catalog for offline resolution of owl:imports
shapes/                 SHACL shapes (not imported by the umbrella)
examples/               example A-Boxes
load_all.py             loads the modules with rdflib and runs SHACL validation
check_hermit.py         consistency and classification check with HermiT
requirements.txt        Python dependencies of the scripts
CITATION.cff, .zenodo.json   citation metadata
CHANGELOG.md            release notes
```

Comments inside the Turtle files are written in Russian; labels and definitions are in Russian and English.

## How to cite

If you use the ontology, please cite it. Citation metadata is in [`CITATION.cff`](CITATION.cff) (GitHub shows it under
*Cite this repository*) and in `.zenodo.json`; each release is archived on Zenodo with a DOI.

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

## License

Released under the [MIT License](LICENSE).

## Authors

- **Andrey P. Khalov** — Moscow Institute of Physics and Technology (MIPT), Dolgoprudny, Russia; Federal Research
  Center "Computer Science and Control" of the Russian Academy of Sciences, Moscow, Russia ·
  ORCID [0009-0005-4584-8245](https://orcid.org/0009-0005-4584-8245) · `khalov.a@phystech.edu`
- **Denis V. Kustov** — Moscow Institute of Physics and Technology (MIPT), Dolgoprudny, Russia ·
  ORCID [0000-0002-8389-6388](https://orcid.org/0000-0002-8389-6388) · `kustov.dv@ya.ru`
- **Olga M. Ataeva** — Federal Research Center "Computer Science and Control" of the Russian Academy of Sciences ·
  ORCID [0000-0003-0367-5575](https://orcid.org/0000-0003-0367-5575) · `oataeva@frccsc.ru`
- **Natalia P. Tuchkova** — Federal Research Center "Computer Science and Control" of the Russian Academy of
  Sciences · ORCID [0000-0001-5357-9640](https://orcid.org/0000-0001-5357-9640) · `ntuchkova@frccsc.ru`

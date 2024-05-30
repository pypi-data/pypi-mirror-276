import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, Annotation

from pyprocessors_reconciliation.reconciliation import (
    ReconciliationProcessor,
    ReconciliationParameters,
    group_annotations,
)


def test_model():
    model = ReconciliationProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == ReconciliationParameters


def by_lexicon(a: Annotation):
    if a.terms:
        return a.terms[0].lexicon
    else:
        return ""


def by_label(a: Annotation):
    return a.labelName or a.label


def by_linking(a: Annotation):
    if a.terms:
        links = sorted({t.lexicon.split("_")[0] for t in a.terms})
        return "+".join(links)
    else:
        return "candidate"


def test_reconciliation_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = ReconciliationProcessor()
    parameters = ReconciliationParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso.annotations, by_linking)
    assert len(conso_groups["candidate"]) == 3
    assert len(conso_groups["wikidata"]) == 4


def test_x_cago():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/x_cago_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = ReconciliationProcessor()
        parameters = ReconciliationParameters()
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        # consolidated_groups_label = group_annotations(consolidated.annotations, by_label)
        result = Path(testdir, "data/x_cago_ner_en-document_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)

import importlib


def test_pdf_composer_importable():
    module = importlib.import_module("insight.pdf_composer")
    assert hasattr(module, "__file__")

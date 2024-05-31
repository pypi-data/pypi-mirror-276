#!/usr/bin/env python

"""Tests for `datonius` package."""


import unittest

from datonius import datonius
from datonius import cli
from datonius import util
from datonius import ontology


class TestBasic(unittest.TestCase):
    """Tests for `datonius` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.ctx = datonius.make_connection(":memory:")
        self.db = self.ctx.__enter__()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.ctx.__exit__(None, None, None)


    def test_add_an_isolate(self):
        self.assertEqual(datonius.Sample.create(oradss_id=1).id, 1)


class TestCli(unittest.TestCase):
    "Test CLI"

    def testLookup(self):
        "Test lookup subcommand"

    def testTax(self):
        "Test tax subcommand"

    def testOntology(self):
        "Test ontology subcommand"

class TestUtil(TestBasic):

    def testIsolateToDict(self):
        "Test isolate_to_dict function"

    def testSampleToDict(self):
        "Test sample_to_dict function"

    def testLookup(self):
        "Test lookup function"

    def testTax(self):
        "Test tax function"

    def testOntology(self):
        "Test ontology function"

class TestOntology(unittest.TestCase):

    def setUp(self):
        self.ctx = ontology.load_ontology()
        self.onto, self.struc = self.ctx.__enter__()

    def tearDown(self):
        self.ctx.__exit__(None, None, None)

    def test_search_one(self):
        self.assertEqual(self.onto.search_one(iri="*03530088")._name, "FOODON_03530088")

    def test_from_name_to_subnames(self):
        assert False

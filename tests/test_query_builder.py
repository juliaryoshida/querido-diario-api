import unittest
from datetime import date, datetime
from unittest.mock import patch
from gazettes import GazetteQueryBuilder

class GazetteQueryBuilderTest(unittest.TestCase):

    def setUp(self):
        self.query_builder = GazetteQueryBuilder(
            text_content_field="source_text",
            text_content_exact_field_suffix=".exact",
            publication_date_field="date",
            scraped_at_field="scraped_at",
            territory_id_field="territory_id",
        )

    # Caso 1: Territory
    def test_build_query_with_territory_ids(self):
        query = self.query_builder.build_query(
            territory_ids=["1234"],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring="",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["terms"]["territory_id"], ["1234"])

    # Caso 2: Published since
    def test_build_query_with_published_since(self):
        published_since = date.today()
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=published_since,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring="",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["range"]["date"]["gte"], published_since.isoformat())

    # Caso 3: Published until
    def test_build_query_with_published_until(self):
        published_until = date.today()
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=published_until,
            scraped_since=None,
            scraped_until=None,
            querystring="",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["range"]["date"]["lte"], published_until.isoformat())

    # Caso 4: Scraped since
    def test_build_query_with_scraped_since(self):
        scraped_since = datetime.now()
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=scraped_since,
            scraped_until=None,
            querystring="",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["range"]["scraped_at"]["gte"], scraped_since.isoformat())

    # Caso 5: Scraped until
    def test_build_query_with_scraped_until(self):
        scraped_until = datetime.now()
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=scraped_until,
            querystring="",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["range"]["scraped_at"]["lte"], scraped_until.isoformat())

    # Caso 6: Querystring
    def test_build_query_with_querystring(self):
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring="keyword",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["must"][0]["simple_query_string"]["query"], "keyword")

    # Caso 7: All true
    def test_build_query_with_all_filters(self):
        published_since = date.today()
        published_until = date.today()
        scraped_since = datetime.now()
        scraped_until = datetime.now()
        query = self.query_builder.build_query(
            territory_ids=["1234"],
            published_since=published_since,
            published_until=published_until,
            scraped_since=scraped_since,
            scraped_until=scraped_until,
            querystring="keyword",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="relevance",
        )
        self.assertEqual(query["query"]["bool"]["filter"][0]["terms"]["territory_id"], ["1234"])
        self.assertEqual(query["query"]["bool"]["filter"][1]["range"]["date"]["gte"], published_since.isoformat())
        self.assertEqual(query["query"]["bool"]["filter"][1]["range"]["date"]["lte"], published_until.isoformat())
        self.assertEqual(query["query"]["bool"]["filter"][2]["range"]["scraped_at"]["gte"], scraped_since.isoformat())
        self.assertEqual(query["query"]["bool"]["filter"][2]["range"]["scraped_at"]["lte"], scraped_until.isoformat())
        self.assertEqual(query["query"]["bool"]["must"][0]["simple_query_string"]["query"], "keyword")

    # Caso 8: Sort by false, query string false
    def test_build_query_with_sort_by_and_querystring(self):
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring="keyword",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="ascending_date",
        )
        self.assertEqual(query["sort"][0]["date"]["order"], "asc")
        self.assertEqual(query["query"]["bool"]["must"][0]["simple_query_string"]["query"], "keyword")

    # Caso 9: Query string true
    def test_build_query_with_sort_by_and_no_querystring(self):
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring=None,
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="ascending_date",
        )
        self.assertEqual(query["sort"][0]["date"]["order"], "asc")
        self.assertNotIn("must", query["query"]["bool"])

    # Caso 10: Sort by true
    def test_build_query_with_sort_by_and_querystring_descending(self):
        query = self.query_builder.build_query(
            territory_ids=[],
            published_since=None,
            published_until=None,
            scraped_since=None,
            scraped_until=None,
            querystring="keyword",
            excerpt_size=150,
            number_of_excerpts=1,
            pre_tags=[""],
            post_tags=[""],
            size=10,
            offset=0,
            sort_by="descending_date",
        )
        self.assertEqual(query["sort"][0]["date"]["order"], "desc")
        self.assertEqual(query["query"]["bool"]["must"][0]["simple_query_string"]["query"], "keyword")

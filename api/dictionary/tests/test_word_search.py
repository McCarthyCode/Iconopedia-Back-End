from django.conf import settings
from django.urls import reverse

from rest_framework import status
# from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient, APITestCase

from api.test_mixins import TestCaseShortcutsMixin

from ..models import Word, DictionaryEntry
from ..utils import ExternalAPIManager


class WordSearchTests(TestCaseShortcutsMixin, APITestCase):
    """
    Tests to check search endpoints. Checks against a hard-coded URL and a reverse-lookup name in nine tests, which check for an OPTIONS request and POST requests that validate user input.
    """
    client = APIClient()
    databases = {'default', 'admin_db'}

    search_word = 'hammer'
    search_word_entries = 2

    url_name = 'api:dict:search'
    url_path = f'/api/{settings.VERSION}/search/{search_word}'

    reverse_kwargs = {'word': search_word}

    def setUp(self):
        # reset the counter
        ExternalAPIManager.reset_mw_dict_calls()

    def test_options(self):
        """
        Ensure we can successfully get data from an OPTIONS request.
        """
        response = self.client.options(self.url_path, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictTypes(response.data, self.options_types)

    def __get_word(self):
        try:
            self.word = Word.objects.get(id=self.search_word)
        except Word.DoesNotExist:
            self.word = None

        return self.word

    def __get_dict_entries(self):
        return DictionaryEntry.objects.filter(word=self.word)

    def __check_dict_entries(self):
        for entry in self.__get_dict_entries():
            self.assertIsInstance(entry, DictionaryEntry)
            self.assertIsInstance(entry.json, str)
            self.assertGreater(len(entry.json), 0)

    def __test_success(self, response):
        """
        Ensure that we can query the Merriam-Webster dictionary API and populate our database.
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(ExternalAPIManager.mw_dict_calls(), 1)
        self.assertIsNotNone(self.__get_word())
        self.assertEquals(
            len(self.__get_dict_entries()), self.search_word_entries)

        types = {
            'results': [dict],
            'pagination': {
                'totalResults': int,
                'maxResultsPerPage': int,
                'numResultsThisPage': int,
                'thisPageNumber': int,
                'totalPages': int,
                'prevPageExists': int,
                'nextPageExists': int,
            }
        }

        self.assertDictTypes(response.data, types)

        types = {'id': str, 'sort': str, 'stems': [str], 'offensive': bool}

        for result in response.data['results']:
            self.assertDictTypes(result, types)

        self.__check_dict_entries()

    def test_success_miss(self):
        """
        Ensure that we can query the Merriam-Webster dictionary API and populate our database when the entry is not in store.
        """
        # execution
        response = self.client.get(self.url_path, format='json')

        # test
        self.assertEqual(ExternalAPIManager.mw_dict_calls(), 1)
        self.assertIsNotNone(self.__get_word())
        self.assertGreater(len(self.__get_dict_entries()), 0)
        self.__test_success(response)

    def test_success_hit(self):
        """
        Ensure that we can use the entry in store if one exists.
        """
        # test-specific setup - initial call to ensure a db entry exists
        self.client.get(self.url_path, format='json')
        self.assertIsNotNone(self.__get_word())
        self.assertEquals(
            len(self.__get_dict_entries()), self.search_word_entries)

        # execution
        response = self.client.get(self.url_path, format='json')

        # test
        self.__test_success(response)

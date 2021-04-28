from django.conf import settings

from rest_framework.exceptions import ErrorDetail


class TestCaseShortcutsMixin():
    """
    Class containing parameters and methods to help with testing response data.
    """
    options_types = {
        'name': str,
        'description': str,
        'renders': [str],
        'parses': [str]
    }
    credentials_types = {
        'credentials': {
            'type': str,
            'required': bool,
            'read_only': bool,
            'label': str,
            'children': {
                'username': {
                    'type': str,
                    'required': bool,
                    'read_only': bool,
                    'label': str,
                    'max_length': int
                },
                'email': {
                    'type': str,
                    'required': bool,
                    'read_only': bool,
                    'label': str,
                    'max_length': int
                },
                'password': {
                    'type': str,
                    'required': bool,
                    'read_only': bool,
                    'label': str,
                    'min_length': int,
                    'max_length': int
                },
                'tokens': {
                    'type': str,
                    'required': bool,
                    'read_only': bool,
                    'label': str,
                    'children': {
                        'access': {
                            'type': str,
                            'required': bool,
                            'read_only': bool,
                            'label': str,
                            'max_length': int
                        },
                        'refresh': {
                            'type': str,
                            'required': bool,
                            'read_only': bool,
                            'label': str,
                            'max_length': int
                        }
                    }
                }
            }
        }
    }

    def assertListType(self, _list, _type):
        """
        Method to check the type of members of a given list, based on a given type.
        """
        for item in _list:
            self.assertIsInstance(item, _type)

    def assertDictValues(self, obj, values_dict):
        """
        Method to check fields within a given dictionary, based a dictionary of values. First, the field is compared to the type of the value, then the value itself. If value is None, the value check is skipped.
        """
        self.assertEqual(len(values_dict), len(obj))
        for key, value in values_dict.items():
            self.assertIn(key, obj)

            if value == None:
                continue

            field = obj[key]
            value_type = type(value)

            if value_type == dict:
                self.assertDictValues(field, value)
            elif value_type == ErrorDetail:
                self.assertDictValues(field, value)
            elif value:
                self.assertIsInstance(field, value_type)
                self.assertEqual(field, value)

    def assertDictTypes(self, obj, types):
        """
        Method to check if the values of an object match the types defined in a second dictionary.
        """
        self.assertEqual(len(obj), len(types))
        for key, value in obj.items():
            if isinstance(value, dict):
                self.assertDictTypes(value, types[key])
            elif isinstance(value, list):
                self.assertListType(value, types[key][0])
            else:
                self.assertIsInstance(value, types[key])

    def assertCredentialsValid(
            self, obj, username='alice', email='alice@example.com'):
        """
        Method to check fields within a credentials dictionary, comparing username and email values to given parameters and comparing tokens to settings.TOKEN_REGEX.
        """
        fields = {'username': username, 'email': email, 'tokens': None}
        self.assertDictValues(obj, fields)

        tokens = obj['tokens']
        self.assertEqual(len(tokens), 2)
        for key, value in tokens.items():
            self.assertIsInstance(value, str)
            self.assertRegexpMatches(value, settings.TOKEN_REGEX)

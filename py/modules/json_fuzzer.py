import random
import json
import sys
import os

from helper import *

class JSONFuzzer:
    def __init__(self, input):
        try:
            self._json = json.load(input)
        except Exception as e:
            print(e)

    def invalid_json():
        return [ chr(random.randrange(0, 255)) for x in range(0, 1000) ].encode('UTF-8')

    def random_json():
        d = {}
        chances = [None, get_random_string(6), randint(0, 1024), deep_nested_json({}, 32)]
        for i in range(100):
            d[get_random_string(5)] = chances[randint(0, 3)]

        return payload

    # ASDASD
    def nullify_json(self):
        payload = self._json.copy()
        # set inputs to 0 equivelants
        for key in payload.keys():
            try:
                payload[key] += 1
                payload[key] = 0
            except TypeError:
                payload[key] = [] if (type(payload[key]) is dict) else ''

        return payload

    def all_null(self):
        payload = self._json.copy()
        for key in payload.keys():
            payload[key] = None

        return payload

    # asdasdasdas
    def add_fields(self):
        # add additional entries
        for i in range(25):
            payload = json_object.copy()
            for x in range(i):
                payload[get_random_string(10)] = get_random_string(5) if randint(0, 1) else randint(0, 262144)

            yield payload

    def remove_fields(self):
        for i in range(len(self._json.keys())):
            payload = json_object.copy()
            for x in range(i):
                # have chosen not to sort to have different subsets of fields removed (more random impact ?)
                del payload[list(self._json.keys())[x]]

            yield payload

    def swap_json_fields(self):
        fields = [ self._json[entry] for entry in self._json ]
        payload = self._json.copy()
        for entry in payload:
            payload[entry] = random.choice(fields)

        return payload

    # ADASDSA
    def wrong_type_values_json(self):
        return self._json.copy() + json.dumps(swap_json_values(self._json.copy())).encode("UTF-8")

    # TODO: fix the actions switch
    def random_types(self):
        actions = {
            'string': get_random_string(randint(16, 12000)),
            'boolean': random.choice([True, False]),
            'int': randint(-429496729, 429496729),
            'none': None,
            'list': list(range(randint(-64, 0), randint(0, 64))),
            'float': random.uniform(-128, 128),
            'dict': random_json(False)
        }

        for i in range(100):
            payload = self._json.copy()
            for key in payload.keys():
                choice = random.choice(actions.keys)
                payload(key) = actions[choice]

        return payload

    # ASDASDASASDS
    # performs type swaps on ints and strings in root level of json dict
    def swap_json_values(self):
        for key in self._json:
            try:
                self._json[key] += 1
                self._json[key] = get_random_string(randint(2, 10))
            except TypeError:
                if type(self._json[key]) is dict:
                    self._json[key] = swap_json_values(self._json[key])
                else:
                    self._json[key] = randint(2, 10)
        return self._json

    def deep_nested_json(dictionary, length):
        if length == 0:
            return randint(0, 1024)
        else:
            dictionary[get_random_string(8)] = deep_nested_json({}, length - 1)

        return dictionary

    # TODO: fix
    def get_random_format_string(size):
        return ''.join(random.choice(['%x', '%c', '%d', '%p']) for _ in range(size))

    def overflow_strings_json():
        payload = json_input.copy()
        for i in range(1000, 12000, 200):
            for key in payload.keys():
                try:
                    payload[key] += 1
                    payload[key] -= 1
                except TypeError:
                    if type(payload[key]) is str:
                        payload[key] = get_random_string(i)

            yield payload

    def integer_overflow_keys():
        keys = list(json_input.keys())
        for i in range(len(keys)):
            payload = json_input.copy()
            try:
                payload[keys[i]] += 1
                payload[keys[i]] = 429496729
            except TypeError:
                continue

            return payload

    def integer_overflow_values():
        payload = json_input.copy()
        for key in copy.keys():
            try:
                payload[key] += 1
                payload[key] = 429496729
            except TypeError:
                continue

        return payload

    def format_string_fuzz(self):
        payload = self._json.copy()
        for key in payload.keys():
            if type(payload[key]) is str:
                payload[key] = get_random_format_string(64)
            elif type(copy[key]) is int:
                payload[key] = 429496730

        return json.dumps(copy).encode("UTF-8")

    def generate_input(self):
        ##########################################################
        ##             Test valid (format) JSON data            ##
        yield ""    # check empty payload
        
        yield invalid_json()    # invalid json
        yield random_json()     # lots of random fields and things

        # actual fuzzing
        yield nullify_json()            # nullify fields - zero and empty strings
        yield all_null()

        yield add_fields()
        yield remove_fields()
        yield swap_json_fields()        # swap fields
        
        yield wrong_type_values_json()  # swapping expected data types - works for high level and sub dictionaries
        yield random_types()            # random type assignment
        
        yield format_string_fuzz()      # format strings
        yield overflow_strings_json()   # overflow strings
        yield overflow_integers_json()  # overflow integers

def json_fuzzer(binary, inputFile):
    context.log_level = 'WARNING'

    with open(inputFile) as input:
        for test_input in JSONFuzzer(input).generate_input():
            try:
                test_payload(binary, json.dumps(test_input).encode('UTF-8'))
            except Exception as e:
                print(e)
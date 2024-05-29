import json

from django.http import QueryDict
from django.test import TestCase

from NEMO.utilities import EmptyHttpRequest
from NEMO.widgets.dynamic_form import DynamicForm


class TestDynamicForm(TestCase):
    def test_formula_number_field(self):
        data = [
            {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
            {
                "name": "test_func",
                "type": "formula",
                "title": "test function",
                "formula": "test*2",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        http_request.POST["df_test"] = "2"
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_func"]["user_input"], str(2 * 2))

    def test_formula_float_field(self):
        data = [
            {"name": "test", "type": "float", "title": "Pair of wafer trays", "max-width": 250},
            {
                "name": "test_func",
                "type": "formula",
                "title": "test function",
                "formula": "test*2",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        http_request.POST["df_test"] = "2.0"
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_func"]["user_input"], str(2.0 * 2))

    def test_formula_zero(self):
        data = [
            {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
            {
                "name": "test_func",
                "type": "formula",
                "title": "test function",
                "formula": "test*0",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        http_request.POST["df_test"] = "2"
        extracted_value = json.loads(dynamic_form.extract(http_request))

        self.assertEqual(extracted_value["test_func"]["user_input"], str(0))

    def test_formula_zero_zero(self):
        data = [
            {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
            {
                "name": "test_func",
                "type": "formula",
                "title": "test function",
                "formula": "test*0",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        http_request.POST["df_test"] = "0"
        extracted_value = json.loads(dynamic_form.extract(http_request))

        self.assertEqual(extracted_value["test_func"]["user_input"], str(0))

    def test_formula_inside_group(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "test*0",
                    },
                ],
            }
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test"] = "2"
        http_request.POST["df_test_func"] = ""
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], str(0))

    def test_formula_with_no_value(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "test*2",
                    },
                ],
            }
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test"] = ""
        http_request.POST["df_test_func"] = ""
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], None)

    def test_formula_outside_group(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "test*0",
                    },
                ],
            },
            {
                "name": "test_group2",
                "type": "group",
                "title": "This is a test group2",
                "max_number": 2,
                "questions": [
                    {"name": "test2", "type": "number", "title": "Pair of wafer trays2", "max-width": 250},
                    {
                        "name": "test_func2",
                        "type": "formula",
                        "title": "test function2",
                        "formula": "test2*2",
                    },
                ],
            },
            {
                "name": "test_sum",
                "type": "formula",
                "title": "test function",
                "formula": "sum(test)",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test"] = "2"
        http_request.POST["df_test_2"] = "4"
        http_request.POST["df_test_func"] = ""
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], str(0))
        self.assertEqual(extracted_value["test_sum"]["user_input"], str(6))

    def test_formula_outside_group_with_spaces(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test unit", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "df_test_unit*0",
                    },
                ],
            },
            {
                "name": "test_group2",
                "type": "group",
                "title": "This is a test group2",
                "max_number": 2,
                "questions": [
                    {"name": "test2", "type": "number", "title": "Pair of wafer trays2", "max-width": 250},
                    {
                        "name": "test_func2",
                        "type": "formula",
                        "title": "test function2",
                        "formula": "test2*0",
                    },
                ],
            },
            {
                "name": "test_sum",
                "type": "formula",
                "title": "test function",
                "formula": "sum(df_test_unit)",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test_unit"] = "2"
        http_request.POST["df_test_unit_2"] = "4"
        http_request.POST["df_test_func"] = ""
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], str(0))
        self.assertEqual(extracted_value["test_sum"]["user_input"], str(6))

    def test_formula_using_other_formula_with_missing_arg(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "test*2",
                    },
                ],
            },
            {
                "name": "test_group2",
                "type": "group",
                "title": "This is a test group2",
                "max_number": 2,
                "questions": [
                    {"name": "test2", "type": "number", "title": "Pair of wafer trays2", "max-width": 250},
                    {
                        "name": "test_func2",
                        "type": "formula",
                        "title": "test function2",
                        "formula": "test2*4",
                    },
                ],
            },
            {
                "name": "test_sum",
                "type": "formula",
                "title": "test function",
                "formula": "sum(test_func) + sum(test_func2)",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test"] = "2"
        http_request.POST["df_test_2"] = "4"
        http_request.POST["df_test_func"] = ""
        http_request.POST["df_test_func2"] = ""
        http_request.POST["df_test_sum"] = ""
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], str(4))
        self.assertEqual(extracted_value["test_sum"]["user_input"], str(4))

    def test_formula_using_other_formula(self):
        data = [
            {
                "name": "test_group",
                "type": "group",
                "title": "This is a test group",
                "max_number": 2,
                "questions": [
                    {"name": "test", "type": "number", "title": "Pair of wafer trays", "max-width": 250},
                    {
                        "name": "test_func",
                        "type": "formula",
                        "title": "test function",
                        "formula": "test*2",
                    },
                ],
            },
            {
                "name": "test_group2",
                "type": "group",
                "title": "This is a test group2",
                "max_number": 2,
                "questions": [
                    {"name": "test2", "type": "number", "title": "Pair of wafer trays2", "max-width": 250},
                    {
                        "name": "test_func2",
                        "type": "formula",
                        "title": "test function2",
                        "formula": "test2*4",
                    },
                ],
            },
            {
                "name": "test_sum",
                "type": "formula",
                "title": "test function",
                "formula": "sum(test_func) + sum(test_func2)",
            },
        ]
        dynamic_form = DynamicForm(json.dumps(data))
        dynamic_form.validate("tool_usage_group_question", 1)
        http_request = EmptyHttpRequest()
        http_request.POST = QueryDict(mutable=True)
        # We are simulating what the request data would look like. Formula questions will render a hidden, no value input
        http_request.POST["df_test"] = "2"
        http_request.POST["df_test_2"] = "4"
        http_request.POST["df_test2"] = "3"
        http_request.POST["df_test2_2"] = "6"
        http_request.POST["df_test_func"] = ""
        http_request.POST["df_test_func_2"] = ""
        http_request.POST["df_test_func2"] = ""
        http_request.POST["df_test_func2_2"] = ""
        http_request.POST["df_test_sum"] = ""
        # Total = sum(test_func) + sum(test_func2) = sum(tests[]*2) + sum(test2[]*4)
        # = sum(2*2, 4*2) + sum(3*4, 6*4) = sum(4, 8) + sum(12, 24) = 12 + 36 = 48
        extracted_value = json.loads(dynamic_form.extract(http_request))
        self.assertEqual(extracted_value["test_group"]["user_input"]["0"]["test_func"], str(4))
        self.assertEqual(extracted_value["test_group"]["user_input"]["2"]["test_func"], str(8))
        self.assertEqual(extracted_value["test_group2"]["user_input"]["0"]["test_func2"], str(12))
        self.assertEqual(extracted_value["test_group2"]["user_input"]["2"]["test_func2"], str(24))
        self.assertEqual(extracted_value["test_sum"]["user_input"], str(48))

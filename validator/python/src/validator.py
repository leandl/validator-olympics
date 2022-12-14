from typing import Dict, List, Callable

from src.printer import Printer
from src.question import Question

class Validator:
    
    def __init__(self, questions: List[Question], questions_def: Dict[str, Callable]):
        self.__questions = questions
        self.__questions_def = questions_def

    def test_all(self):
        return [self.__get_info_question(name_question) for name_question in self.__questions_def.keys()]

    def __get_info_question(self, name_question: str):
        return {
            "number": self.__get_number_question(name_question),
            "data": self.test(name_question)
        }

    def __get_number_question(self, name_question: str) -> int:
        return int(''.join(c for c in name_question if c.isdigit()))

    def __get_index_question(self, name_question: str) -> int:
        number_question = self.__get_number_question(name_question)
        return number_question - 1
        
    def test(self, name_question: str): 
        index_question = self.__get_index_question(name_question)

        question = self.__questions[index_question]
        question_def = self.__questions_def.get(name_question)
        
        if not question:
            Printer.error("not existis question")

        if not question_def:
            Printer.error("not existis question function")

        data_tests = []
        for test in question.get_tests():
            test_args = test.get_args()
            result = question_def(*test_args)
            expected_result = test.get_result()

            data_tests.append({
                'args': test_args,
                'expected_result': expected_result,
                'result': result,
                'passed': result == expected_result
            })

        return data_tests











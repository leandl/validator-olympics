<?php
include_once __DIR__ . '/question.php';

if (!is_dir($pathexam)) {
    echo json_encode(['status' => 'error', 'message' => "Invalid path specified."]);
    die;
}
$files = scandir($pathexam);
$questionsDef = [];
foreach ($files as $file) {
    if (substr($file, -4) == '.php') {
        include_once $pathexam . '/' . $file;
        $aux = str_replace(".php", "", $file);
        $questionsDef[$aux] = $aux;
    }
}

class ValidatorException extends Exception
{
}

class Validator
{
    protected $questions;

    public function __construct($questions)
    {
        $this->questions = $questions;
    }

    public function testAll()
    {
        global $questionsDef;

        $response = [];
        foreach ($questionsDef as $nameQuestion => $question) {
            $response[] = [
                'number' => $this->getNumberQuestion($nameQuestion),
                'data' => $this->test($nameQuestion)
            ];
        }

        return $response;
    }

    private function getNumberQuestion(string $nameQuestion)
    {
        return (int) preg_replace("/[^0-9]/", "", $nameQuestion);
    }

    private function getIndexQuestion(string $nameQuestion)
    {
        return $this->getNumberQuestion($nameQuestion) - 1;
    }

    public function test(string $nameQuestion)
    {
        global $questionsDef;
        $index = $this->getIndexQuestion($nameQuestion);
        
        if (!isset($this->questions[$index])) {
            echo json_encode(['status' => 'error', 'message' => "Question doesn't exists."]);
            die;
        }

        if (!isset($questionsDef[$nameQuestion])) {
            echo json_encode(['status' => 'error', 'message' => "Function doesn't exists."]);
            die;
        }

        $question = $this->questions[$index];
        $questionFunction = $questionsDef[$nameQuestion];

        $response = [];

        foreach ($question->getTests() as $test) {
            $args = $test->getArgs();
            $expectedResult = $test->getResult();
            $results = $questionFunction(...$test->getArgs());
            $response[] = [
                'args' => $args,
                'expected_result' => $expectedResult,
                'result' => $results,
                'passed' => $results === $expectedResult
            ];
        }

        return $response;
    }
}

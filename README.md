# test-app

## Basic expression calculator written in Python (and second version in Go)

Server needs Flask framework to run.
Start server using ``FLASK_APP=main.py flask run``.
Calculator accepts digits (as integers and floats) and operators '+ - / * ( )'.
Negative numbers must be wrapped in parenthisis, e.g. (-1).
It transforms infix notation to postfix, then splits expression to smaller expressions and then evaluates them.


Go version shows how it could use multiprocessing (in function expressionEvaluation) to count every smaller expressions, because I couldn't make it in Python.

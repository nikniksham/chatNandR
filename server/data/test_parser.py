from flask_restful import reqparse

test_parser = reqparse.RequestParser()
test_parser.add_argument('some_data', type=str)

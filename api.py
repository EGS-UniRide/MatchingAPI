from flask import *
from flask_restx import Api, Resource, Namespace, fields
import math

app = Flask(__name__)
api = Api(app, version='1.0', title="Matching API",
          description='An API that evaluates the similarities between an object and a list of objects.' +
          '\nIt returns the objects that have more than 50% of similarity.')

ns = Namespace(
    'objects', description='The objects that the API will evaluate.')
api.add_namespace(ns)

objects_model = api.model('fields', dict(
    field1=fields.String(required=True, default="value1"),
    field2=fields.String(required=False, default="value2"),
    field3=fields.String(required=False, default="value3")
))

obj_lst_model = api.model('fields_lst', dict(
    field_lst1=fields.String(required=True, default="value1"),
    field_lst2=fields.String(required=False, default="value2"),
    field_lst3=fields.String(required=False, default="value3")
))

list_model = api.model('list', obj_lst_model)

body = api.model('objects', dict(
    objects=fields.Nested(objects_model),
    list=fields.Nested(list_model, as_list=True)
))


@ns.route('/v1/match')
@api.doc(responses={200: "Success"})
@api.doc(responses={404: "Match not found"})
@api.doc(responses={400: "Bad request"})
@api.doc(responses={500: "Internal Server Error"})
class MatchingAPI(Resource):
    @api.expect(body)
    def post(self):
        body_req = json.loads(request.data)
        keys = list(body_req.keys())

        # Verify if the body follows the syntax predefined
        if (len(keys) > 2):
            abort(400, 'Bad request: there\'s an error on the body request.')

        obj = {}
        lst = []

        # Storing the data into variables
        for key in keys:
            if ("dict" in str(type(body_req[key]))):
                obj = body_req[key]
            if ("list" in str(type(body_req[key]))):
                lst = body_req[key]
           
        if (len(obj) == 0 or len(lst) == 0):
            abort(400, 'Bad request: there\'s a type error on a key of the body request.')

        equals = {}
        index = 0
        # Iterate over the list of objects
        for elem in lst:
            count = 0
            for key in obj.keys():
                for key_lst in elem.keys():
                    if (key.strip() == key_lst.strip()):
                        if (obj[key] == elem[key_lst]):
                            # Count the equal keys and values
                            count += 1
            equals[index] = math.floor((count / len(elem)) * 100)
            index += 1

        # Verify if the equals elems have more than 50% of similarity
        match = []
        for elem in equals:
            if (equals[elem] > 50):
                match.append(lst[elem])

        return match


if __name__ == '__main__':
    app.run(debug=True, port=8030)

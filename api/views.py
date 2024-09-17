from ninja import NinjaAPI,Schema,Path,Query

api = NinjaAPI()

class HelloSchema(Schema):
    name: str | None  

@api.get("/hello")
def hello(request):
    return "Hello world"

# Path 
@api.get("/tmp_path/{name}/{phone}")
def tmp_query_path(request ,name:int ,phone:float ):
    return f"Hello {name} {phone}"


# Path 
@api.get("/tmp_path_schema/{name}/{phone}")
def tmp_path_schema(request ,params:Path[HelloSchema]):
    return f"Hello {params.name}"


# query  
@api.get("/tmp_query")
def tmp_query(request ,name:int ,phone:float = None):
    return f"Hello {name} {phone}"

# query  
@api.get("/tmp_query_schema")
def tmp_query_schema(request ,params:Query[HelloSchema]):
    return f"Hello {params.name}"


# Body  
@api.post("/tmp_body")
def tmp_query_body(request ,data: HelloSchema):
    try:
        return f"Hello {data.name}"
    except Exception as e :
        print(e)

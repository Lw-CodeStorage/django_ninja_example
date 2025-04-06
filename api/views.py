from functools import wraps
from ninja import NinjaAPI,Schema,Path,Query
from .cache import MemoryCache
from ninja.responses import Response
api = NinjaAPI()
# SETUP
cache = MemoryCache()

def requires_cache(fields):
    def decorator(f):
        @wraps(f)
        def decorated(request, *args, **kwargs):
            id = request.GET.get('id')   # <--- 這裡從 query string 取 id

            if id is None:
                return Response({"type": "error", "error": "No id provided"}, status=400)
            
            for field in fields:
                if cache.get(id=id, field=field) is None:
                    return Response({"type": "error", "error": f"No {field} found"}, status=400)
            
            field_values = {field: cache.get(id=id, field=field) for field in fields}
            field_values['id'] = id

            # 補上 field_values 到 kwargs
            return f(request, **field_values, **kwargs)
        return decorated
    return decorator

class HelloSchema(Schema):
    name: str | None  

@api.get("/hello")
def hello(request):
    return "Hello world"

@api.post("/catch/{name}")
def set_cache(request ,name:str):
    id = cache.generate_id()
    cache.set(id=id, field="name", value=name)
    return {"id": id}

@api.get("/cache/{id}")
def get_cache(request ,id:str):
    name = cache.get(id=id, field="name")
    return {"id": id, "name": name}

@api.get("/cache/test")
@requires_cache(fields=["name"])
def test_cache(request, id: str, **kwargs):
    return kwargs

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

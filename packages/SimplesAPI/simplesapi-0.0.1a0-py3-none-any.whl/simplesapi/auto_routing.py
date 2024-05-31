
import importlib
import os


def _import_handler(module_path, handler_name="handler"):
    spec = importlib.util.spec_from_file_location("routes", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, handler_name)

def _create_route_from_file(app, file_path):
    parts = file_path.split(os.sep)
    method_file = parts[-1]
    method = method_file.split('.')[0].split('__')[1].lower() if '__' in method_file else method_file.split('.')[0].lower()
    
    route = os.sep.join(parts[:-1])
    route = route.replace('routes', '')
    route = route.replace('[', '{').replace(']', '}')
    route = '/' + route.strip(os.sep)

    handler = _import_handler(file_path)
    
    if method == "get":
        app.get(route)(handler)
    elif method == "post":
        app.post(route)(handler)
    elif method == "put":
        app.put(route)(handler)
    elif method == "delete":
        app.delete(route)(handler)
    elif method == "patch":
        app.patch(route)(handler)

def register_routes(app, base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                _create_route_from_file(app, file_path)

import json,re
from collections import deque
import dihlibs.functions as fn

class JsonQ:
    def __init__(self, source=None, file_name=None):
        if isinstance(source, str):
            self.root = json.loads(source)
        elif isinstance(source, (list, dict)):
            self.root = source
        elif file_name:
            self.root = fn.file_dict(file_name)
        else:
            raise ValueError("Unsupported input type")

    def get(self, json_path, clazz=None):
        result = self._get(json_path)
        return clazz(result) if clazz else result

    def _log(self, e):
        print(f"Error: {e}")

    def _get(self, json_path):
        results = [self.root]
        paths = self._evaluate_path(json_path)
        for path in paths:
            results = self._traverse_path(path, results)
        return results

    def _evaluate_path(self, json_path):
        parts = re.finditer(PATH_POSSIBILITIES, json_path)
        paths = []
        for part in parts:
            for i in range(1, 4):
                if part.group(i):
                    paths.append(part.group(i))
        return paths

    def _traverse_path(self, path, results):
        handlers = {
            REGULAR_PATH: self._handle_normal_path,
            PATH_EXPRESSION: self._handle_path_expression,
            WILDCARD: self._handle_wildcard_path,
            MATCH_ALL: self._handle_match_all
        }
        temp = []

        for pattern, handler in handlers.items():
            if re.match(pattern, path):
                self._list_and_json_array_for_each(results, handler(path, temp))

        return temp

    def _handle_normal_path(self, path, temp):
        def add_to_temp(_, obj):
            temp.append(self._handle_normal_path_internal(path, obj))
        return add_to_temp

    def _handle_path_expression(self, path, temp):
        def extend_temp(_, obj):
            temp.extend(self._filter(obj, path))
        return extend_temp

    def _handle_wildcard_path(self, path, temp):
        def extend_matching_path(_, obj):
            temp.extend(self._find_matching_path(path, obj))
        return extend_matching_path

    def _handle_match_all(self, path, temp):
        def add_all(_, obj):
            self._flat_for_each(obj, lambda _, v: temp.append(v))
        return add_all

    def _list_and_json_array_for_each(self, input, consumer):
        if isinstance(input, (list, dict)):
            self._flat_for_each(input, consumer)
        else:
            consumer("", input)

    def _find_matching_path(self, json_path, root):
        results = []
        stack = deque([root])
        seen = set()
        path = re.sub(r"^\W+", "", json_path)

        def process_stack(current):
            result = self._handle_normal_path_internal(path, current)
            if result:
                results.append(result)
            self._flat_for_each(current, lambda _, obj: stack.append(obj) if id(obj) not in seen else None)
            seen.update(id(o) for o in stack)

        while stack:
            current = stack.pop()
            process_stack(current)
        return results

    def _filter(self, json_object, expression):
        results = []

        def add_to_results(key, obj):
            if self._evaluate_expression(key, obj, expression):
                results.append(obj)

        self._list_and_json_array_for_each(json_object, add_to_results)
        return results

    def _evaluate_expression(self, key, obj, expression):
        if isinstance(obj, dict):
            exp = expression
            for match in JSON_VARIABLE.finditer(expression):
                variable = match.group(1)
                value = obj.get(variable)
                if value is None:
                    return False
                if isinstance(value, str):
                    value=f"'{value}'"
                exp = exp.replace(f"@.{variable}", str(value))
                exp = re.sub(r'[\[\]?]','',exp);
            return eval(exp)
        elif self._json_primitive(obj):
            exp=expression.replace(f"@.{key}", str(obj))
            exp = re.sub(r'[\[\]?]','',exp);
            return eval(exp)[0]
        return False

    def _handle_normal_path_internal(self, path, json_object):
        if not path:
            return json_object
        current = json_object
        for p in path.split('.'):
            current = self._json_value(p, current)
        return current if current != json_object else None

    def _json_value(self, key, json_thing):
        if isinstance(json_thing, dict):
            return json_thing.get(key)
        elif isinstance(json_thing, list) and isinstance(key,int):
            try:
                return json_thing[int(key)]
            except (ValueError, IndexError):
                return None
        return json_thing


    def _flat_for_each(self, input, consumer):
        if isinstance(input, list):
            for idx, value in enumerate(input):
                consumer(str(idx), value)
       lif isinstance(input, dict):
            for key, value in input.items():
                consumer(key, value)
        elif isinstance(input, (set, tuple)):
            for value in input:
                consumer("", value)
        else:
            consumer("", input)

    def _json_primitive(self, obj):
        return isinstance(obj, (str, int, float, bool))


NUMBER_PATTERN = r"\d+.?\d*"
REGULAR_PATH = r"\w+(?:\.\w+)*"
MATCH_ALL = r"\[\*\]"
WILDCARD = r"\.{2,3}" + REGULAR_PATH
PATH_EXPRESSION = r".*\[\??\(.*"
PATH_POSSIBILITIES = r"(" + REGULAR_PATH + r")(" + WILDCARD + r")?(\([^)]+\)|\[[^]]+\])?"
JSON_VARIABLE = re.compile(r"@\.(\w+)")
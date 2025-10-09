import json

from rest_framework.views import APIView


class BaseAPIView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        drf_request = super().initialize_request(request, *args, **kwargs)

        def parse_value(value):
            """Convierte un string a int, float, bool, list o dict si es posible."""
            if isinstance(value, str):
                value = value.strip()
                try:
                    parsed = json.loads(value)
                    return parsed
                except (ValueError, json.JSONDecodeError):
                    pass

                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    return int(value)

                try:
                    return float(value)
                except ValueError:
                    pass

                if value.lower() == "true":
                    return True
                if value.lower() == "false":
                    return False
                return value
            return value

        def normalize(data):
            """Normaliza cualquier dict-like, parseando valores."""
            if hasattr(data, "dict"):
                data = data.dict()
            else:
                try:
                    data = dict(data)
                except Exception:
                    return {}

            normalized_data = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalized_data[k] = [parse_value(i) for i in v]
                else:
                    normalized_data[k] = parse_value(v)
            return normalized_data

        normalized = normalize(drf_request.data)

        normalized = {**normalize(drf_request.query_params), **normalized}

        drf_request._full_data = normalized

        return drf_request
from vital_ai_vitalsigns.ontology.ontology import Ontology
from vital_ai_vitalsigns.service.graph.binding import Binding


class ConstructQuery:
    def __init__(self, namespace_list: list[Ontology], binding_list: list[Binding], query: str,
                 limit: int | None = None, offset: int | None = None):
        self.namespace_list = namespace_list
        self.binding_list = binding_list
        self.query = query
        self.limit = limit
        self.offset = offset




class QueryExpander:

    def expand(self, query):

        return f"""
Repository code question:

{query}

Relevant functions classes implementation source code
"""
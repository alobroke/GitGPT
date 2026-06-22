class QueryExpander:

    def expand(self, query):

        return f"""
Repository source code question:

{query}

Find relevant:

- files
- classes
- methods
- functions
- implementations
- dependencies
- imports
- APIs
- routes
- configuration
- source code

Return repository-specific results.
"""
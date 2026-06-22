from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("Loading reranker...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Reranker loaded")

    def rerank(
        self,
        query,
        chunks,
        top_k=5
    ):

        if not chunks:
            return []

        pairs = []

        for chunk in chunks:

            rerank_text = f"""
File: {chunk.get('file', '')}

Class: {chunk.get('class_name', '')}

Name: {chunk.get('name', '')}

Type: {chunk.get('chunk_type', '')}

Code:
{chunk.get('content', '')}
"""

            pairs.append(
                (
                    query,
                    rerank_text
                )
            )

        scores = self.model.predict(
            pairs
        )

        ranked = []

        for chunk, score in zip(
            chunks,
            scores
        ):

            item = chunk.copy()

            item["rerank_score"] = float(score)

            ranked.append(item)

        ranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return ranked[:top_k]
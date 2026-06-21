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

        pairs = []

        for chunk in chunks:

            pairs.append(
                (
                    query,
                    chunk["content"]
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

            chunk["rerank_score"] = float(score)

            ranked.append(chunk)

        ranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return ranked[:top_k]
import math


class RuntimeVectorMemory:

    def __init__(self):

        self.memory = []

    def _embed(
        self,
        text
    ):

        vector = []

        for char in text.lower():

            vector.append(
                ord(char) % 32
            )

        return vector[:128]

    def _similarity(
        self,
        a,
        b
    ):

        length = min(
            len(a),
            len(b)
        )

        if length == 0:
            return 0

        total = 0

        for i in range(length):

            total += (
                a[i] * b[i]
            )

        magnitude_a = math.sqrt(
            sum(x * x for x in a)
        )

        magnitude_b = math.sqrt(
            sum(x * x for x in b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        return total / (
            magnitude_a * magnitude_b
        )

    def store(
        self,
        text,
        metadata=None
    ):

        self.memory.append(
            {
                "text": text,
                "vector": self._embed(text),
                "metadata": metadata or {}
            }
        )

    def search(
        self,
        query,
        limit=3
    ):

        query_vector = (
            self._embed(query)
        )

        ranked = []

        for item in self.memory:

            similarity = (
                self._similarity(
                    query_vector,
                    item["vector"]
                )
            )

            ranked.append(
                (
                    similarity,
                    item
                )
            )

        ranked.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item
            for _, item in ranked[:limit]
        ]
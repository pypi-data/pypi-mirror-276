import pytest

from .. import rank, retrieve


def cherche_retrievers(key: str, on: str):
    """List of retrievers available in cherche."""
    for retriever in [
        retrieve.TfIdf,
        retrieve.Lunr,
    ]:
        yield retriever(key=key, on=on, documents=documents())


def cherche_rankers(key: str, on: str):
    """List of rankers available in cherche."""
    from sentence_transformers import CrossEncoder, SentenceTransformer
    from transformers import pipeline

    yield from [
        rank.DPR(
            encoder=SentenceTransformer(
                "facebook-dpr-ctx_encoder-single-nq-base",
            ).encode,
            query_encoder=SentenceTransformer(
                "facebook-dpr-question_encoder-single-nq-base",
            ).encode,
            key=key,
            on=on,
        ),
        rank.Encoder(
            encoder=SentenceTransformer(
                "sentence-transformers/all-mpnet-base-v2",
            ).encode,
            key=key,
            on=on,
        ),
        rank.CrossEncoder(
            on=on,
            encoder=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1").predict,
        ),
    ]


def documents():
    return [
        {
            "id": 0,
            "title": "Paris",
            "article": "This town is the capital of France",
            "author": "Wikipedia",
        },
        {
            "id": 1,
            "title": "Eiffel tower",
            "article": "Eiffel tower is based in Paris",
            "author": "Wikipedia",
        },
        {
            "id": 2,
            "title": "Montreal",
            "article": "Montreal is in Canada.",
            "author": "Wikipedia",
        },
    ]


@pytest.mark.parametrize(
    "search, documents, k",
    [
        pytest.param(
            (retriever_a | retriever_b | retriever_c) + documents(),
            documents(),
            k,
            id=f"Union retrievers: {retriever_a.__class__.__name__} | {retriever_b.__class__.__name__} | {retriever_c.__class__.__name__} k: {k}",
        )
        for k in [None, 3, 4]
        for retriever_c in cherche_retrievers(key="id", on="title")
        for retriever_b in cherche_retrievers(key="id", on="article")
        for retriever_a in cherche_retrievers(key="id", on="author")
    ],
)
def test_retriever_union(search, documents: list, k: int):
    """Test retriever union operator."""
    # Empty documents
    search = search.add(documents)

    answers = search(q="France", k=k)
    assert len(answers) == min(k, 1) if k is not None else 1

    for sample in answers:
        for key in ["title", "article", "author"]:
            assert key in sample

    answers = search(q="Wikipedia", k=k)
    assert len(answers) == min(k, len(documents)) if k is not None else len(documents)

    answers = search(q="Unknown")
    assert len(answers) == 0


@pytest.mark.parametrize(
    "search, documents, k",
    [
        pytest.param(
            (retriever_a & retriever_b & retriever_c) + documents(),
            documents(),
            k,
            id=f"Intersection retrievers: {retriever_a.__class__.__name__} & {retriever_b.__class__.__name__}, & {retriever_c.__class__.__name__},  k: {k}",
        )
        for k in [None, 3, 4]
        for retriever_c in cherche_retrievers(key="id", on="title")
        for retriever_b in cherche_retrievers(key="id", on="article")
        for retriever_a in cherche_retrievers(key="id", on="author")
    ],
)
def test_retriever_intersection(search, documents: list, k: int):
    """Test retriever intersection operator."""
    # Empty documents
    search = search.add(documents)

    answers = search(q="Paris tower capital Montreal Canada France Wikipedia", k=k)
    if k is not None and k < len(documents):
        assert len(answers) >= (k // 3)
    else:
        assert len(answers) == len(documents)
    assert len(answers) <= len(documents)

    for sample in answers:
        for key in ["title", "article", "author"]:
            assert key in sample

    answers = search(q="is Wikipedia", k=k)
    assert len(answers) == 0

    answers = search(q="Paris capital France Wikipedia", k=k)
    if k is None or k >= 1:
        assert len(answers) == 1
    else:
        assert len(answers) == 0


@pytest.mark.parametrize(
    "search, documents, k",
    [
        pytest.param(
            ranker_a | ranker_b,
            documents(),
            k,
            id=f"Union rankers: {ranker_a.__class__.__name__} | {ranker_b.__class__.__name__} k: {k}",
        )
        for k in [None, 3, 4]
        for ranker_b in cherche_rankers(key="id", on="article")
        for ranker_a in cherche_rankers(key="id", on="title")
    ],
)
def test_ranker_union(search, documents: list, k: int):
    """Test retriever union operator."""
    search.add(documents)
    answers = search(q="Eiffel tower France", documents=documents, k=k)

    if k is not None:
        assert len(answers) == min(k, len(documents))
    else:
        assert len(answers) == len(documents)

    for index, sample in enumerate(answers):
        for key in ["title", "article", "author"]:
            assert key in sample

        if index == 0:
            assert sample["title"] == "Eiffel tower"

    answers = search(q="Canada", documents=documents, k=k)

    if k is None:
        assert answers[0]["title"] == "Montreal"
    elif k >= 1:
        assert answers[0]["title"] == "Montreal"
    else:
        assert len(answers) == 0

    # Empty documents.
    answers = search(q="Paris", documents=[], k=k)
    assert len(answers) == 0


@pytest.mark.parametrize(
    "search, documents, k",
    [
        pytest.param(
            ranker_a & ranker_b,
            documents(),
            k,
            id=f"Intersection rankers: {ranker_a.__class__.__name__} | {ranker_b.__class__.__name__} k: {k}",
        )
        for k in [None, 3, 4]
        for ranker_b in cherche_rankers(key="id", on="article")
        for ranker_a in cherche_rankers(key="id", on="title")
    ],
)
def test_ranker_intersection(search, documents: list, k: int):
    """Test retriever intersection operator."""
    search.add(documents)
    answers = search(q="Eiffel tower France", documents=documents, k=k)

    if k is not None:
        assert len(answers) == min(k, len(documents))
    else:
        assert len(answers) == len(documents)

    for index, sample in enumerate(answers):
        for key in ["title", "article", "author"]:
            assert key in sample

        if index == 0:
            assert sample["title"] == "Eiffel tower"

    answers = search(q="Canada", documents=documents, k=k)

    if k is None:
        assert answers[0]["title"] == "Montreal"
    elif k >= 1:
        assert answers[0]["title"] == "Montreal"
    else:
        assert len(answers) == 0

    # Empty documents.
    answers = search(q="Paris", documents=[], k=k)
    assert len(answers) == 0

import httpx

SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/"
SEMANTIC_SCHOLAR_FIELDS = (
    "url,title,venue,year,authors,externalIds,abstract,openAccessPdf,"
    "fieldsOfStudy,publicationTypes,journal"
)


def search_semantic_scholar(query, _results=None, _token=None):
    if _results is None:
        _results = []

    params = {
        "fields": SEMANTIC_SCHOLAR_FIELDS,
    }
    if _token:  # TODO first call does not have a token
        params["token"] = _token
    response = httpx.get(
        f"{SEMANTIC_SCHOLAR_BASE_URL}paper/search/bulk?query={query}&", params=params
    )
    response.raise_for_status()
    response = response.json()
    _results.extend(response["data"])
    print(f"Collected articles... {len(_results)}")

    # TODO remove recursive call
    if response.get("token"):
        search_semantic_scholar(query, _results=_results, _token=response["token"])
    return _results

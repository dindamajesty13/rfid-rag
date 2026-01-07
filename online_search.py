import requests

N8N_SEARCH_URL = "https://n8n.najihhome.dev/webhook/search"

def online_search(query: str, timeout: int = 20) -> dict:
    try:
        res = requests.get(
            N8N_SEARCH_URL,
            params={"question": query},
            timeout=timeout
        )
        res.raise_for_status()

        data = res.json()

        return {
            "answer": data.get("response", "").strip(),
            "sources": data.get("sources", [])
        }

    except Exception as e:
        print("[ONLINE SEARCH ERROR]", e)
        return {
            "answer": "",
            "sources": []
        }

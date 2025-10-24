# backend/agents/retriever_agent.py
import requests
import xml.etree.ElementTree as ET

class RetrieverAgent:
    def search_papers(self, query, max_results=3):
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
        response = requests.get(url)

        # Parse XML properly
        root = ET.fromstring(response.text)
        papers = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
            abstract_elem = entry.find("{http://www.w3.org/2005/Atom}summary")

            if title_elem is not None and abstract_elem is not None:
                title = title_elem.text.strip()
                abstract = abstract_elem.text.strip()
                papers.append({
                    "title": title,
                    "abstract": abstract
                })

        # Important: return a list, not raw XML text
        return papers

import logging
import requests
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class GOData:
    """
    A data class to hold information about a single Gene Ontology (GO) term.
    
    Using the @dataclass decorator automatically generates methods like
    __init__, __repr__, and __eq__, reducing boilerplate code.
    """
    # --- Class Attributes ---
    go_id: str
    name: str
    measurement: str
    namespace: str
    source: str
    terms_with_annotations: str
    date: str
    link: str

    # --- Private Class Constant ---
    _EBI_API_URL_TEMPLATE = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{GO_ID}"

    # --- Instance Methods ---
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the GOData instance.
        The dataclasses.asdict function is a convenient way to do this.
        """
        return asdict(self)

    # --- Properties ---
    @property
    def ebi_api_url(self) -> str:
        """
        Returns the full EBI API URL for this specific GO term.
        """
        return self._EBI_API_URL_TEMPLATE.format(GO_ID=self.go_id)

    # --- Class Methods (Alternative Constructors) ---
    @classmethod
    def from_api(cls, go_id: str):
        """
        An alternative constructor that fetches data from the EBI API
        and creates a GOData instance.

        Args:
            go_id (str): The Gene Ontology ID to fetch (e.g., "GO:0000001").

        Returns:
            GOData: An instance of the class, or None if the request fails.
        """
        logger.info(f"Fetching data for {go_id} from EBI API...")
        url = cls._EBI_API_URL_TEMPLATE.format(GO_ID=go_id)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()['results'][0]
            
            # Create and return an instance of the class using the fetched data
            return cls(
                go_id=data.get('id'),
                name=data.get('name'),
                measurement="Binary",  
                namespace=data.get('aspect', 'N/A').replace('_', ' ').title(),
                source="GO",
                terms_with_annotations="Terms with >1 annotation", 
                date=datetime.now().strftime("%d-%m-%Y"),
                link=f"http://www.ebi.ac.uk/QuickGO/GTerm?id={data.get('id')}"
            )
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse API response. Unexpected format. Error: {e}")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Creating an instance directly (like the original code)
    go_term_1 = GOData(
        go_id="GO:0000001",
        name="mitochondrion inheritance",
        measurement="Binary",
        namespace="GO Biological Process",
        source="GO",
        terms_with_annotations=10, # Example value
        date="02-03-2020",
        link="http://www.ebi.ac.uk/QuickGO/GTerm?id=GO:0000001"
    )
    print("--- Created directly ---")
    print(go_term_1)
    print("API URL:", go_term_1.ebi_api_url)
    print("As Dictionary:", go_term_1.to_dict())

    print("\n" + "="*40 + "\n")

    # Example 2: Creating an instance using the new class method from the API
    print("--- Created from API ---")
    go_term_2 = GOData.from_api("GO:0005829") # GO term for 'cytosol'
    if go_term_2:
        print(go_term_2)
        print("API URL:", go_term_2.ebi_api_url)

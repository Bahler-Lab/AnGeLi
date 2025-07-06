import logging
import requests
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import quote

logger = logging.getLogger(__name__)

@dataclass
class FYPOData:
    """
    A data class to hold information about a single Fission Yeast
    Phenotype Ontology (FYPO) term.
    
    Using the @dataclass decorator automatically generates methods like
    __init__, __repr__, and __eq__, reducing boilerplate code.
    """
    # --- Class Attributes ---
    fypo_id: str
    name: str
    measurement: str
    namespace: str
    source: str
    terms_with_annotations: str
    date: str
    link: str

    # --- Private Class Constant ---
    # The EBI OLS API requires the FYPO ID to be URL-encoded.
    _EBI_API_URL_TEMPLATE = "https://www.ebi.ac.uk/ols4/api/ontologies/fypo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F{fypo_id}"

    # --- Instance Methods ---
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the FYPOData instance.
        """
        return asdict(self)

    # --- Properties ---
    @property
    def ebi_api_url(self) -> str:
        """
        Returns the full EBI OLS API URL for this specific FYPO term.
        The FYPO ID part is URL-encoded for correctness.
        """
        # The API requires the colon in the ID to be encoded (e.g., FYPO_0000001)
        encoded_id = self.fypo_id.replace(":", "_")
        return self._EBI_API_URL_TEMPLATE.format(fypo_id=encoded_id)

    # --- Class Methods (Alternative Constructors) ---
    @classmethod
    def from_api(cls, fypo_id: str):
        """
        An alternative constructor that fetches data from the EBI OLS API
        and creates a FYPOData instance.

        Args:
            fypo_id (str): The FYPO ID to fetch (e.g., "FYPO:0000001").

        Returns:
            FYPOData: An instance of the class, or None if the request fails.
        """
        logger.info(f"Fetching data for {fypo_id} from EBI OLS API...")
        
        # The API requires the colon in the ID to be encoded (e.g., FYPO_0000001)
        encoded_id = fypo_id.replace(":", "_")
        url = cls._EBI_API_URL_TEMPLATE.format(fypo_id=encoded_id)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            # Create and return an instance of the class using the fetched data
            return cls(
                fypo_id=data.get('obo_id', fypo_id),
                name=data.get('label', 'N/A'),
                measurement="Binary",  # This info isn't in the API response
                namespace=data.get('ontology_prefix', 'N/A'),
                source="FYPO",
                terms_with_annotations="Terms with >1 annotation", # This info isn't in the API response
                date=datetime.now().strftime("%d-%m-%Y"),
                link=data.get('iri', '')
            )
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse API response. Unexpected format. Error: {e}")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Creating an instance directly
    fypo_term_1 = FYPOData(
        fypo_id="FYPO:0000001",
        name="phenotype",
        measurement="Binary",
        namespace="Phenotypes (FYPO)",
        source="FYPO",
        terms_with_annotations="Terms with >1 annotation", # Example value
        date="02-03-2020",
        link="http://www.pombase.org/term/FYPO:0000001"
    )
    print("--- Created directly ---")
    print(fypo_term_1)
    print("API URL:", fypo_term_1.ebi_api_url)
    print("As Dictionary:", fypo_term_1.to_dict())

    print("\n" + "="*40 + "\n")

    # Example 2: Creating an instance using the new class method from the API
    print("--- Created from API ---")
    # FYPO:0002061 is "viable"
    fypo_term_2 = FYPOData.from_api("FYPO:0002061") 
    if fypo_term_2:
        print(fypo_term_2)
        print("API URL:", fypo_term_2.ebi_api_url)


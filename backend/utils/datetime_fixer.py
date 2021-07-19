from datetime import datetime
from app.models.subreddit import Extracted_Created_Date

def datetimefixer(extracted_at: float, created_at: float) -> Extracted_Created_Date:
    extracted_at = datetime.utcfromtimestamp(extracted_at).utcnow()
    created_at = datetime.utcfromtimestamp(created_at).utcnow()
    return Extracted_Created_Date(extracted_at=extracted_at,created_at=created_at)



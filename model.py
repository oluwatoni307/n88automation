from typing import Optional, List
from pydantic import BaseModel, Field



class Choose(BaseModel):
    choice: bool = Field(
        description="decide if the call is a sales call or not"
    )



class PricingOption(BaseModel):
    low: Optional[str] = Field(None, description="Minimal offer that lacks core needs")
    mid: Optional[str] = Field(None, description="Full solution close to the client’s budget")
    high: Optional[str] = Field(None, description="Premium anchor offer with maximum value")

class SalesBrief(BaseModel):
    company_name: Optional[str] = Field(None, description="Name of the client's company")
    contact_person: Optional[str] = Field(None, description="Name of the primary contact person")
    pain_points: Optional[str] = Field(None, description="Key pain points mentioned by the client")
    objections: Optional[str] = Field(None, description="Objections or concerns raised by the client")
    summary: Optional[str] = Field(None, description="Summary of the sales call conversation")
    close_strategy: Optional[str] = Field(None, description="Proposed strategy to close the deal")
    pricing: Optional[PricingOption] = Field(None, description="Breakdown of pricing tiers: Low, Mid, High")

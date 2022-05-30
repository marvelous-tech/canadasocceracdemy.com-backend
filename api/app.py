from ninja import NinjaAPI

from campaign.api.api import router as campaign_router

api = NinjaAPI()

api.add_router('/campaign', campaign_router)

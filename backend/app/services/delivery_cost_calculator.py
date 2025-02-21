from datetime import datetime
from typing import List

from app.core.logger import logger
from app.db.models.package import Package
from app.external.CBRF_client import CBRFClient


class DeliveryCostCalculator:
    def __init__(self, cbrf_client: CBRFClient):
        self.cbrf_client = cbrf_client

    async def calculate_delivery_cost(
        self, weight: float, content_cost: float
    ) -> float:
        """Calculate delivery cost in rubles."""
        rates = await self.cbrf_client.get_daily_rates()
        usd_rate = rates["Valute"]

        delivery_cost = (weight * 0.5 + content_cost * 0.01) * usd_rate
        return round(delivery_cost, 2)

    async def process_unprocessed_packages(self, packages: List[Package]) -> None:
        """Process packages without delivery cost."""
        try:
            for package in packages:
                delivery_cost = await self.calculate_delivery_cost(
                    weight=package.weight, content_cost=package.content_cost
                )
                package.delivery_cost = delivery_cost

            logger.info(f"Processed {len(packages)} packages with delivery costs")
        except Exception as e:
            logger.error(f"Error processing packages: {str(e)}")

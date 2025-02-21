import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.logger import logger
from app.db.repositories.package_repository import PackageRepository
from app.external.CBRF_client import CBRFClient
from app.services.delivery_cost_calculator import DeliveryCostCalculator


class DeliveryCostScheduler:
    def __init__(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
        interval_seconds: int = 300,  # 5 minutes
    ):
        self.async_session_maker = async_session_maker
        self.interval_seconds = interval_seconds
        self.is_running = False
        self.task: Optional[asyncio.Task] = None

    async def process_delivery_costs(self) -> None:
        """Process delivery costs for unprocessed packages."""
        async with self.async_session_maker() as session:
            try:
                # Get unprocessed packages
                package_repository = PackageRepository(session)
                packages = await package_repository.get_unprocessed_packages()

                if not packages:
                    logger.info("No unprocessed packages found")
                    return

                # Calculate delivery costs
                async with CBRFClient() as cbrf_client:
                    calculator = DeliveryCostCalculator(cbrf_client)
                    await calculator.process_unprocessed_packages(packages)

                # Update packages in database
                await package_repository.bulk_update_delivery_costs(packages)

                logger.info(f"Successfully processed {len(packages)} packages")

            except Exception as e:
                logger.error(f"Error in delivery cost processing: {str(e)}")

    async def start(self) -> None:
        """Start the scheduler."""
        if self.is_running:
            return

        self.is_running = True

        async def run_scheduler():
            while self.is_running:
                await self.process_delivery_costs()
                await asyncio.sleep(self.interval_seconds)

        self.task = asyncio.create_task(run_scheduler())
        logger.info("Delivery cost scheduler started")

    async def stop(self) -> None:
        """Stop the scheduler."""
        if self.is_running and self.task:
            self.is_running = False
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            logger.info("Delivery cost scheduler stopped")

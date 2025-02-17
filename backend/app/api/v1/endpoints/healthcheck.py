from fastapi import APIRouter, HTTPException, status

from app.schemas.healthcheck import HealthCheckResponse
from app.services.health_checker import health_checker

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Проверка состояния сервиса",
)
async def health_check():
    """Проверка доступности сервиса и его зависимостей"""
    checks = {
        "database": await health_checker.check_database(),
        "redis": await health_checker.check_redis(),
    }

    overall_status = (
        "ok" if all(v["status"] == "ok" for v in checks.values()) else "degraded"
    )

    return {
        "status": overall_status,
        "version": health_checker.version,
        "uptime": health_checker.uptime,
        "timestamp": health_checker.timestamp,
        "dependencies": checks,
    }


@router.get(
    "/health/logs",
    # status_code=status.HTTP_200_OK,
    summary="Проверка логов сервиса",
)
async def log_example():
    import logging

    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("Это информационное сообщение")
    logger.debug("Это отладочное сообщение")
    logger.warning("Это предупреждение")

    # try:
    #     # Ошибка деления на ноль
    #     result = 10 / 0
    #     return {"result": result}
    # except ZeroDivisionError as e:
    #     logger.error("Произошла ошибка: %s", str(e))
    #     raise HTTPException(status_code=500, detail="Произошла ошибка сервера") from e

    result = 10 / 0
    return {"result": result}

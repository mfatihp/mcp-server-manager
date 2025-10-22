import json
import time
import redis
from fastapi import Request



r = redis.Redis(
                host="mcp_manager_db_redis",
                port=6379,
                db=5,
                decode_responses=True,
                socket_timeout=2,
                health_check_interval=30
            )


async def log_success_responses(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time)),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": duration,
            "client_ip": request.client.host if request.client else None,
        }

        if 200 <= response.status_code < 300:
            r.lpush("service_logs", json.dumps(log_entry))

        return response

    except Exception as e:
        duration = round(time.time() - start_time, 4)
        r.lpush("service_logs", json.dumps({
                                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time)),
                                            "method": request.method,
                                            "path": request.url.path,
                                            "status_code": "error",
                                            "error": str(e),
                                            "duration": duration,
                                        }))
        raise

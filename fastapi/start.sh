uvicorn proxy_app:proxy --reload --host 0.0.0.0 --port 8000 T & uvicorn proxy_app:api_app --reload --host 0.0.0.0 --port 8001
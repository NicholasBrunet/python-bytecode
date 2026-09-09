import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .api.auth import router as auth_router
from .services.auth import FRONT_END_URL
import os

app = FastAPI()

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the structure of your incoming HTTP request data
# class DataPayload(BaseModel):
#     device_id: str
#     command: str

# UNIX_SOCKET_PATH: str = os.environ.get("UNIX_SOCKET_PATH", "")

# @app.get("/test-tcp")
# async def route_data_to_tcp():
#     try:
#         # 1. Open a non-blocking TCP socket connection
#         reader, writer = await asyncio.open_unix_connection(UNIX_SOCKET_PATH)
        
#         # -------------------------------------------------------------
#         # Protocol for asking the Orchestrator to do the following:
#         # - Startup a virtual runtime for a UNIQUE USER/CLIENT ID
#         #   this should also LOAD CLIENT ID stored modules (cached and)
#         #   pesisted via DB/other persistence mechanism through web
#         # - Check if a virtual runtime is running for a CLIENT ID
#         # - Stop a virtual runtime for a CLIENT ID
#         # - add a modules to a virtual runtime for a CLIENT ID
#         # - execute a module on a virtual runtime for a CLIENT ID
#         # - delete a module on a virtual runtime for a CLIENT ID
#         # - list all modules on a virtual runtime for a CLIENT ID
#         # -------------------------------------------------------------

#         payload = b"test" 
        
#         writer.write(payload)
#         await writer.drain()
#         # -------------------------------------------------------------
        
#         # 2. Read response stream from Orchestrator
#         response_bytes = await reader.read(1024)
        
#         # 3. Clean up the socket connection channel
#         writer.close()
#         await writer.wait_closed()
        
#         return {"status": "data_sent", "response": list(response_bytes)}

#     except Exception as e:
#         # Handle connection failures gracefully without crashing the server
#         raise HTTPException(status_code=500, detail=f"TCP Error: {str(e)}")

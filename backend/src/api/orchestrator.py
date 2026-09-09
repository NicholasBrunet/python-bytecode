# from fastapi import Depends

# from ..services.auth import get_current_user_id
# from ..server import app

# @app.get("/pvr/me")
# async def me(current_client_id: str = Depends(get_current_user_id)):

#     return {
#         "message": f"Successfully authenticated client context!",
#         "client_id": current_client_id
#     }
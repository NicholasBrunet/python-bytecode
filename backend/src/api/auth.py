from fastapi import Request, Depends, APIRouter
from fastapi.responses import RedirectResponse

from ..services.auth import microsoft_sso, create_access_token, get_current_user_id, FRONT_END_URL


router = APIRouter()

@router.get("/auth/login")
async def auth_microsoft_login():
    """Step 1: Redirects the user's browser directly to Microsoft's Passwordless Login Page."""
    async with microsoft_sso:
        return await microsoft_sso.get_login_redirect()

@router.get("/auth/callback")
async def auth_microsoft_callback(request: Request):
    async with microsoft_sso:
        user_profile = await microsoft_sso.verify_and_process(request)
        
    local_jwt_token = create_access_token(client_id=user_profile.id)
    
    return RedirectResponse(url=f"{FRONT_END_URL}/?access_token={local_jwt_token}")

@router.get("/auth/me")
async def me(current_client_id: str = Depends(get_current_user_id)):

    return {
        "message": f"You are succesfully authenticated via Microsoft!",
        "client_id": current_client_id
    }
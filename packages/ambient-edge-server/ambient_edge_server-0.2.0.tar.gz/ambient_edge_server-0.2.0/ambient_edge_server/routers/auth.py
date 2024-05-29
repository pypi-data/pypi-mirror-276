from fastapi import APIRouter, Depends

from ambient_edge_server.services.authorization_service import AuthorizationService
from ambient_edge_server.services.service_manager import svc_manager

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/")
async def authorize_node(
    node_id: str,
    device_code: str,
    auth_svc: AuthorizationService = Depends(svc_manager.get_authorization_service),
):
    """Authorize a node to connect to the backend API

    Args:
        node_id (str): Node ID
        device_code (str): Device code
        auth_svc (AuthorizationService, optional): Defaults to
            Depends(svc_manager.get_authorization_service).

    Returns:
        dict: Response
    """
    await auth_svc.authorize_node(node_id, device_code)
    return {"status": "success"}


@router.get("/status")
async def get_auth_status(
    auth_svc: AuthorizationService = Depends(svc_manager.get_authorization_service),
):
    """Get authorization status

    Args:
        auth_svc (AuthorizationService, optional): Defaults to
            Depends(svc_manager.get_authorization_service).

    Returns:
        dict: Response
    """
    result = await auth_svc.verify_authorization_status()
    if result.is_ok():
        return {"status": result.unwrap()}
    return {"status": result.unwrap_err()}

from fastapi import Depends, HTTPException, status
from .security import get_current_admin


def require_roles(roles: list[str]):

    def role_checker(current_admin = Depends(get_current_admin)):
        print(f"current admin: {current_admin}")
        if current_admin["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_admin

    return role_checker
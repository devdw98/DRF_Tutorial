"""
*객체 수준에서 권한 설정하기
코드 조각은 아무나 볼 수 있지만 업데이트와 삭제는 관리자만 할 수 있어야 한다.
이를 위해 커스텀 권한을 만들어야 한다
"""
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
    """
    def has_object_permission(self, request, view, obj):
        #읽기 권한은 모두에게 허용
        #GET, HEAD, OPTIONS 요청은 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #쓰기 권한은 코드 조각의 소유자에게만 부여
        return obj.owner == request.user
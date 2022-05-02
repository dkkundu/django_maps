"""API > views > user.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
# DRF IMPORTS
from rest_framework import generics, permissions, viewsets
# API IMPORTS
from API.serializers import UserSerializer


logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """Create new user API endpoint"""
    queryset = USER_MODEL.objects.none()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )  # overrides default

    def post(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating user: email={request.POST.get('email')}"
        )
        return super().post(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """CRUD view set for User model and serializer"""
    queryset = USER_MODEL.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = ()  # check defaults in settings
    # permission_classes = ()  # check defaults in settings
    # filter_backends = ()  # check defaults in settings
    search_field = ('email', 'first_name', 'last_name', 'phone')
    ordering_fields = ('id', 'email', 'first_name', 'last_name', 'phone')
    ordering = 'id'

    def get_permissions(self):
        """Restrict normal users to only detail and update views"""
        if self.action == 'create' or \
                self.action == 'list' or \
                self.action == 'destroy':
            return (  # execute the function, example: IsAdminUser()
                permissions.IsAuthenticated(),
                permissions.IsAdminUser()
            )  # user must be an admin user for that above actions
        return super().get_permissions()

    def get_queryset(self):
        """Restrict normal users to their own user object only"""
        if not self.request.user.is_staff:  # restrict access to self object
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating user: email={request.POST.get('email')}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Retrieving user: {self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Updating user: {self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Partial update: {self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            "Listing users..."
        )
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """overriding to enable logging"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Deleting user... {self.lookup_field}={kwargs[self.lookup_field]}"
        )
        return super().list(request, *args, **kwargs)

# chat/tests/conftest.py
import pytest
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

@pytest.fixture
def test_application():

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": URLRouter(chat.routing.websocket_urlpatterns),
    })
    return application

from .start import start_router
from .wallets import wallets_router
from .transfers import transfer_router

all_routers = [
    start_router,
    wallets_router,
    transfer_router
]

import os

TOKEN=os.getenv("TELEGRAM_TOKEN")
JUPITER_REFERRAL_CONF = os.getenv("JUPITER_REFERRAL_CONF")
DB_CONNECT = os.getenv("DB_CONNECT", default="postgresql+asyncpg://myuser:mypassword@localhost:5433/mydatabase")
RPC_ENDPOINT = os.getenv("RPC_ENDPOINT")
SEND_RPC_ENDPOINT=os.getenv("SEND_RPC_ENDPOINT")
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_PASSWORD")
TEST_EXECUTOR = os.getenv("TEST_EXECUTOR", default="false").lower() == "true"
FAST_FEE = int(os.getenv("FAST_FEE", default=1_500_000))
TURBO_FEE = int(os.getenv("TURBO_FEE", default=7_500_000))
MOCK_TRANSACTION = "7eTQLYphWAGHh2QeEv4JXj1Stg7eLiknHawRycBCDwWF5ESYVrST5niuL6Zs2jePUpr2jQHk16Z438PXgGWLrUW"

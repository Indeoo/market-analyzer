import requests
from datetime import datetime
from loguru import logger
import asyncio

from data.db_utils import save_model, get_all_models
from data.models import Token


# Helper function to normalize datetimes
def normalize_datetime(dt_str):
    """Converts ISO datetime string to naive datetime in UTC."""
    if dt_str is None:
        return None
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))  # Parse as aware datetime
    return dt.replace(tzinfo=None)  # Convert to naive datetime in UTC


async def process_new_tokens(context, update, user_id):
    while True:
        new_tokens = await find_new_tokens()

        if new_tokens:
            for new_token in new_tokens:
                text = (
                    f"!!!NEW TOKEN ON JUPITER!!!\n"
                    f"Address: {new_token.address}\n"
                    f"Name: {new_token.name}\n"
                    f"Trade: https://jup.ag/swap/{new_token.address}-SOL"
                )
                await context.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    disable_web_page_preview=True
                )

        logger.info("SLEEP FOR 60 seconds...")
        await asyncio.sleep(60)


async def find_new_tokens():
    jupiter = requests.get("https://tokens.jup.ag/tokens?tags=verified")
    data = jupiter.json()
    logger.info("Retrieved new tokens")

    all_models = await get_all_models(Token)
    logger.info("Get all stored tokens")

    # List of addresses in the `list1`
    token_addresses = [token.address for token in all_models]
    # New list of tokens that have addresses not in `list1`
    new_tokens = [token_dict for token_dict in data if token_dict['address'] not in token_addresses]

    logger.info(f"New tokens amount: {len(new_tokens)}")

    for token_data in new_tokens:
        token = Token(
            address=token_data['address'],
            name=token_data['name'],
            symbol=token_data['symbol'],
            decimals=token_data['decimals'],
            logo_uri=token_data.get('logoURI'),
            tags=token_data.get('tags'),
            daily_volume=token_data.get('daily_volume'),
            created_at=normalize_datetime(token_data['created_at']),
            freeze_authority=token_data.get('freeze_authority'),
            mint_authority=token_data.get('mint_authority'),
            permanent_delegate=token_data.get('permanent_delegate'),
            minted_at=normalize_datetime(token_data.get('minted_at'))
            if token_data.get('minted_at')
            else None,
            extensions=token_data.get('extensions'),
        )
        await save_model(token)

    return new_tokens


# Run the async function
if __name__ == "__main__":
    asyncio.run(find_new_tokens())

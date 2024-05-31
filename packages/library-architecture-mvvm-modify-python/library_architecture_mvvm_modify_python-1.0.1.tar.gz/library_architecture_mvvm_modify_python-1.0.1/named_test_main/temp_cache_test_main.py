import asyncio
from library_architecture_mvvm_modify_python import *

def __listen_stream_from_key_temp_cache_and_callback_parameter_one(object: str) -> None:
    debug_print("Listen: " + object)

def __listen_stream_from_key_temp_cache_and_callback_parameter_one_first(object: str) -> None:
    debug_print("ListenTwo: " + object)

def __listen_stream_from_key_temp_cache_and_callback_parameter_one_second(object: str) -> None:
    debug_print("ListenThree: " + object)

async def main() -> None:
    temp_cache_service = TempCacheService()
    key = "key"
    temp_cache_service.update_where_stream_notification_is_possible_from_key_temp_cache_and_value_parameter_one(key,"One")
    from_key_temp_cache_parameter_temp_cache = temp_cache_service.get_from_key_temp_cache_parameter_temp_cache(key)
    debug_print("FromKeyTempCacheParameterTempCache: " + from_key_temp_cache_parameter_temp_cache)
    temp_cache_service.listen_stream_from_key_temp_cache_and_callback_parameter_one(key,__listen_stream_from_key_temp_cache_and_callback_parameter_one)
    await asyncio.sleep(1)
    temp_cache_service.update_where_stream_notification_is_possible_from_key_temp_cache_and_value_parameter_one(key,"Two")
    temp_cache_service.listen_stream_from_key_temp_cache_and_callback_parameter_one(key,__listen_stream_from_key_temp_cache_and_callback_parameter_one_first)
    await asyncio.sleep(1)
    temp_cache_service.update_where_stream_notification_is_possible_from_key_temp_cache_and_value_parameter_one(key,"Three")
    temp_cache_service.listen_stream_from_key_temp_cache_and_callback_parameter_one(key,__listen_stream_from_key_temp_cache_and_callback_parameter_one_second)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
## EXPECTED OUTPUT:
##
## FromKeyTempCacheParameterTempCache: One
## Listen: Two
## Listen: Three
## ListenTwo: Three
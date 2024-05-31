from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, TypeVar, Generic, final

QENUM = TypeVar("QENUM", bound=Enum)

@final
class ExceptionController():
    ### DO NOT CALL DIRECTLY, USE A STATIC METHOD: "success","exception"
    def __init__(self, exception: BaseException | None) -> None:
        self.__EXCEPTION: BaseException | None = exception
    
    @staticmethod
    def success() -> 'ExceptionController':
        return ExceptionController(None)
    
    @staticmethod
    def exception(exception: BaseException) -> 'ExceptionController':
        return ExceptionController(exception)
    
    def get_key_parameter_exception(self) -> str:
        if self.__EXCEPTION is None:
            return ""
        return self.__EXCEPTION.KEY
    
    def is_where_not_equals_null_parameter_exception(self) -> bool:
        return self.__EXCEPTION != None
    
    def to_string(self) -> str:
        if self.__EXCEPTION is None:
            return "ExceptionController(exception: null)"
        return "ExceptionController(exception: " + self.__EXCEPTION.to_string() + ")"

class BaseDataForNamed(Generic[QENUM], ABC):
    def __init__(self, is_loading: bool) -> None:
        self.is_loading: bool = is_loading
        self.exception_controller: ExceptionController = ExceptionController.success()

    @abstractmethod    
    def get_enum_data_for_named(self) -> QENUM:
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

class BaseException(Exception, ABC):
    def __init__(self, this_class: str, exception_class: str, key: str) -> None:
        self.KEY: str = key
        self.__THIS_CLASS: str = this_class
        self.__EXCEPTION_CLASS: str = exception_class

    @abstractmethod
    def to_string(self) -> str:
        pass
    
    ### Call this method in the descendant constructor as the last line
    def _debug_print_exception_where_to_string_parameters_this_class_and_exception_class(self) -> None:
        debug_print_exception("\n===start_to_trace_exception===\n")
        debug_print_exception(
            "WhereHappenedException(Class) --> " + self.__THIS_CLASS + "\n" +
            "NameException(Class) --> " + self.__EXCEPTION_CLASS + "\n" +
            "toString() --> " + self.to_string())
        debug_print_exception("\n===end_to_trace_exception===\n")

@final
class EnumGuilty(Enum):
    DEVELOPER = "developer"
    DEVICE = "device"
    USER = "user"

@final
class LocalException(BaseException):
    def __init__(self, this_class: str, enum_guilty: EnumGuilty, key: str, message: str = "") -> None:
        super().__init__(this_class, "LocalException", key)
        self.ENUM_GUILTY: EnumGuilty = enum_guilty
        self.MESSAGE: str = message
        self._debug_print_exception_where_to_string_parameters_this_class_and_exception_class()

    def to_string(self) -> str:
        return "LocalException(enumGuilty: " + self.ENUM_GUILTY.name + ", " + "key: " + self.KEY + ", " + "message (optional): " + self.MESSAGE + ")"

@final
class NetworkException(BaseException):
    def __init__(self, this_class: str, key: str, status_code: int, name_status_code: str = "", description_status_code: str = "") -> None:
        super().__init__(this_class, "NetworkException", key)
        self.STATUS_CODE: int = status_code
        self.NAME_STATUS_CODE: str = name_status_code
        self.DESCRIPTION_STATUS_CODE: str = description_status_code
        self._debug_print_exception_where_to_string_parameters_this_class_and_exception_class()

    @staticmethod
    def from_key_and_status_code(this_class: str,key: str, status_code: int) -> 'NetworkException':
        match status_code:
           case 201:
                return NetworkException(this_class, key, 201, "201 Created", "The request has been fulfilled and resulted in a new resource being created.")
           case 202:
                return NetworkException(this_class, key, 202, "202 Accepted", "The request has been accepted for processing, but the processing has not been completed.")
           case 203:
                return NetworkException(this_class, key, 203, "203 Non-Authoritative Information", "The returned metaInformation in the entity-header is not the definitive set as available from the origin server, but is gathered from a local or a third-party copy.")
           case 204:
                return NetworkException(this_class, key, 204, "204 No Content", "The server has fulfilled the request but does not need to return an entity-body, and might want to return updated metaInformation.")
           case 205:
                return NetworkException(this_class, key, 205, "205 Reset Content", "The server has fulfilled the request and the user agent SHOULD reset the document view which caused the request to be sent.")
           case 206:
                return NetworkException(this_class, key, 206, "206 Partial Content", "The server has fulfilled the partial GET request for the resource.")
           case 300:
                return NetworkException(this_class, key, 300, "300 Multiple Choices", "User (or user agent) can select a preferred representation and redirect its request to that location.")
           case 301:
                return NetworkException(this_class, key, 301, "301 Moved Permanently", "The requested resource has been assigned a new permanent URI and any future references to this resource SHOULD use one of the returned URIs.")
           case 302:
                return NetworkException(this_class, key, 302, "302 Found", "The requested resource resides temporarily under a different URI.")
           case 303:
                return NetworkException(this_class, key, 303, "303 See Other", "The response to the request can be found under a different URI and SHOULD be retrieved using a GET method on that resource.")
           case 304:
                return NetworkException(this_class, key, 304, "304 Not Modified", "If the client has performed a conditional GET request and access is allowed, but the document has not been modified, the server SHOULD respond with this status code.")
           case 305:
                return NetworkException(this_class, key, 305, "305 Use Proxy", "The requested resource MUST be accessed through the proxy given by the Location field.")
           case 307:
                return NetworkException(this_class, key, 307, "307 Temporary Redirect", "The requested resource resides temporarily under a different URI.")
           case 400:
                return NetworkException(this_class, key, 400, "400 Bad Request", "The request could not be understood by the server due to malformed syntax.")
           case 401:
                return NetworkException(this_class, key, 401, "401 Unauthorized", "The request requires user authentication.")
           case 403:
                return NetworkException(this_class, key, 403, "403 Forbidden", "The server understood the request, but is refusing to fulfill it.")
           case 404:
                return NetworkException(this_class, key, 404, "404 Not Found", "The server has not found anything matching the Request-URI.")
           case 405:
                return NetworkException(this_class, key, 405, "405 Method Not Allowed','The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.")
           case 406:
                return NetworkException(this_class, key, 406, "406 Not Acceptable", "The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.")
           case 407:
                return NetworkException(this_class, key, 407, "407 Proxy Authentication Required", "This code is similar to 401 (Unauthorized), but indicates that the client must first authenticate itself with the proxy.")
           case 408:
                return NetworkException(this_class, key, 408, "408 Request Timeout", "The client did not produce a request within the time that the server was prepared to wait.")
           case 409:
                return NetworkException(this_class, key, 409, "409 Conflict", "The request could not be completed due to a conflict with the current state of the resource.")
           case 410:
                return NetworkException(this_class, key, 410, "410 Gone", "The requested resource is no longer available at the server and no forwarding address is known.")
           case 411:
                return NetworkException(this_class, key, 411, "411 Length Required", "The server refuses to accept the request without a defined Content-Length.")
           case 412:
                return NetworkException(this_class, key, 412, "412 Precondition Failed", "The precondition given in one or more of the request-header fields evaluated to false when it was tested on the server.")
           case 413:
                return NetworkException(this_class, key, 413, "413 Request Entity Too Large", "The server is refusing to process a request because the request entity is larger than the server is willing or able to process.")
           case 414:
                return NetworkException(this_class, key, 414, "414 Request-URI Too Long", "The server is refusing to service the request because the Request-URI is longer than the server is willing to interpret.")
           case 415:
                return NetworkException(this_class, key, 415, "415 Unsupported Media Type", "The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method.")
           case 416:
                return NetworkException(this_class, key, 416, "416 Requested Range Not Satisfiable", "A server SHOULD return a response with this status code if a request included a Range request-header field (section 14.35), and none of the range-specifier values in this field overlap the current extent of the selected resource, and the request did not include an If-Range request-header field.")
           case 417:
                return NetworkException(this_class, key, 417, "417 Expectation Failed", "The expectation given in an Expect request-header field (see section 14.20) could not be met by this server.")
           case 500:
                return NetworkException(this_class, key, 500, "500 Internal Server Error", "The server encountered an unexpected condition which prevented it from fulfilling the request.")
           case 501:
                return NetworkException(this_class, key, 501, "501 Not Implemented", "The server does not support the functionality interface_function_view_model to fulfill the request.")
           case 502:
                return NetworkException(this_class, key, 502, "502 Bad Gateway", "The server, while acting as a gateway or proxy, received an invalid response from the upstream server it accessed in attempting to fulfill the request.")
           case 503:
                return NetworkException(this_class, key, 503, "503 Service Unavailable", "The server is currently unable to handle the request due to a temporary overloading or maintenance of the server.")
           case 504:
                return NetworkException(this_class, key, 504, "504 Gateway Timeout", "The server, while acting as a gateway or proxy, did not receive a timely response from the upstream server specified by the URI.")
           case 505:
                return NetworkException(this_class, key, 505, "505 HTTP Version Not Supported", "The server does not support, or refuses to support, the HTTP protocol version that was used in the request message.")
           case _:
                return NetworkException(this_class, key, 0)

    def to_string(self) -> str:
        return "NetworkException(key: " + self.KEY + ", " + "statusCode: " + self.STATUS_CODE + ", " + "nameStatusCode (optional): " + self.NAME_STATUS_CODE + ", " + "descriptionStatusCode (optional): " + self.DESCRIPTION_STATUS_CODE + ")"

class BaseModel(ABC):
    def __init__(self, unique_id: str) -> None:
        self.UNIQUE_ID: str = unique_id
    
    @abstractmethod
    def get_clone(self) -> 'BaseModel':
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

QBASEMODEL = TypeVar("QBASEMODEL", bound=BaseModel)

@final
class CurrentModelWIndex(Generic[QBASEMODEL], ABC):
    def __init__(self, current_model: QBASEMODEL, index: int) -> None:
        self.CURRENT_MODEL: QBASEMODEL = current_model
        self.INDEX: int = index
    
class BaseModelWNamedWNamedWNamedIterator(Generic[QBASEMODEL], ABC):
    def __init__(self) -> None:
        self._LIST_MODEL_ITERATOR: list[QBASEMODEL] = []
    
    @abstractmethod
    def current_model_w_index(self) -> CurrentModelWIndex[QBASEMODEL]:
        pass

    def get_sorted_list_model_from_new_list_model_parameter_list_model_iterator(self, new_list_model: list[QBASEMODEL]) -> list[QBASEMODEL]:
        if len(new_list_model) <= 0:
            return []
        self._LIST_MODEL_ITERATOR.extend(new_list_model)
        new_list_model_first = []
        while len(self._LIST_MODEL_ITERATOR) > 0:
            current_model_w_index = self.current_model_w_index()
            self._LIST_MODEL_ITERATOR.pop(current_model_w_index.INDEX)
            new_list_model_first.append(current_model_w_index.CURRENT_MODEL)
        return new_list_model_first

class BaseListModel(Generic[QBASEMODEL], ABC):
    def __init__(self, list_model: list[QBASEMODEL]) -> None:
        self.LIST_MODEL: list[QBASEMODEL] = list_model
    
    @abstractmethod
    def get_clone(self) -> 'BaseListModel':
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    def sorting_from_model_w_named_w_named_w_named_iterator_parameter_list_model(self,model_w_named_w_named_w_named_iterator: BaseModelWNamedWNamedWNamedIterator[QBASEMODEL]) -> None:
        sorted_list_model_from_new_list_model_parameter_list_model_iterator = model_w_named_w_named_w_named_iterator.get_sorted_list_model_from_new_list_model_parameter_list_model_iterator(self.LIST_MODEL)
        if len(self.LIST_MODEL) <= 0 and len(sorted_list_model_from_new_list_model_parameter_list_model_iterator) <= 0:
            return
        if len(self.LIST_MODEL) > 0 and len(sorted_list_model_from_new_list_model_parameter_list_model_iterator) <= 0:
            self.LIST_MODEL.clear()
            return
        self.LIST_MODEL.clear()
        self.LIST_MODEL.extend(sorted_list_model_from_new_list_model_parameter_list_model_iterator)

    def insert_from_new_model_parameter_list_model(self, new_model: QBASEMODEL) -> None:
        self.LIST_MODEL.append(new_model)
    
    def update_from_new_model_parameter_list_model(self, new_model: QBASEMODEL) -> None:
        for i in range(0,len(self.LIST_MODEL)):
            item_model = self.LIST_MODEL[i]
            if item_model.UNIQUE_ID != new_model.UNIQUE_ID:
                continue
            self.LIST_MODEL[i] = new_model
            break
    
    def delete_from_unique_id_by_model_parameter_list_model(self, unique_id_by_model: str) -> None:
        for i in range(0,len(self.LIST_MODEL)):
            item_model = self.LIST_MODEL[i]
            if item_model.UNIQUE_ID != unique_id_by_model:
                continue
            self.LIST_MODEL.pop(i)
            break
    
    def insert_list_from_new_list_model_parameter_list_model(self, new_list_model: list[QBASEMODEL]) -> None:
        self.LIST_MODEL.extend(new_list_model)
    
    def update_list_from_new_list_model_parameter_list_model(self, new_list_model: list[QBASEMODEL]) -> None:
        for i in range(0,len(new_list_model)):
            new_item_model = new_list_model[i]
            for y in range(0,len(self.LIST_MODEL)):
                item_model = self.LIST_MODEL[y]
                if item_model.UNIQUE_ID != new_item_model.UNIQUE_ID:
                    continue
                self.LIST_MODEL[y] = new_item_model
                break

    def delete_list_from_list_unique_id_by_model_parameter_list_model(self, list_unique_id_by_model: list[str]) -> None:
        for i in range(0,len(list_unique_id_by_model)):
            item_unique_id_by_model = list_unique_id_by_model[i]
            for y in range(0,len(self.LIST_MODEL)):
                item_model = self.LIST_MODEL[y]
                if item_model.UNIQUE_ID != item_unique_id_by_model:
                    continue
                self.LIST_MODEL.pop(y)
                break

class IDispose(ABC):
    @abstractmethod
    def dispose(self) -> None:
        pass

QBASEDATAFORNAMED = TypeVar("QBASEDATAFORNAMED", bound=BaseDataForNamed)

class BaseNamedState(IDispose, Generic[QBASEDATAFORNAMED], ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def get_data_for_named(self) -> QBASEDATAFORNAMED:
        pass

@final
class DefaultState(BaseNamedState[QBASEDATAFORNAMED], Generic[QBASEDATAFORNAMED]):
    def __init__(self, data_for_named: QBASEDATAFORNAMED) -> None:
        super().__init__()
        self.__DATA_FOR_NAMED: QBASEDATAFORNAMED = data_for_named
        self.__is_dispose: bool = False
    
    def dispose(self) -> None:
        if self.__is_dispose:
            return
        self.__is_dispose = True
    
    def get_data_for_named(self) -> QBASEDATAFORNAMED:
        return self.__DATA_FOR_NAMED

class BaseNamedStreamWState(IDispose, Generic[QBASEDATAFORNAMED], ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def dispose(self) -> None:
        pass
    
    @abstractmethod
    def get_data_for_named(self) -> QBASEDATAFORNAMED:
        pass

    @abstractmethod
    def listen_stream_data_for_named_from_callback(self,callback: Callable[[QBASEDATAFORNAMED], None]) -> None:
        pass

    @abstractmethod
    def notify_stream_data_for_named(self) -> None:
        pass

@final
class DefaultStreamWState(BaseNamedStreamWState[QBASEDATAFORNAMED], Generic[QBASEDATAFORNAMED]):
    def __init__(self, data_for_named: QBASEDATAFORNAMED) -> None:
        super().__init__()
        self.__DATA_FOR_NAMED: QBASEDATAFORNAMED = data_for_named
        self.__is_dispose: bool = False
        self.__callback: Callable[[QBASEDATAFORNAMED], None] | None = None
    
    def dispose(self) -> None:
        if self.__is_dispose:
            return
        self.__is_dispose = True
        self.__callback = None

    def get_data_for_named(self) -> QBASEDATAFORNAMED:
        return self.__DATA_FOR_NAMED
    
    def listen_stream_data_for_named_from_callback(self, callback: Callable[[QBASEDATAFORNAMED], None]) -> None:
        if self.__is_dispose:
            raise LocalException("DefaultStreamWState",EnumGuilty.DEVELOPER,"DefaultStreamWStateQQListenStreamDataForNamedFromCallback","Already disposed of")
        if self.__callback != None:
            raise LocalException("DefaultStreamWState",EnumGuilty.DEVELOPER,"DefaultStreamWStateQQListenStreamDataForNamedFromCallback","Duplicate")
        self.__callback = callback
    
    def notify_stream_data_for_named(self) -> None:
        if self.__is_dispose:
            raise LocalException("DefaultStreamWState",EnumGuilty.DEVELOPER,"DefaultStreamWStateQQNotifyStreamDataForNamed","Already disposed of")
        if self.__callback is None:
            raise LocalException("DefaultStreamWState",EnumGuilty.DEVELOPER,"DefaultStreamWStateQQNotifyStreamDataForNamed","Stream has no listener")
        self.__callback(self.__DATA_FOR_NAMED)

@final
class TempCacheService:
    __instance = None

    def __new__(cls) -> 'TempCacheService':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__temp_cache = {}
            cls.__instance.__temp_cache_w_list_action = {}
            return cls.__instance
        return cls.__instance
    
    @staticmethod
    def clear_temp_cache_parameter_instance() -> None:
        temp_cache: dict[str,object] = TempCacheService.__instance.__temp_cache
        temp_cache.clear()
    
    @staticmethod
    def close_stream_from_key_temp_cache_parameter_instance(key_temp_cache: str) -> None:
        temp_cache_w_list_action: dict[str,list[Callable[[object], None]]] = TempCacheService.__instance.__temp_cache_w_list_action
        if temp_cache_w_list_action.get(key_temp_cache) is None:
            return
        get = temp_cache_w_list_action.get(key_temp_cache)
        get.clear()
    
    @staticmethod
    def close_stream_from_list_key_temp_cache_parameter_instance(list_key_temp_cache: list[str]) -> None:
        temp_cache_w_list_action: dict[str,list[Callable[[object], None]]] = TempCacheService.__instance.__temp_cache_w_list_action
        for i in range(0,len(list_key_temp_cache)):
            item_key_temp_cache = list_key_temp_cache[i]
            if temp_cache_w_list_action.get(item_key_temp_cache) is None:
                return
            get = temp_cache_w_list_action.get(item_key_temp_cache)
            get.clear()
    
    @staticmethod
    def close_streams_parameter_instance() -> None:
        temp_cache_w_list_action: dict[str,list[Callable[[object], None]]] = TempCacheService.__instance.__temp_cache_w_list_action
        for _,value in temp_cache_w_list_action.items():
            value.clear()
    
    def get_from_key_temp_cache_parameter_temp_cache(self, key_temp_cache: str) -> object:
        temp_cache: dict[str,object] = self.__temp_cache
        if temp_cache.get(key_temp_cache) is None:
            raise LocalException("TempCacheService",EnumGuilty.DEVELOPER,key_temp_cache,"No exists key")
        return temp_cache.get(key_temp_cache)
    
    def listen_stream_from_key_temp_cache_and_callback_parameter_one(self, key_temp_cache: str, callback: Callable[[object], None]) -> None:
        temp_cache_w_list_action: dict[str,list[Callable[[object], None]]] = self.__temp_cache_w_list_action
        if temp_cache_w_list_action.get(key_temp_cache) is None:
            temp_cache_w_list_action[key_temp_cache] = list[Callable[[object], None]]()
            temp_cache_w_list_action.get(key_temp_cache).append(callback)
            return
        temp_cache_w_list_action.get(key_temp_cache).append(callback)
    
    def update_from_key_temp_cache_and_value_parameter_temp_cache(self, key_temp_cache: str, value: object) -> None:
        self.__temp_cache[key_temp_cache] = value

    def update_where_stream_notification_is_possible_from_key_temp_cache_and_value_parameter_one(self, key_temp_cache: str, value: object) -> None:
        self.update_from_key_temp_cache_and_value_parameter_temp_cache(key_temp_cache,value)
        temp_cache_w_list_action: dict[str,list[Callable[[object], None]]] = self.__temp_cache_w_list_action
        if temp_cache_w_list_action.get(key_temp_cache) is None:
            return
        get = temp_cache_w_list_action.get(key_temp_cache)
        for item_get in get:
            item_get(value)
    
    def delete_from_key_temp_cache_parameter_temp_cache(self, key_temp_cache: str) -> None:
        self.__temp_cache.pop(key_temp_cache)

@final
class EnumRWTMode(Enum):
    RELEASE = "release"
    TEST = "test"

@final
class NamedCallback():
    def __init__(self, name: str, callback: object) -> None:
        self.NAME: str = name
        self.CALLBACK: object = callback

@final
class RWTMode():
    def __init__(self, enum_rwt_mode: EnumRWTMode, list_named_callback_w_release: list[NamedCallback], list_named_callback_w_test: list[NamedCallback]) -> None:
        self.__ENUM_RWT_MODE: EnumRWTMode = enum_rwt_mode
        self.__DICT_STR_W_NAMED_CALLBACK_W_RELEASE: dict[str,NamedCallback] = RWTMode.__get_dict_str_w_named_callback_from_list_named_callback(list_named_callback_w_release)
        self.__DICT_STR_W_NAMED_CALLBACK_W_TEST: dict[str,NamedCallback] = RWTMode.__get_dict_str_w_named_callback_from_list_named_callback(list_named_callback_w_test)
    
    @staticmethod
    def __get_dict_str_w_named_callback_from_list_named_callback(list_named_callback: list[NamedCallback]) -> dict[str,NamedCallback]:
        dict_str_w_named_callback = dict[str,NamedCallback]()
        for item_named_callback in list_named_callback:
            dict_str_w_named_callback[item_named_callback.NAME] = item_named_callback
        return dict_str_w_named_callback
    
    def get_named_callback_from_name(self, name: str) -> NamedCallback:
        dict_str_w_named_callback_where_select_mod_parameters_three = self.__get_dict_str_w_named_callback_where_select_mod_parameters_three()
        if dict_str_w_named_callback_where_select_mod_parameters_three.get(name) is None:
            raise LocalException("RWTMode",EnumGuilty.DEVELOPER,"RWTModeQQGetNamedCallbackFromName","no exists key: " + name)
        return dict_str_w_named_callback_where_select_mod_parameters_three.get(name)

    def __get_dict_str_w_named_callback_where_select_mod_parameters_three(self) -> dict[str,NamedCallback]:
        if self.__ENUM_RWT_MODE == EnumRWTMode.RELEASE:
            return self.__DICT_STR_W_NAMED_CALLBACK_W_RELEASE
        return self.__DICT_STR_W_NAMED_CALLBACK_W_TEST

@final
class Result():
    ### DO NOT CALL DIRECTLY, USE A STATIC METHOD: "success","exception"
    def __init__(self, parameter: object | None, exception_controller: ExceptionController) -> None:
        self.PARAMETER: object | None = parameter
        self.EXCEPTION_CONTROLLER: ExceptionController = exception_controller
    
    @staticmethod
    def success(parameter: object) -> 'Result':
        return Result(parameter,ExceptionController.success())
    
    @staticmethod
    def exception(exception: BaseException) -> 'Result':
        return Result(None,ExceptionController.exception(exception))

def debug_print(text: str) -> None:
    print(text)

def debug_print_exception(text: str) -> None:
    debug_print("\x1B[31m" + text + "\x1b[0m")
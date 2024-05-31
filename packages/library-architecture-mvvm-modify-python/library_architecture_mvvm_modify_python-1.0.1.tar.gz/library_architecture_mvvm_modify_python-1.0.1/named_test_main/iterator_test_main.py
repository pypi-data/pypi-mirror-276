from typing import Generic, TypeVar
from library_architecture_mvvm_modify_python import *

class UserBalance(BaseModel):
    def __init__(self, username: str, money: int) -> None:
        super().__init__(username)
        self.USERNAME: str = username
        self.MONEY: int = money
    
    def get_clone(self) -> 'UserBalance':
        return UserBalance(self.USERNAME,self.MONEY)
    
    def to_string(self) -> str:
        return "UserBalance(username: " + self.USERNAME + ", " + "money: " + str(self.MONEY) + ")"

T = TypeVar("T", bound=UserBalance)

class ListUserBalance(Generic[T],BaseListModel[T]):
    def __init__(self, list_model: list[T]) -> None:
        super().__init__(list_model)
    
    def get_clone(self) -> 'ListUserBalance':
        new_list_model: list[T] = []
        for item_model in self.LIST_MODEL:
            new_list_model.append(item_model.get_clone())
        return ListUserBalance(new_list_model)
    
    def to_string(self) -> str:
        str_list_model = "\n"
        for item_model in self.LIST_MODEL:
            str_list_model += item_model.to_string() + ",\n"
        return "ListUserBalance(listModel: [" + str_list_model + "])"

class UserBalanceWOrderByDescWMoneyIterator(Generic[T],BaseModelWNamedWNamedWNamedIterator[T]):
    def __init__(self) -> None:
        super().__init__()
    
    def current_model_w_index(self) -> CurrentModelWIndex[T]:
        clone = self._LIST_MODEL_ITERATOR[0].get_clone()
        if(len(self._LIST_MODEL_ITERATOR) <= 1):
            return CurrentModelWIndex[T](clone,0)
        index_remove = 0
        for i in range(1,len(self._LIST_MODEL_ITERATOR)):
            item_model_iterator = self._LIST_MODEL_ITERATOR[i]
            if item_model_iterator.MONEY > clone.MONEY:
                clone = item_model_iterator.get_clone()
                index_remove = i
                continue
        return CurrentModelWIndex[T](clone,index_remove)


def main() -> None:
    list_user_balance = ListUserBalance[UserBalance]([])
    list_user_balance.insert_list_from_new_list_model_parameter_list_model([
        UserBalance("Jone",3),
        UserBalance("Freddy",1),
        UserBalance("Mitsuya",10),
        UserBalance("Duramichi",5),
        UserBalance("Hook",7),
        UserBalance("Sexy",-1)
    ])
    debug_print("Before: " + list_user_balance.to_string()) ## 3, 1, 10, 5, 7, -1
    user_balance_w_order_by_desc_w_money_iterator = UserBalanceWOrderByDescWMoneyIterator[UserBalance]()
    list_user_balance.sorting_from_model_w_named_w_named_w_named_iterator_parameter_list_model(user_balance_w_order_by_desc_w_money_iterator)
    debug_print("After: " + list_user_balance.to_string()) ## 10, 7, 5, 3, 1, -1
    list_user_balance.update_from_new_model_parameter_list_model(UserBalance("Duramichi",15))
    list_user_balance.sorting_from_model_w_named_w_named_w_named_iterator_parameter_list_model(user_balance_w_order_by_desc_w_money_iterator)
    debug_print("After(Two): " + list_user_balance.to_string()) ## 15, 10, 7, 3, 1, -1
    list_user_balance.delete_from_unique_id_by_model_parameter_list_model("Mitsuya")
    list_user_balance.sorting_from_model_w_named_w_named_w_named_iterator_parameter_list_model(user_balance_w_order_by_desc_w_money_iterator)
    debug_print("After(Three): " + list_user_balance.to_string()) ## 15, 7, 3, 1, -1
## EXPECTED OUTPUT:
##
## Before: ListUserBalance(listModel: [
## UserBalance(username: Jone, money: 3),
## UserBalance(username: Freddy, money: 1),
## UserBalance(username: Mitsuya, money: 10),
## UserBalance(username: Duramichi, money: 5),
## UserBalance(username: Hook, money: 7),
## UserBalance(username: Sexy, money: -1),
## ])
## After: ListUserBalance(listModel: [
## UserBalance(username: Mitsuya, money: 10),
## UserBalance(username: Hook, money: 7),
## UserBalance(username: Duramichi, money: 5),
## UserBalance(username: Jone, money: 3),
## UserBalance(username: Freddy, money: 1),
## UserBalance(username: Sexy, money: -1),
## ])
## After(Two): ListUserBalance(listModel: [
## UserBalance(username: Duramichi, money: 15),
## UserBalance(username: Mitsuya, money: 10),
## UserBalance(username: Hook, money: 7),
## UserBalance(username: Jone, money: 3),
## UserBalance(username: Freddy, money: 1),
## UserBalance(username: Sexy, money: -1),
## ])
## After(Three): ListUserBalance(listModel: [
## UserBalance(username: Duramichi, money: 15),
## UserBalance(username: Hook, money: 7),
## UserBalance(username: Jone, money: 3),
## UserBalance(username: Freddy, money: 1),
## UserBalance(username: Sexy, money: -1),
## ])
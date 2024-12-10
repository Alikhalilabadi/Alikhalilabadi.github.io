from __future__ import annotations
from state_machine import (State, Event, acts_as_state_machine, after, before, InvalidStateTransition)

@acts_as_state_machine
class OrderProcess:
    checkout = State(initial=True)
    select_flavor = State()
    placed_order = State()
    preparing_order = State()
    making_order = State()
    ready_for_pickup = State()
    completed_order = State()

    select_flavor_event = Event(from_states=checkout, to_state=select_flavor)
    check_inventory_event = Event(from_states=select_flavor, to_state=placed_order)
    prepare_order_event = Event(from_states=placed_order, to_state=preparing_order)
    make_ice_cream_event = Event(from_states=preparing_order, to_state=making_order)
    finish_ice_cream_event = Event(from_states=making_order, to_state=ready_for_pickup)
    pickup_order_event = Event(from_states=ready_for_pickup, to_state=completed_order)
    cancel_order_event = Event(from_states=(select_flavor, placed_order), to_state=checkout)

    def __init__(self, store: IceCreamStore) -> None:
        self.store = store

    @after("select_flavor_event")
    def after_select_flavor(self):
        print("Ready to select flavor.")

    @before("check_inventory_event")
    def before_check_inventory(self):
        print("Checking inventory...")
        return self.store.is_enough_inventory()

    @after("check_inventory_event")
    def after_check_inventory(self):
        print("Order placed.")

class IceCreamStore:
    def __init__(self) -> None:
        self._state = OrderProcess(self)
        self._selected_flavor: str = None
        self._selected_size: str = None
        self._inventory = {"Vanilla": 5, "Chocolate": 2, "Strawberry": 1}
        self._recipes = {"large": 1, "medium": 0.5, "small": 0.25}

    def is_enough_inventory(self) -> bool:
        required_recipe_size = self._recipes.get(self._selected_size, 0)
        if self._inventory.get(self._selected_flavor, 0) >= required_recipe_size:
            return True
        else:
            return False

    def select_flavor(self, flavor, size):
        try:
            self._state.select_flavor_event()
            self._selected_flavor = flavor
            self._selected_size = size
            print(f"Selected flavor: {self._selected_flavor}, Size: {self._selected_size}")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

    def check_inventory(self, flavor, size):
        self._selected_flavor = flavor
        self._selected_size = size
        try:
            self._state.check_inventory_event()
            required_recipe_size = self._recipes.get(self._selected_size, 0)
            if self._inventory.get(self._selected_flavor, 0) >= required_recipe_size:
                self._inventory[self._selected_flavor] -= required_recipe_size
                print(f"Order placed! Remaining {self._selected_flavor} inventory: {self._inventory[self._selected_flavor]} lbs.")
            else:
                print("Insufficient inventory. Order could not be placed.")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

    def prepare_order(self):
        try:
            self._state.prepare_order_event()
            print("Preparing the order...")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

    def make_ice_cream(self):
        try:
            self._state.make_ice_cream_event()
            print("Making the ice cream...")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

    def finish_ice_cream(self):
        try:
            self._state.finish_ice_cream_event()
            print("Ice cream is ready for pickup.")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

    def pickup_order(self):
        try:
            self._state.pickup_order_event()
            print("Order completed. Enjoy your ice cream!")
        except InvalidStateTransition as err:
            print(f"Error: {err}")

def show_menu():
    print("\n=== MENU ===")
    print("1. Select Flavor")
    print("2. Place Order (Check Inventory)")
    print("3. Prepare Order")
    print("4. Make Ice Cream")
    print("5. Finish Ice Cream")
    print("6. Pickup Order")
    print("9. Exit")

def main():
    store = IceCreamStore()
    while True:
        show_menu()
        try:
            option = int(input("Enter your option: "))
            if option == 1:
                flavor = input("Select your flavor (Vanilla, Chocolate, Strawberry): ")
                size = input("Select size (large, medium, small): ")
                store.select_flavor(flavor, size)
            elif option == 2:
                store.check_inventory(store._selected_flavor, store._selected_size)
            elif option == 3:
                store.prepare_order()
            elif option == 4:
                store.make_ice_cream()
            elif option == 5:
                store.finish_ice_cream()
            elif option == 6:
                store.pickup_order()
            elif option == 9:
                print("Exiting the program.")
                break
            else:
                print("Invalid option. Try again.")
        except InvalidStateTransition as err:
            print(f"Could not perform {option} in {store._state.current_state} state")
        except ValueError:
            print("Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()

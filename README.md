# FoodShare

## Questions/Concerns
### 1. Where to implement security checks in database?
### 2. How to Transaction-Donate if an item doesn't exist in a pantry's inventory?
#### Solution: remove not null constraint on item_id in transaction.
When a request to donate is made, make the transaction with the status 'pending' and item_id Null.
When it is approved of, create the inventory_item, update the inventory and transaction.

### 3. Should Managers be able to control who joins their pantry?

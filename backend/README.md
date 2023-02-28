# User Stories - INCOMPLETE

# A. Shoppers

## 1. Browse New Pantries
        A. view a list of pantries with location in menu
            ?. add a feature to sort by location?
                1. server side filter for by address
                2. OR database side query against more specific location fields

        B. select a pantry from menu
            i.  view the pantry's inventory
            ii. join the pantry
            
        C. view pantry's inventory in submenu
            i. create transaction request

        D. return to pantry browser
## 2. Browse "My Pantries"
        A. Same as 1 except it's only a list of pantries
            associated with the shopper in pantry_shopper

        B. Toggle nofiticaitons on/off for any given pantry

## 3. Create a Transaction - Receive Items

## 4. Create a Transaction - Donate Items
        * From pantry menu
        A. select either 'donate' action

        B. get user input data for transaction and inventory_item
            i.  Pre-Approval
                1. set status to 'pending'
                2. set item_id to NEW entry in inventory_item

## 6. Turn notifications on/off


# B. Managers

## 1. Everything from Shoppers

## 2. Create a Pantry
        ?. Should Manager-Pantry be One-to-One
## 3. Manually Edit their Pantry's Inventory

## 4. Respond to Transaction Request
        A. ???        

        B. update tables following manager-response
            i.  Approval
                1. set status to 'approved'
                2. use pantry_id, item_id to CREATE entry in inventory
            ii. Disapproval
                1. set status to 'disapproved'
                2. use item_id to DROP entry from inventory_item
# C. Any User
## 1. Login
## 2. Logout
## 3. Create Account
## 4. Delete Account

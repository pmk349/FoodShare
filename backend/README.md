# Functional Requirments (FR)

       1. The ability for shoppers to make requests to receive from or donate to pantries.
       2. The ability for managers to create pantries.
       3. The ability for managers to approve or deny shoppers’ requests.
       4. The ability for shoppers to view a pantry’s inventory.
       5. The ability for a manager to view the transaction history of their pantry.
       6. The ability for shoppers to silence notifications from a particular pantry.
       7. The ability to post an image of an item after donation/reception.
       8. The ability to create an account.
       9. The ability for managers to manually alter the inventory of their pantry.


# User Stories - INCOMPLETE

# A. Any User

## 1. Browse New Pantries
        A. view a list of pantries with location in menu
            ?. add a feature to sort by location?
                1. server side filter for by address
                2. OR database side query against more specific location fields

        B. select a pantry from menu
            i.  view the pantry's inventory
            ii. join the pantry
            
        C. view pantry's inventory in submenu (FR 4)
            i. create transaction request

        D. return to pantry browser
## 2. Browse "My Pantries"
        A. Same as 1 except it's only a list of pantries
            associated with the shopper in pantry_shopper

        B. Toggle nofiticaitons on/off for any given pantry (FR 6)

## 3. Create a Transaction - Receive Items (FR 1)

## 4. Create a Transaction - Donate Items (FR 1)
        * From pantry menu
        A. select 'donate' action

        B. get user input data for transaction + image (FR 7)
             * a new inventory_item is created
            i. Pre-Approval
                1. set status to 'pending'
                2. set item_id to NEW entry in inventory_item
## 5. Login
## 6. Logout
## 7. Create Account (FR 8)
## 8. Delete Account

# B. Managers

## 1. Everything from Shoppers

## 2. Create a Pantry (FR 2)
        ?. Should Manager-Pantry be One-to-One
    

## 3. Manually Edit their Pantry's Inventory (FR 9)

## 4. Respond to Transaction Request
        * when a shopper creates a transaction, 
            the API should also create a notification
            to the pantry manager

        A. send notification following request
            i. get pantry manager email
            ii. create email(?) with transaction info
                aka. templated html file
            iii. send email 

        B. update tables following manager-response (FR 3)
            i.  Approval
                1. set status to 'approved'
                2. use pantry_id, item_id to CREATE entry in inventory
            ii. Disapproval
                1. set status to 'disapproved'
                2. use item_id to DROP entry from inventory_item

## 5. View your Pantry's Transaction History (FR 5)

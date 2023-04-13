# FoodShare

# Frontend-Backend Integration

# Manager only 
### Tab 1: Manager Dashboard
    1. Pantries Managed
        inputs: managerID
        outputs (INT): # of pantries managed

    2. Number of Students Helped
        inputs: managerID
        outputs (INT): shopper count, for all pantries managed by managerID

    3. Number of Total Transactions
        inputs: managerID
        outputs (INT): transaction count, for all pantries managed by managerID

    4. Your Pantries
        inputs: managerID
        outputs (TABLE w/ BUTTONS): pantry name, addr, manager name, inspectButton

    5. Create Pantry
        inputs: name, street, city, state, zip
        


## Tab 2: Inventories
    1. Inventory Display
        inputs: managerID   
        output (TABLE): pantry name, item type, quantity, expration date, summary, image 

    2. Add Item
        inputs: item type, quantity, expration date, summary, image
    
    3. Remove Item
        inputs: item_id
        * Need a way to select pantry and item from pantry

## Tab 3: Transaction History and Approval
    1. Transaction History
        inputs: managerID   
        output (TABLE): pantry name, shopper name, time, donate or receive, item_type, quantity, status
       
    2. Pending Transactions (Approve, Deny buttons)
        inputs: managerID   
        output (TABLE w/ BUTTONS): pantry name, shopper name, time, donate or receive, item_type, quantity, approveButton, denyButton
       

# Shopper Dashboard (manager view too)
## Tab 4: Pantry Broswer
    1. All Pantries
        ouput (TABLE w/ BUTTONS): : pantry name, addr, manager name, inspectButton, joinPantryButton

## Tab 5: Transaction Donate/ Recieve
    2. Some way to select a pantry, display its inventory, make a transaction
        NOTE: transaction logic differs depending on RECEIVE or DONATE

        Displaying the Inventory of a Pantry:
            inputs: managerID   
            output (TABLE): pantry name, item type, quantity, expration date, summary, image 

        Make a Transaction-Receive:
            inputs: shopper id , pantry id , item id (ideally these 3 are gotten via some user selection, i.e. they've selected this item somehow),
                    quantity, summary, anonymousToggleOption
  
        Make a Transaction-Donation:
            inputs: shopper id, pantry id, item id (the user has to create this item, same way Managers can create items),
                    quantity, summary, anonymousToggleOption

## Tab 6: My Pantries
    1. Same as 4, but not all pantries.

## Initial Project Code

# Backend
## How To Run
### To run the backend
    1. make sure database.py line 7 is correct
        a. SQLALCHEMY_DATABASE_URL = "postgresql://USERNAME:PASSWORD@localhost/DATABASE"
    2. navigate to backend/main.py
    3. on VS Code "Run without Debugging"
    4. navigate to http://127.0.0.1:8000
    5. run api calls from /docs page to see if working

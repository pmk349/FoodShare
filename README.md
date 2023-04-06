# FoodShare

# FoodShare

# Frontend-Backend Integration

### Tab 1: Manager Dashboard
    1. Your Pantries
        inputs: managerID
        outputs (TABLE): pantry name, addr, manager name

    2. Create Pantry
        inputs: name, street, city, state, zip
        
    3. Pantries Mangers
        inputs: managerID
        outputs (INT): # of pantries managed

    4. Number of Students Helped
        inputs: managerID
        outputs (INT): shopper count, for all pantries managed by managerID

    5. Number of Total Transactions
        inputs: managerID
        outputs (INT): transaction count, for all pantries managed by managerID

## Tab 2: Inventories
    1. Inventory Display
        inputs: managerID   
        output (TABLE): pantry name, item type, quantity, expration date, summary, image 

    2. Add Item
        inputs: item type, quantity, expration date, summary, image
    
    3. Remove Item
        inputs: item_id        

## Tab 3: Transactions
    1. 

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

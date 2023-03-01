
    # 1a. view a list of pantries

-- get all pantries
select p.name, p.address
from pantry as p;


    # 1bi. view a pantry's inventory

-- get the inventory of a single pantry
select t.item_type, t.image, t.quantity, t.description, t.experation_date
from inventory as i, inventory_item as t
where i.pantry_id = {ID}
    and i.item_id = t.id;


    # 1bii. join a pantry

-- join a pantry
insert into pantry_shopper(pantry_id, shopper_id)
values ({PANTRY_ID}, {SHOPPER_ID});


    # 1ci. create a transaction request

-- create donation request


-- create  request


    # 2a. view 'my pantries'

-- get "my pantries"
select p.name, p.address
from pantry as p, pantry_shopper as s
where p.id = s.pantry_id
    and s.shopper_id = {SHOPPER_ID};


    # 2b. toggle notifications on/off

update pantry_shopper
set notifications = {NEW_STATUS}
where pantry_id = {PANTRY_ID}
    and shopper_id = {SHOPPER_ID};



-- get all pantries
select p.name, p.address
from pantry as p;

-- get "my pantries"
select p.name, p.address
from pantry as p, pantry_shopper as s
where p.id = s.pantry_id
    and s.shopper_id = {SHOPPER_ID};


-- get the inventory of a single pantry
select t.item_type, t.image, t.quantity, t.description, t.expr_date
from inventory as i, inventory_item as t
where i.pantry_id = {ID}
    and i.item_id = t.id;

-- join a pantry
insert into pantry_shopper(pantry_id, shopper_id)
values ({PANTRY_ID}, {SHOPPER_ID});

-- create transaction


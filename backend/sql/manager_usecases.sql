

-- create pantry
insert into pantry(id, name, manager_id, address)
values ({ID},{NAME},{MANAGER_ID},{ADDRESS});

-- manually edit pantry item
-- note 1: this query is dynamically generated depending
--         on the user inputs. If an input is Null, it
--         should NOT be included in the query.
-- note 2: there's an exists() check to see if the
--         requester's id is the manager of the pantry
--         in which the item is located.
update inventory_item as i
set i.quantity = {QUANTITY}, i.expration_date = {EXPRATION_DATE},
    i.description = {DESCRIPTION}, i.image = {IMAGE}

where i.id = {INV_ITEM_ID}
  and exists(
    select *
    from inventory as n, pantry as p
    where n.item_id = i.id
        and n.pantry_id = p.id
        and p.manager_id = {MANAGER_ID};
);

-- update transaction status
update transaction as t
set request_status='{new_status}'

where id={transaction_id}
  and exists(
    select *
    from pantry as p
    where t.pantry_id = i.id
        and p.manager_id = {MANAGER_ID};
);
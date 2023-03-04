


    # 2. create a pantry

-- create pantry
insert into pantry(id, name, manager_id, address)
values ({ID},{NAME},{MANAGER_ID},{ADDRESS});


    # 3. manually update a pantry's inventory

-- manually edit pantry item, quantity cannot = 0
-- note 1: this query is dynamically generated depending
--         on the user inputs. If an input is Null, it
--         should NOT be included in the query.
--         DO NOT JUST TEMPLATE WITH NULL -- that will cause integrity issues

-- note 2: there's an exists() check to see if the
--         requester's id is the manager of the pantry
--         in which the item is located.

update inventory_item as i
set i.quantity = {QUANTITY},
    i.expration_date = {EXPRATION_DATE},
    i.description = {DESCRIPTION},
    i.image = {IMAGE}
where
    i.id = {INV_ITEM_ID}
  and exists(
    select *
    from inventory as n, pantry as p
    where n.item_id = i.id
        and n.pantry_id = p.id
        and p.manager_id = {MANAGER_ID};
);

-- delete an item from the inventory

delete from inventory
where pantry_id = {PANTRY_ID}
  and item_id = {ITEM_ID};

delete from inventory_item
where id = {ITEM_ID};

-- add an item to the inventory

insert into inventory_item(id, item_type, quantity, expiration_date, summary, image) values
  ({ITEM_ID}, '{ITEM_TYPE}', {QUANTITY}, {EXPIRATION_DATE}, '{SUMMARY}', {IMAGE});

insert into inventory(pantry_id, item_id) values
  ({PANTRY_ID}, {ITEM_ID});


    # 4. respond  to transaction request

-- update transaction status
update transaction_request as t
set request_status='{new_status}'
where id={transaction_id}
  and exists(
    select *
    from pantry as p
    where t.pantry_id = i.id
        and p.manager_id = {MANAGER_ID}
);

    # 5. view transaction history

-- get transaction history
select
	(case
    when t.anonymous then 'anonymous shopper'
    when not t.anonymous then a.name
	end) as shopper, t.request_time, t.request_action, t.request_status, t.summary, t.quantity
from transaction_request as t, pantry as p, account as a
where t.pantry_id = p.id
  and t.shopper_id = a.id
  and p.manager_id = {MANAGER_ID}


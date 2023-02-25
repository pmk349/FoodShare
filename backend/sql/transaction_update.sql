




-- update transaction request status
update transaction as t
set t.request_status = {STATUS};

-- update inventory following approval
using (
select *
from transaction
where id =  {TRANSACTION_ID}
      ) as T, -- TRANSACTION

using (
select *
from inventory_item
where T.item_id = id
      ) as NI, -- NEW ITEM
on



-- update inventory following denial

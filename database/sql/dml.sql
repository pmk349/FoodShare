
-- SAMPLE DATA for testing/dev purposes

insert into account(id, name, email, password, account_type) values
    (1,'alex kowalczyk','alex@gmail.com','7c6a180b36896a0a8c02787eeafb0e4c','shopper'),
    (2,'bob smith','bob@gmail.com','6cb75f652a9b52798eb6cf2201057c73','shopper'),
    (3,'cole phrompan','cole@gmail.com','819b0643d6b89dc9b579fdfc9094f28e','shopper'),
    (4,'daisy mulenga','daisy@gmail.com','34cc93ece0ba9e3f6f235d4af979b16c','manager'),
    (5,'emily lu','emily@gmail.com','db0edd04aaac4506f7edab03ac855d56','manager');
    

insert into pantry(id, name, manager_id, address) values
    (1, 'food4everyone', 4, '55 Clark St, Brooklyn, NY 11201'),
    (2, 'food4none', 5, '101 Johnson St, Brooklyn, NY 11201');
    (3, 'coralpantry', 4, '129 Third Ave, New York, NY 10003' )

insert into pantry_shopper(pantry_id, shopper_id, notifications) values
    (1,1,FALSE),
    (1,2,TRUE),
    (1,3,FALSE),
    (1,5,FALSE),
    (2,1,TRUE),
    (2,2,FALSE),
    (2,3,TRUE);

insert into inventory_item(id, item_type, quantity, expiration_date, summary, image) values
    (1, 'beans', 3, cast('2024-02-26'), '12oz bag of dried pinto beans', Null),
    (2, 'bananas', 6, cast('2023-04-22'), 'bunches of bananas', Null),
    (3, 'apples', 5, cast('2023-02-22' ), 'individual apples', Null),
    (4, 'apples', 10, cast('2023-04-22'), 'new apples to donate', Null);
    (5, 'bread', 10, cast('2023-06-08'), 'two five packs of brioche', Null);
    (6, 'cheerios', 2, cast('2023-11-08'), 'extra cereal boxes', Null);
    (7, 'corn', 1, cast('2024-04-10'), 'can of corn', Null);
    (8, 'pasta', 4, cast('2023-08-12'), '4 500g packs of linguini', Null);
    (9, 'cornflakes', 2, cast('2024-04-12'), 'box of cornflakes', Null);


insert into inventory(pantry_id, item_id) values
    (1,1),
    (1,2),
    (2,3),
    (2,4),
    (3,5),
    (1,6),
    (3,7),
    (3,8),
    (2,9);


insert into transaction_request(id, shopper_id, pantry_id, item_id, request_time,
                        request_status, request_action, quantity, summary, anonymous) values
    (1, 3, 1, 1, cast('2023-02-26 12:30:00'), 'approved', 'donate', 3, 'donating 12oz bag of dried pinto beans', False),            
    
    (2, 3, 1, 1, cast('2023-02-26 12:30:00'), 'approved', 'receive', 1, 'requesting beans, please', True),
    (3, 2, 1, 1, cast('2023-02-26 12:30:00'), 'denied', 'receive', 6, 'requesting all the beans, please', True),

    (4, 2, 1, 2, cast('2023-03-02 10:30:00'), 'approved', 'donate', 6, 'donating bananas', True),
    (5, 1, 2, 3, cast('2023-03-12 10:45:00'), 'approved', 'donate', 5, 'donating apples', False),
    (6, 1, 2, 4, cast('2023-03-13 10:45:00'), 'approved', 'donate', 10, 'donating apples', False),

    (7, 5, 2, 3, cast('2023-03-12 3:00:00'), 'approved', 'receive', 5, 'requesting apples', False),
    (8, 5, 2, 4, cast('2023-03-13 12:30:00'), 'denied', 'receive', 10, 'requesting apples', False);

    (9, 4, 3, 5, cast('2023-04-08 13:00:00'), 'approved', 'donate', 10, 'donating brioche bread', False),
    (10, 3, 3, 5, cast('2023-04-08 14:00:00'), 'pending', 'receive', 5, 'requesting brioche bread', False),
    (11, 5, 3, 5, cast('2023-04-08 17:00:00'), 'denied', 'receive', 10, 'requesting all the brioche bread', False),

    (12, 3, 1, 6, cast('2023-04-08 13:00:00'), 'approved', 'donate', 2, 'donating 2 cheerios boxes', True),
    (13, 1, 3, 7, cast('2023-04-10 09:15:00'), 'approved', 'donate', 1, 'donating a can of corn', False),

    (14, 4, 3, 8, cast('2023-04-10 11:30:00'), 'approved', 'donate', 4, 'donating 4 packs of pasta', False),
    (15, 5, 2, 9, cast('2023-04-12 13:00:00'), 'approved', 'donate', 2, 'donating a box of cereal', False),

    (16, 1, 1, 6, cast('2023-04-12 14:00:00'), 'pending', 'receive', 2, 'requesting 2 cheerios', False),
    (17, 5, 3, 8, cast('2023-04-14 12:00:00'), 'approved', 'receive', 1, 'requesting a pack of pasta', True),
    (18, 5, 3, 8, cast('2023-04-16 12:00:00'), 'pending', 'receive', 2, 'requesting 2 packs of pasta', True),
    (19, 2, 2, 9, cast('2023-04-17 10:30:00'), 'denied', 'receive', 2, 'requesting 2 boxes of cornflakes', False),

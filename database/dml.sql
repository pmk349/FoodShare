
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

insert into pantry_shopper(pantry_id, shopper_id, notifications) values
    (1,1,FALSE),
    (1,2,TRUE),
    (1,3,FALSE),
    (1,5,FALSE),
    (2,1,TRUE),
    (2,2,FALSE),
    (2,3,TRUE);


insert into inventory_item(id, item_type, quantity, expiration_date, summary, image) values
    (1, 'beans', 3, cast('2024-02-26' as date), '12oz bag of dried pinto beans', Null),
    (2, 'bananas', 6, cast('2023-03-02' as date), 'bunches of bananas', Null),
    (3, 'apples', 5, cast('2023-03-13' as date), 'individual apples', Null),
    (4, 'apples', 10, cast('2023-03-12' as date), 'new apples to donate', Null);




insert into account(id, email, password, acc_type) values
    (1,'alex@gmail.com','7c6a180b36896a0a8c02787eeafb0e4c','shopper'),
    (2,'bob@gmail.com','6cb75f652a9b52798eb6cf2201057c73','shopper'),
    (3,'cole@gmail.com','819b0643d6b89dc9b579fdfc9094f28e','shopper'),
    (4,'daisy@gmail.com','34cc93ece0ba9e3f6f235d4af979b16c','manager'),
    (5,'emily@gmail.com','db0edd04aaac4506f7edab03ac855d56','manager');


insert into pantry(id, name, manager_id) values
    (1, 'food4everyone', 4),
    (2, 'food4none', 5);

insert into pantry_shopper(pantry_id, shopper_id) values
    (1,1),
    (1,2),
    (1,3),
    (1,5),
    (2,1),
    (2,2),
    (2,3);

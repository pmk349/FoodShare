import psycopg2
def create_foodshare_db():
    try:

        # Connect to database.
        conn = psycopg2.connect(host='localhost', database='foodshare_db',
                                    user='postgres', password='19065RA2y') # change to user information

        conn.autocommit = True
        cursor = conn.cursor()

    except psycopg2.DatabaseError as e:

        # Confirm unsuccessful connection and stop program execution.
        conn = psycopg2.connect(host = 'localhost', user = 'postgres', password = '19065RA2y')
        conn.autocommit = True
        cursor = conn.cursor()
        name = "foodshare_db"


        cursor.execute("CREATE database "+name+"")

        conn = psycopg2.connect(host = 'localhost', database = 'foodshare_db', user = 'postgres', password = '19065RA2y')

        cursor = conn.cursor()

        account = '''create table account(
            id          bigint not null,
            name        varchar(20) not null unique,
            email       varchar(20) not null unique,
            password    varchar(40) not null,
            acc_type    varchar(10) not null,

            primary key(id),    
            check(acc_type='manager' or acc_type='shopper')
        );'''

        pantry = '''create table pantry(
            id          bigint not null,
            name    varchar(40) not null,
            manager_id  bigint not null,
            address  varchar(40) not null,

            primary key(id),
            foreign key(manager_id) references account(id)
        );'''

        pantry_shopper = '''create table pantry_shopper(
            pantry_id     bigint not null,
            shopper_id    bigint not null,
            notifications boolean not null,
            primary key(pantry_id, shopper_id),
            foreign key(pantry_id) references pantry(id),
            foreign key(shopper_id) references account(id)
        );'''

        inventory_item = '''create table inventory_item(
            id          bigint not null,
            item_type   varchar(20) not null,
            quantity    int not null,
            expiration_date date,
            description     varchar(200),
            image           bytea,

            primary key(id),
            check(quantity>=0)
        );'''

        inventory = '''create table inventory(
            pantry_id   bigint not null,
            item_id     bigint not null,

            primary key(pantry_id, item_id),
            foreign key(item_id) references inventory_item(id)
        );'''

        transaction = '''create table transaction(
            id          bigint not null,
            shopper_id  bigint not null,
            pantry_id   bigint not null,
            item_id     bigint,
            request_time    timestamp not null,
            request_status  varchar(10) not null,
            request_action  varchar(10) not null,
            quantity        int not null,
            description     varchar(400) not null,

            primary key(id),
            foreign key(shopper_id) references account(id),
            foreign key(pantry_id, item_id) references inventory(pantry_id,item_id),
            check(request_status='pending'
                or request_status='approved'
                or request_status='denied'
            ),
            check(request_action='receive'
                or request_action='donate'
            ),
            check(quantity>0)
        );'''

        cursor.execute(account)
        conn.commit()

        cursor.execute(pantry)
        conn.commit()

        cursor.execute(pantry_shopper)
        conn.commit()

        cursor.execute(inventory_item)
        conn.commit()

        cursor.execute(inventory)
        conn.commit()

        cursor.execute(transaction)
        conn.commit()


    conn.close()

if __name__ == "__main__":
    create_foodshare_db()
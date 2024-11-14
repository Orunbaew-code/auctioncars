# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CopartCleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        intValues = ['Mileage', 'Year']
        for intValue in intValues:
            value = adapter.get(intValue)
            value = value[0].strip()
            adapter[intValue] = int(value)

        price_keys = ['Buy_now', 'Fees', 'Cur_bid']

        for price_key in price_keys:
            value = adapter.get(price_key)
            if value and value[0] is not None:
                value = value[0].replace('$', '')
                value = ''.join(filter(str.isdigit, value))  # Remove non-numeric characters
                if value:
                    adapter[price_key] = float(value)
                else:
                    adapter[price_key] = 0
            else:
                adapter[price_key] = 0

        return item
    
class SaveToMySQLPipeline:
    
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host = '167.88.170.180',
                user = 'postgres',
                password = 'Asadbek1505#',
                database = 'cars',
            )
            self.cur = self.conn.cursor()
            self.conn.autocommit = True
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)


        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS clean_cars(
        id serial PRIMARY KEY,
        Title text,
        Make VARCHAR(255),
        Model VARCHAR(255),
        Year INTEGER,
        Mileage INTEGER,
        Exterior VARCHAR(255),
        Interior VARCHAR(255),
        Drive_train VARCHAR(255),
        Engine VARCHAR(255),
        Transmission VARCHAR(255),
        Sale_doc VARCHAR(255),
        carKeys VARCHAR(255),
        Buy_now DECIMAL,
        Fees DECIMAL,
        Cur_bid DECIMAL,
        Auction VARCHAR(255),
        End_date VARCHAR(255)
            )
        """)

        self.cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'old_cars')")
        result = self.cur.fetchone()[0]
        if result:
            self.cur.execute("DROP TABLE old_cars")
        
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'clean_cars')")
        result = self.cur.fetchone()[0]
        if result:
            self.cur.execute("CREATE TABLE old_cars AS SELECT * FROM clean_cars")
            self.cur.execute("TRUNCATE TABLE clean_cars")


    def process_item(self, item, spider):
        self.cur.execute("""INSERT INTO clean_cars (            
            Title, Make, Model, Year, Mileage, Exterior, Interior, Drive_train, Engine, Transmission, Sale_doc, carKeys, Buy_now, Fees, Cur_bid, Auction, End_date
            ) values (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s 
            )""", (
            item["Title"][0],
            item["Make"][0],
            item["Model"][0],
            item["Year"],
            item["Mileage"],
            item["Exterior"][0],
            item["Interior"][0],
            item["Drive_train"][0],
            item["Engine"][0],
            item["Transmission"][0],
            item["Sale_doc"][0],
            item["Keys"][0],
            item["Buy_now"],
            item["Fees"],
            item["Cur_bid"],
            item["Auction"][0],
            item["End_date"]
         ))
        
        return item
        
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

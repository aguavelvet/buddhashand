DROP TABLE PRODUCT;

CREATE TABLE IF NOT EXISTS PRODUCT (
    ID int(10) NOT NULL auto_increment,
    ProductType varchar(128) NOT NULL,
    Product varchar(128) NOT NULL,
    Price decimal(15,2) NOT NULL,
    PRIMARY KEY(ID)
);


INSERT INTO PRODUCT (ProductType,Product,Price) values ( 'fruit', 'apple',10);
INSERT INTO PRODUCT (ProductType,Product,Price) values ( 'fruit', 'orange',15);
INSERT INTO PRODUCT (ProductType,Product,Price) values ( 'fruit', 'pear',  8);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'fruit', 'cherry', 15);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'fruit', 'banana', 5);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'vegetable', 'broccoli' , 10);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'vegetable', 'cauliflower', 10);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'vegetable', 'green onions', 3);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'vegetable', 'potato', 4);
INSERT INTO PRODUCT (ProductType,Product,Price) values  ( 'vegetable', 'tomato', 6);

commit;


-- Create the database
CREATE DATABASE chocolates;
USE chocolates;

-- Create the chocolates table
CREATE TABLE chocolates (
    chocolate_id INT AUTO_INCREMENT PRIMARY KEY,
    brand ENUM('Lindt', 'Godiva', 'Hershey', 'Cadbury') NOT NULL,
    flavor ENUM('Milk Chocolate', 'Dark Chocolate', 'White Chocolate', 'Mint Chocolate') NOT NULL,
    weight ENUM('50g', '100g', '150g', '200g') NOT NULL,
    price INT CHECK (price BETWEEN 1 AND 20),
    stock_quantity INT NOT NULL,
    UNIQUE KEY brand_flavor_weight (brand, flavor, weight)
);

-- Create the discounts table
CREATE TABLE discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    chocolate_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (chocolate_id) REFERENCES chocolates(chocolate_id)
);

-- Create a stored procedure to populate the chocolates table
DELIMITER $$
CREATE PROCEDURE PopulateChocolates()
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE max_records INT DEFAULT 100;
    DECLARE brand ENUM('Lindt', 'Godiva', 'Hershey', 'Cadbury');
    DECLARE flavor ENUM('Milk Chocolate', 'Dark Chocolate', 'White Chocolate', 'Mint Chocolate');
    DECLARE weight ENUM('50g', '100g', '150g', '200g');
    DECLARE price INT;
    DECLARE stock INT;

    -- Seed the random number generator
    SET SESSION rand_seed1 = UNIX_TIMESTAMP();

    WHILE counter < max_records DO
        -- Generate random values
        SET brand = ELT(FLOOR(1 + RAND() * 4), 'Lindt', 'Godiva', 'Hershey', 'Cadbury');
        SET flavor = ELT(FLOOR(1 + RAND() * 4), 'Milk Chocolate', 'Dark Chocolate', 'White Chocolate', 'Mint Chocolate');
        SET weight = ELT(FLOOR(1 + RAND() * 4), '50g', '100g', '150g', '200g');
        SET price = FLOOR(1 + RAND() * 20);
        SET stock = FLOOR(5 + RAND() * 95);

        -- Attempt to insert a new record
        -- Duplicate brand, flavor, weight combinations will be ignored due to the unique constraint
        BEGIN
            DECLARE CONTINUE HANDLER FOR 1062 BEGIN END;  -- Handle duplicate key error
            INSERT INTO chocolates (brand, flavor, weight, price, stock_quantity)
            VALUES (brand, flavor, weight, price, stock);
            SET counter = counter + 1;
        END;
    END WHILE;
END$$
DELIMITER ;

-- Call the stored procedure to populate the chocolates table
CALL PopulateChocolates();

-- Insert records into the discounts table
INSERT INTO discounts (chocolate_id, pct_discount)
VALUES
(1, 10.00),
(2, 15.00),
(3, 20.00),
(4, 5.00),
(5, 25.00)
-- Add more records as needed
;
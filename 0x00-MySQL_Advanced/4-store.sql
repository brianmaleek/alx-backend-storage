-- SQL script creates a trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.

DELIMITER //
CREATE TRIGGER decrease_quantity AFTER INSERT ON orders FOR EACH ROW
BEGIN
    DECLARE item_quantity INT;

    -- Get current quantity of the item
    SELECT quantity INTO item_quantity FROM items WHERE name = NEW.item_name;

    -- Update quantity by subtracting the number of items in the order
    UPDATE items SET quantity = item_quantity - NEW.number WHERE name = NEW.item_name;
END;
//
DELIMITER ;

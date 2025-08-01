-- Create a new schema for the supply chain
CREATE SCHEMA IF NOT EXISTS supply_chain;

-- Create the supplier table
CREATE TABLE supply_chain.supplier (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL
);

-- Create the parts table
CREATE TABLE supply_chain.parts (
    part_id SERIAL PRIMARY KEY,
    part_name VARCHAR(255) NOT NULL
);

-- Create the supplies table (join table)
CREATE TABLE supply_chain.supplies (
    supply_id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES supply_chain.supplier (supplier_id),
    FOREIGN KEY (part_id) REFERENCES supply_chain.parts (part_id)
);
--รอถามพี่ว่าต้องทำไหม ถ้าสร้างตารางใน pgadmin ไปแล้ว
CREATE TABLE customer(
    customer_code character varing(10),
    name character varing(100),
    address character varing(100),
    credit_limit numeric,
    country character varing(20),
    PRIMARY KEY (customer_code)
)

CREATE TABLE invoice(
    invoice_no character varing(10),
    date date,
    customer_code character varing(10),
    due_date date,
    total numeric(18,2),
    vat numeric(18,2),
    amount_due numeric(18,2),
    PRIMARY KEY (invoice_no),
    CONSTRAINT fkey_customer_code FOREIGN KEY (customer_code)
        REFERENCES public.customer (customer_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE invoice_line_item(
    invoice_no character varying(10),
    item_no integer,
    product_code character varying(10),
    quantity integer,
    unit_price numeric(18,2),
    extend_price numeric(18,2),
    PRIMARY KEY (invoice_no, item_no),
    CONSTRAINT fkey_product_code FOREIGN KEY (product_code)
        REFERENCES public.product (code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
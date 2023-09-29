CREATE TABLE LOG(
    id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_user BIGINT NOT NULL,
    log VARCHAR(100) NOT NULL
)

CREATE TABLE TOKEN(
    id_token BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_user BIGINT NOT NULL,
    type_user varchar(1) NOT NULL,
    token varchar(50) NOT NULL,
    expiration_date DATE NOT NULL
)

CREATE TABLE LIBRARY(
    id_library BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE ADMIN(
	id_admin BIGINT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE ALUMN(
	id_alumn BIGINT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    user VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    school_group VARCHAR(10) NULL,
    carreer VARCHAR(30) NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL,
    last_preference BIGINT NULL,
    state INT NOT NULL
);
CREATE TABLE ADVICE(
    id_advice BIGINT AUTO_INCREMENT PRIMARY KEY,
	id_alumn BIGINT NOT NULL,
    message VARCHAR(1000) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE BOOK(
	id_book BIGINT AUTO_INCREMENT PRIMARY KEY,
    tittle VARCHAR(100) NOT NULL,
    id_category BIGINT NOT NULL,
    id_author BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL,
    image VARCHAR(200) NOT NULL,
    id_library BIGINT NOT NULL,
    state INT NOT NULL
);
CREATE TABLE BOOK_NOTATIONS(
	id_book_notation BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_book BIGINT NOT NULL,
    message VARCHAR(1000) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE FAVORITE(
	id_favorite BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_alumn BIGINT NOT NULL,
    id_book BIGINT NOT NULL,
    state INT NOT NULL
);
CREATE TABLE COMMENTARY(
	id_commentary BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_alumn BIGINT NOT NULL,
    id_book BIGINT NOT NULL,
    message VARCHAR(1000) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE AUTHOR(
	id_author BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE CATEGORY(
	id_category BIGINT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(120) NOT NULL,
    state INT NOT NULL
);
CREATE TABLE TRANSACTIONS(
	id_transaction BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_alumn BIGINT NOT NULL,
    id_book BIGINT NOT NULL,
    date_transaction DATE NOT NULL,
    date_deadline DATE NOT NULL,
    date_return DATE NOT NULL,
    notation VARCHAR(1000) NOT NULL,
    id_library BIGINT NOT NULL,
    state INT NOT NULL
);
CREATE TABLE RESERVES(
	id_reserve BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_alumn BIGINT NOT NULL,
    id_book BIGINT NOT NULL,
    date_pickup DATE NOT NULL,
    id_library BIGINT NOT NULL,
    state INT NOT NULL
);
CREATE TABLE `AUTHOR`(
    `id_author` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `TRANSACTIONS`(
    `id_transaction` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_alumn` BIGINT NOT NULL,
    `id_book` BIGINT NOT NULL,
    `date_transaction` DATE NOT NULL,
    `date_deadline` DATE NOT NULL,
    `date_return` DATE NOT NULL,
    `notation` VARCHAR(1000) NOT NULL,
    `id_library` BIGINT NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `RESERVES`(
    `id_reserve` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_alumn` BIGINT NOT NULL,
    `id_book` BIGINT NOT NULL,
    `date_pickup` DATE NOT NULL,
    `id_library` BIGINT NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `LIBRARY`(
    `id_library` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL,
    `address` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(10) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `ADVICE`(
    `id_advice` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_alumn` BIGINT NOT NULL,
    `message` VARCHAR(1000) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `FAVORITE`(
    `id_favorite` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_alumn` BIGINT NOT NULL,
    `id_book` BIGINT NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `BOOK_NOTATIONS`(
    `id_book_notation` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_book` BIGINT NOT NULL,
    `message` VARCHAR(1000) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `LOG`(
    `id_log` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_user` BIGINT NOT NULL,
    `log` VARCHAR(100) NOT NULL
);
CREATE TABLE `CATEGORY`(
    `id_category` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `category` VARCHAR(120) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `ALUMN`(
    `id_alumn` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `account_number` VARCHAR(20) NOT NULL,
    `user` VARCHAR(30) NOT NULL,
    `password` VARCHAR(30) NOT NULL,
    `school_group` VARCHAR(10) NULL,
    `carreer` VARCHAR(30) NULL,
    `first_name` VARCHAR(40) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `phone` VARCHAR(10) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `last_preference` BIGINT NULL,
    `state` INT NOT NULL,
    `library_id` BIGINT NOT NULL
);
CREATE TABLE `ADMIN`(
    `id_admin` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user` VARCHAR(30) NOT NULL,
    `password` VARCHAR(30) NOT NULL,
    `first_name` VARCHAR(40) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `phone` VARCHAR(10) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `state` INT NOT NULL,
    `library_id` BIGINT NOT NULL
);
CREATE TABLE `BOOK`(
    `id_book` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tittle` VARCHAR(100) NOT NULL,
    `isbn` VARCHAR(50) NOT NULL,
    `id_category` BIGINT NOT NULL,
    `id_author` BIGINT NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `image` VARCHAR(200) NOT NULL,
    `id_library` BIGINT NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `COMMENTARY`(
    `id_commentary` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_alumn` BIGINT NOT NULL,
    `id_book` BIGINT NOT NULL,
    `message` VARCHAR(1000) NOT NULL,
    `state` INT NOT NULL
);
CREATE TABLE `VERIFY_TOKEN`(
    `id_token`BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `token` VARCHAR(11) NOT NULL,
    `id_user` BIGINT NOT NULL,
    `type` INT NOT NULL
)

ALTER TABLE
    `COMMENTARY` ADD CONSTRAINT `commentary_id_alumn_foreign` FOREIGN KEY(`id_alumn`) REFERENCES `ALUMN`(`id_alumn`);
ALTER TABLE
    `ADMIN` ADD CONSTRAINT `admin_library_id_foreign` FOREIGN KEY(`library_id`) REFERENCES `LIBRARY`(`id_library`);
ALTER TABLE
    `BOOK` ADD CONSTRAINT `book_id_author_foreign` FOREIGN KEY(`id_author`) REFERENCES `AUTHOR`(`id_author`);
ALTER TABLE
    `FAVORITE` ADD CONSTRAINT `favorite_id_book_foreign` FOREIGN KEY(`id_book`) REFERENCES `BOOK`(`id_book`);
ALTER TABLE
    `TRANSACTIONS` ADD CONSTRAINT `transactions_id_alumn_foreign` FOREIGN KEY(`id_alumn`) REFERENCES `ALUMN`(`id_alumn`);
ALTER TABLE
    `BOOK_NOTATIONS` ADD CONSTRAINT `book_notations_id_book_foreign` FOREIGN KEY(`id_book`) REFERENCES `BOOK`(`id_book`);
ALTER TABLE
    `RESERVES` ADD CONSTRAINT `reserves_id_book_foreign` FOREIGN KEY(`id_book`) REFERENCES `BOOK`(`id_book`);
ALTER TABLE
    `ALUMN` ADD CONSTRAINT `alumn_library_id_foreign` FOREIGN KEY(`library_id`) REFERENCES `LIBRARY`(`id_library`);
ALTER TABLE
    `BOOK` ADD CONSTRAINT `book_id_category_foreign` FOREIGN KEY(`id_category`) REFERENCES `CATEGORY`(`id_category`);
ALTER TABLE
    `TRANSACTIONS` ADD CONSTRAINT `transactions_id_library_foreign` FOREIGN KEY(`id_library`) REFERENCES `LIBRARY`(`id_library`);
ALTER TABLE
    `COMMENTARY` ADD CONSTRAINT `commentary_id_book_foreign` FOREIGN KEY(`id_book`) REFERENCES `BOOK`(`id_book`);
ALTER TABLE
    `FAVORITE` ADD CONSTRAINT `favorite_id_alumn_foreign` FOREIGN KEY(`id_alumn`) REFERENCES `ALUMN`(`id_alumn`);
ALTER TABLE
    `RESERVES` ADD CONSTRAINT `reserves_id_alumn_foreign` FOREIGN KEY(`id_alumn`) REFERENCES `ALUMN`(`id_alumn`);
ALTER TABLE
    `BOOK` ADD CONSTRAINT `book_id_library_foreign` FOREIGN KEY(`id_library`) REFERENCES `LIBRARY`(`id_library`);
ALTER TABLE
    `TRANSACTIONS` ADD CONSTRAINT `transactions_id_book_foreign` FOREIGN KEY(`id_book`) REFERENCES `BOOK`(`id_book`);
ALTER TABLE
    `ADVICE` ADD CONSTRAINT `advice_id_alumn_foreign` FOREIGN KEY(`id_alumn`) REFERENCES `ALUMN`(`id_alumn`);
ALTER TABLE
    `RESERVES` ADD CONSTRAINT `reserves_id_library_foreign` FOREIGN KEY(`id_library`) REFERENCES `LIBRARY`(`id_library`);
CREATE TABLE `users` (
  `user_id` integer PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255) UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `image_path` text DEFAULT 'https://icons8.com/icon/ABBSjQJK83zf/user',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `categories` (
  `category_id` integer PRIMARY KEY AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL
);

CREATE TABLE `tasks` (
  `task_id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT,
  `category_id` INT,
  `task_title` VARCHAR(255) NOT NULL,
  `task_description` TEXT DEFAULT NULL,
  `task_status` VARCHAR(20) DEFAULT 'Sin Empezar',
  `date_to_end` DATE DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `tasks` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
ALTER TABLE `tasks` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);


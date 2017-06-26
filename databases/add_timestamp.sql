ALTER TABLE `shixun`.`user_booklist_opinion` 
ADD COLUMN `last_vote_time` DATETIME NULL AFTER `is_follow`,
ADD COLUMN `last_follow_time` DATETIME NULL AFTER `last_vote_time`;

ALTER TABLE `shixun`.`user_book_opinion` 
ADD COLUMN `last_vote_time` DATETIME NULL AFTER `is_follow`,
ADD COLUMN `last_follow_time` DATETIME NULL AFTER `last_vote_time`;


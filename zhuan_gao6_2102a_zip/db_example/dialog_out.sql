CREATE TABLE `dialog_out` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `key` char(128) DEFAULT '',
  `user` char(128) DEFAULT '',
  `gkey` char(255) DEFAULT '',
  `io` char(32) DEFAULT '',
  `value` varchar(2048) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_key` (`user`,`key`),
  KEY `gkey` (`gkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `dialog_out`
ADD COLUMN `duration`  float(10,6) NULL DEFAULT NULL AFTER `value`;

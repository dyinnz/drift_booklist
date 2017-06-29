-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: shixun
-- ------------------------------------------------------
-- Server version	5.7.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `ISBN` varchar(32) NOT NULL,
  `author` varchar(64) NOT NULL,
  `publisher` varchar(45) NOT NULL,
  `introduction` varchar(1024) NOT NULL,
  `cover` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (1,'book1','0001','xlm','xlm','introduction','it is cover'),(2,'book2','0002','xlm','xlm','introduction','it is cover');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_tag`
--

DROP TABLE IF EXISTS `book_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_tag` (
  `book_id` int(10) unsigned NOT NULL,
  `tag_name` varchar(16) NOT NULL,
  PRIMARY KEY (`book_id`,`tag_name`),
  KEY `fk_book_tag_2_idx` (`tag_name`),
  CONSTRAINT `fk_book_tag_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_book_tag_2` FOREIGN KEY (`tag_name`) REFERENCES `tags` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_tag`
--

LOCK TABLES `book_tag` WRITE;
/*!40000 ALTER TABLE `book_tag` DISABLE KEYS */;
INSERT INTO `book_tag` VALUES (1,'tag1'),(2,'tag2');
/*!40000 ALTER TABLE `book_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booklist`
--

DROP TABLE IF EXISTS `booklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booklist` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `introduction` varchar(256) NOT NULL,
  `cover` varchar(40) NOT NULL,
  PRIMARY KEY (`id`,`user_id`),
  KEY `fk_booklist_1_idx` (`user_id`),
  CONSTRAINT `fk_booklist_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booklist`
--

LOCK TABLES `booklist` WRITE;
/*!40000 ALTER TABLE `booklist` DISABLE KEYS */;
INSERT INTO `booklist` VALUES (1,'my favorite',1,'this is my favorite','it is cover');
/*!40000 ALTER TABLE `booklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booklist_book`
--

DROP TABLE IF EXISTS `booklist_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booklist_book` (
  `booklist_id` int(10) unsigned NOT NULL,
  `book_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`booklist_id`,`book_id`),
  KEY `fk_booklist_book_2_idx` (`book_id`),
  CONSTRAINT `fk_booklist_book_1` FOREIGN KEY (`booklist_id`) REFERENCES `booklist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_booklist_book_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booklist_book`
--

LOCK TABLES `booklist_book` WRITE;
/*!40000 ALTER TABLE `booklist_book` DISABLE KEYS */;
INSERT INTO `booklist_book` VALUES (1,1),(1,2);
/*!40000 ALTER TABLE `booklist_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booklist_tag`
--

DROP TABLE IF EXISTS `booklist_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booklist_tag` (
  `booklist_id` int(10) unsigned NOT NULL,
  `tag_name` varchar(16) NOT NULL,
  PRIMARY KEY (`booklist_id`,`tag_name`),
  KEY `fk_booklist_tag_2_idx` (`tag_name`),
  CONSTRAINT `fk_booklist_tag_1` FOREIGN KEY (`booklist_id`) REFERENCES `booklist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_booklist_tag_2` FOREIGN KEY (`tag_name`) REFERENCES `tags` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booklist_tag`
--

LOCK TABLES `booklist_tag` WRITE;
/*!40000 ALTER TABLE `booklist_tag` DISABLE KEYS */;
INSERT INTO `booklist_tag` VALUES (1,'tag1'),(1,'tag2');
/*!40000 ALTER TABLE `booklist_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friend`
--

DROP TABLE IF EXISTS `friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friend` (
  `user_id1` int(10) unsigned NOT NULL,
  `user_id2` int(10) unsigned NOT NULL,
  PRIMARY KEY (`user_id1`,`user_id2`),
  KEY `fk_friend_2_idx` (`user_id2`),
  CONSTRAINT `fk_friend_1` FOREIGN KEY (`user_id1`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_friend_2` FOREIGN KEY (`user_id2`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friend`
--

LOCK TABLES `friend` WRITE;
/*!40000 ALTER TABLE `friend` DISABLE KEYS */;
/*!40000 ALTER TABLE `friend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `name` varchar(16) NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES ('tag1'),('tag2');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `account` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `birthday` date NOT NULL,
  `introduction` varchar(45) NOT NULL DEFAULT 'No Introduction yet.',
  `gender` enum('male','female') NOT NULL,
  `pic_src` varchar(128) NOT NULL DEFAULT 'resource/pic/default.png',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_UNIQUE` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'xlm','sictiy','xlm104600','2000-01-01','No Introduction yet.','male','/static/react/small_avatar.jpg'),(2,'xlm2','sictiy','xlm104600','2000-01-01','No Introduction yet.','male','/static/react/small_avatar.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_book_opinion`
--

DROP TABLE IF EXISTS `user_book_opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_book_opinion` (
  `user_id` int(10) unsigned NOT NULL,
  `book_id` int(10) unsigned NOT NULL,
  `vote` enum('up','down','netural') NOT NULL DEFAULT 'netural',
  `is_follow` tinyint(4) NOT NULL DEFAULT '0',
  `last_vote_time` datetime DEFAULT NULL,
  `last_follow_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`book_id`),
  KEY `fk_user_book_2_idx` (`book_id`),
  CONSTRAINT `fk_user_book_op_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_book_op_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_book_opinion`
--

LOCK TABLES `user_book_opinion` WRITE;
/*!40000 ALTER TABLE `user_book_opinion` DISABLE KEYS */;
INSERT INTO `user_book_opinion` VALUES (1,1,'up',1,NULL,NULL),(1,2,'down',1,NULL,NULL),(2,1,'up',1,NULL,NULL),(2,2,'down',1,NULL,NULL);
/*!40000 ALTER TABLE `user_book_opinion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_book_remark`
--

DROP TABLE IF EXISTS `user_book_remark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_book_remark` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `book_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `remark` varchar(1024) NOT NULL,
  `remark_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_book_remark_2_idx` (`user_id`),
  KEY `fk_book_remark_1` (`book_id`),
  CONSTRAINT `fk_book_remark_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_book_remark_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_book_remark`
--

LOCK TABLES `user_book_remark` WRITE;
/*!40000 ALTER TABLE `user_book_remark` DISABLE KEYS */;
INSERT INTO `user_book_remark` VALUES (1,2,1,'good','2017-06-24 22:23:01'),(2,2,1,'good','2017-06-24 22:23:12'),(3,2,1,'good','2017-06-24 22:23:36'),(4,2,2,'good','2017-06-24 22:23:43'),(5,1,2,'good','2017-06-24 22:23:47'),(6,1,1,'good','2017-06-24 22:23:51');
/*!40000 ALTER TABLE `user_book_remark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_book_remark_opinion`
--

DROP TABLE IF EXISTS `user_book_remark_opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_book_remark_opinion` (
  `user_id` int(10) unsigned NOT NULL,
  `book_remark_id` int(10) unsigned NOT NULL,
  `vote` enum('up','down','netural') NOT NULL DEFAULT 'netural',
  `last_vote_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`book_remark_id`),
  KEY `fk_user_book_2_idx` (`book_remark_id`),
  CONSTRAINT `fk_user_book_remark_op_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_book_remark_op_2` FOREIGN KEY (`book_remark_id`) REFERENCES `user_book_remark` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_book_remark_opinion`
--

LOCK TABLES `user_book_remark_opinion` WRITE;
/*!40000 ALTER TABLE `user_book_remark_opinion` DISABLE KEYS */;
INSERT INTO `user_book_remark_opinion` VALUES (1,1,'up',NULL),(1,2,'up',NULL),(1,3,'up',NULL),(2,2,'up',NULL),(2,3,'up',NULL),(2,4,'up',NULL);
/*!40000 ALTER TABLE `user_book_remark_opinion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_booklist_opinion`
--

DROP TABLE IF EXISTS `user_booklist_opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_booklist_opinion` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `booklist_id` int(10) unsigned NOT NULL,
  `vote` enum('up','down','netural') NOT NULL DEFAULT 'netural',
  `is_follow` tinyint(4) NOT NULL DEFAULT '0',
  `last_vote_time` datetime DEFAULT NULL,
  `last_follow_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`booklist_id`),
  KEY `fk_user_booklist_2_idx` (`booklist_id`),
  CONSTRAINT `fk_user_booklist_op_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_booklist_op_2` FOREIGN KEY (`booklist_id`) REFERENCES `booklist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_booklist_opinion`
--

LOCK TABLES `user_booklist_opinion` WRITE;
/*!40000 ALTER TABLE `user_booklist_opinion` DISABLE KEYS */;
INSERT INTO `user_booklist_opinion` VALUES (1,1,'up',1,NULL,NULL),(2,1,'up',1,NULL,NULL);
/*!40000 ALTER TABLE `user_booklist_opinion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_booklist_remark`
--

DROP TABLE IF EXISTS `user_booklist_remark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_booklist_remark` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `booklist_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `remark` varchar(1024) NOT NULL,
  `remark_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_booklist_remark_2_idx` (`user_id`),
  KEY `fk_booklist_remark_1` (`booklist_id`),
  CONSTRAINT `fk_booklist_remark_1` FOREIGN KEY (`booklist_id`) REFERENCES `booklist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_booklist_remark_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_booklist_remark`
--

LOCK TABLES `user_booklist_remark` WRITE;
/*!40000 ALTER TABLE `user_booklist_remark` DISABLE KEYS */;
INSERT INTO `user_booklist_remark` VALUES (1,1,1,'good','2017-06-24 22:29:13'),(2,1,2,'good','2017-06-24 22:29:22'),(3,1,2,'good','2017-06-24 22:29:24'),(4,1,1,'good','2017-06-24 22:29:31');
/*!40000 ALTER TABLE `user_booklist_remark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_booklist_remark_opinion`
--

DROP TABLE IF EXISTS `user_booklist_remark_opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_booklist_remark_opinion` (
  `user_id` int(10) unsigned NOT NULL,
  `booklist_remark_id` int(10) unsigned NOT NULL,
  `vote` enum('up','down','netural') NOT NULL DEFAULT 'netural',
  `last_vote_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`booklist_remark_id`),
  KEY `fk_user_booklist_remark_2_idx` (`booklist_remark_id`),
  CONSTRAINT `fk_user_booklist_remark_op_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_booklist_remark_op_2` FOREIGN KEY (`booklist_remark_id`) REFERENCES `user_booklist_remark` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_booklist_remark_opinion`
--

LOCK TABLES `user_booklist_remark_opinion` WRITE;
/*!40000 ALTER TABLE `user_booklist_remark_opinion` DISABLE KEYS */;
INSERT INTO `user_booklist_remark_opinion` VALUES (1,1,'up',NULL),(2,1,'up',NULL);
/*!40000 ALTER TABLE `user_booklist_remark_opinion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_interest`
--

DROP TABLE IF EXISTS `user_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_interest` (
  `user_id` int(10) unsigned NOT NULL,
  `tag_name` varchar(16) NOT NULL,
  PRIMARY KEY (`user_id`,`tag_name`),
  KEY `fk_user_interest_2_idx` (`tag_name`),
  CONSTRAINT `fk_user_interest_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_interest_2` FOREIGN KEY (`tag_name`) REFERENCES `tags` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_interest`
--

LOCK TABLES `user_interest` WRITE;
/*!40000 ALTER TABLE `user_interest` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_interest` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-29 15:07:23

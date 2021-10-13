-- MySQL dump 10.13  Distrib 5.7.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hotelinfo_manage
-- ------------------------------------------------------
-- Server version	5.7.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'hotel_admin'),(3,'hotel_staff'),(1,'user');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `user_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_bin NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `hotel_id` int(11) DEFAULT '-1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,1,'pbkdf2_sha256$260000$oi22oFhTRNv35XyEvKXHVc$5eyEt4lvhp37xurp+tua8OuCIOmgz5R88NWDe7PoNfA=','2021-10-13 03:09:12.331702',0,'glht','123456789@qq.com',0,1,'2021-08-25 08:33:27.409081',1),(2,2,'pbkdf2_sha256$260000$ASACXsKGMhsfVAZhRuGkfz$97BIFsMqGzsB516QTb3bdkYhAoA4BbA5kwi8zb14YsE=','2021-09-06 11:27:50.344229',0,'test','',1,1,'2021-09-06 11:23:47.043828',1),(3,3,'pbkdf2_sha256$260000$Rubsbb9K5Vq3Gcy2Rjc28T$05essMdnNBNx7NdPzExoCE2QE/JTE73QcmZbJTWGo8o=','2021-10-13 03:08:05.830739',0,'customer','2230685848@qq.com',0,1,'2021-09-06 12:04:53.092656',-1),(4,4,'pbkdf2_sha256$260000$iIGN73t9o5XPLh30DUZvkp$Gno/Kj36LJG6lHInpetYM1yUVkRVX8lW+Rk/58J5L4w=','2021-10-13 03:11:51.119124',0,'user','123456789@qq.com',0,1,'2021-10-13 03:11:51.119124',-1);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_bin,
  `object_repr` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-08-10 06:40:30.340165'),(2,'auth','0001_initial','2021-08-10 06:40:36.840809'),(3,'admin','0001_initial','2021-08-10 06:40:38.346775'),(4,'admin','0002_logentry_remove_auto_add','2021-08-10 06:40:38.387667'),(5,'admin','0003_logentry_add_action_flag_choices','2021-08-10 06:40:38.430551'),(6,'contenttypes','0002_remove_content_type_name','2021-08-10 06:40:39.289225'),(7,'auth','0002_alter_permission_name_max_length','2021-08-10 06:40:39.985363'),(8,'auth','0003_alter_user_email_max_length','2021-08-10 06:40:40.086094'),(9,'auth','0004_alter_user_username_opts','2021-08-10 06:40:40.125989'),(10,'auth','0005_alter_user_last_login_null','2021-08-10 06:40:40.562818'),(11,'auth','0006_require_contenttypes_0002','2021-08-10 06:40:40.668536'),(12,'auth','0007_alter_validators_add_error_messages','2021-08-10 06:40:40.725386'),(13,'auth','0008_alter_user_username_max_length','2021-08-10 06:40:41.347719'),(14,'auth','0009_alter_user_last_name_max_length','2021-08-10 06:40:42.057821'),(15,'auth','0010_alter_group_name_max_length','2021-08-10 06:40:42.165531'),(16,'auth','0011_update_proxy_permissions','2021-08-10 06:40:42.207419'),(17,'auth','0012_alter_user_first_name_max_length','2021-08-10 06:40:42.821776'),(18,'sessions','0001_initial','2021-08-10 06:40:43.250629');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `session_data` longtext COLLATE utf8mb4_bin NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5oqzpq7eeapfswmlq13atipgaxzbqdb8','eyJ1c2VybmFtZSI6ImN1c3RvbWVyIn0:1mNFFo:-e1E0hnLL9jRfCOv8XrCL9AAHAiuTiJEBs1_qsrZHBY','2021-09-20 14:05:44.620601'),('kx8pkypnhedxzltowgnebypf5hrq8iok','eyJ1c2VybmFtZSI6ImN1c3RvbWVyIn0:1mNDyk:687IvLzwB_9HcT0peW-hwETYnntoDmqmlf1n7HoXKTA','2021-09-20 12:44:02.405651'),('m5yx8pfm11essoxnmbr8prnghx44bmu7','eyJ1c2VybmFtZSI6ImN1c3RvbWVyIn0:1mNEGF:Rly4h2Um3NxHKxDovxFqVIbCvJ03VOpvSvF_fWsN84c','2021-09-20 13:02:07.465896'),('xdag25m9nimlinqgj43baswlewgtaz0v','eyJ1c2VybmFtZSI6ImdsaHQifQ:1mTOun:e4GbykJL0_dwWzdDU9RtAUqawpE9umY8AZbsEYSWwS0','2021-10-07 13:37:29.216858');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `home_clean_date`
--

DROP TABLE IF EXISTS `home_clean_date`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_clean_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotelid` int(11) DEFAULT NULL COMMENT '酒店id',
  `homenum` int(11) DEFAULT NULL COMMENT '房间号',
  `userid` int(11) DEFAULT NULL COMMENT '打扫人',
  `clean_price` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '打扫薪资',
  `is_clean` int(11) DEFAULT '0' COMMENT '是否打扫房间，默认为0，未打扫\n',
  `clean_date` datetime DEFAULT NULL COMMENT '打扫时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `home_clean_date_id_uindex` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='房间打扫记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_clean_date`
--

LOCK TABLES `home_clean_date` WRITE;
/*!40000 ALTER TABLE `home_clean_date` DISABLE KEYS */;
/*!40000 ALTER TABLE `home_clean_date` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `home_info`
--

DROP TABLE IF EXISTS `home_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotelid` int(11) DEFAULT NULL COMMENT '酒店id',
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '房型名称',
  `price` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '房间价格',
  `datail` text COLLATE utf8mb4_bin COMMENT '房间介绍',
  `num` int(11) DEFAULT NULL COMMENT '剩余个数',
  `clean_price` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '房间打扫价格',
  `live_num` int(11) DEFAULT '0',
  `live_rate` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `home_info_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='酒店房间信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_info`
--

LOCK TABLES `home_info` WRITE;
/*!40000 ALTER TABLE `home_info` DISABLE KEYS */;
INSERT INTO `home_info` VALUES (1,1,'大床房','138','可住两个人',5,'2',1,20);
/*!40000 ALTER TABLE `home_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `home_num`
--

DROP TABLE IF EXISTS `home_num`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_num` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotelid` int(11) DEFAULT NULL COMMENT '酒店id',
  `homeid` int(11) DEFAULT NULL COMMENT '房型id',
  `num` int(11) DEFAULT NULL COMMENT '房号',
  `is_clean` int(11) DEFAULT '1' COMMENT '是否打扫，默认为1',
  `clean_user` int(11) DEFAULT NULL COMMENT '打扫人id',
  `is_live` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `home_num_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='房号信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `home_num`
--

LOCK TABLES `home_num` WRITE;
/*!40000 ALTER TABLE `home_num` DISABLE KEYS */;
INSERT INTO `home_num` VALUES (1,1,1,101,0,NULL,1);
/*!40000 ALTER TABLE `home_num` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel_info`
--

DROP TABLE IF EXISTS `hotel_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hotel_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '酒店名称\n',
  `detail` text COLLATE utf8mb4_bin COMMENT '酒店介绍',
  `open_time` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '营业时间',
  `address` text COLLATE utf8mb4_bin COMMENT '酒店地址',
  `phone` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系电话',
  `city` text COLLATE utf8mb4_bin COMMENT '酒店所在的市区',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hotel_info_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='酒店信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_info`
--

LOCK TABLES `hotel_info` WRITE;
/*!40000 ALTER TABLE `hotel_info` DISABLE KEYS */;
INSERT INTO `hotel_info` VALUES (1,'格林豪泰（临沂兰山区大学城店）','山东省临沂市兰山区临沂大学城格林豪泰酒店','全天','山东省临沂市兰山区临沂大学城','123456','山东省临沂市兰山区');
/*!40000 ALTER TABLE `hotel_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL COMMENT '关联的用户id',
  `hotelid` int(11) DEFAULT NULL COMMENT '关联的酒店id',
  `homeid` int(11) DEFAULT NULL COMMENT '房型id',
  `home_num` int(11) DEFAULT NULL COMMENT '房间号',
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '入住人信息',
  `phone` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '入住人电话',
  `intime` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '到店时间',
  `ordertime` datetime DEFAULT NULL COMMENT '下单时间',
  `ordernum` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '随机生成订单编号',
  `idcard` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '入住人身份证号',
  `check_in` int(11) DEFAULT '0' COMMENT '确认入住，默认为0',
  `outtime` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '离店时间',
  `price` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '订单支付价格',
  `days` int(11) DEFAULT NULL COMMENT '入住天数',
  `live_num` int(11) DEFAULT NULL COMMENT '入住人数',
  `is_departure` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='订单信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,3,1,1,101,'customer','12345612310','2021-09-07 11:00 - 11:30','2021-09-07 01:44:53','McbpFXYU4nTrL3iaZEPh58RQ6','1234567891230012345',1,'2021-09-08','138.0',1,1,NULL);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reset_pwd_log`
--

DROP TABLE IF EXISTS `reset_pwd_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reset_pwd_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL COMMENT '用户id',
  `resetid` text COLLATE utf8mb4_bin COMMENT '随机重置验证链接',
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reset_pwd_log_id_uindex` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reset_pwd_log`
--

LOCK TABLES `reset_pwd_log` WRITE;
/*!40000 ALTER TABLE `reset_pwd_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `reset_pwd_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_pay`
--

DROP TABLE IF EXISTS `staff_pay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_pay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL COMMENT '用户id',
  `hotelid` int(11) DEFAULT NULL COMMENT '工作酒店id',
  `base_salary` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '基础工资',
  `pay` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '结算工资',
  `datetime` datetime DEFAULT NULL COMMENT '结算时间',
  `performance` varchar(255) COLLATE utf8mb4_bin DEFAULT '0' COMMENT '绩效：打扫房间的提成',
  `clean_num` int(11) DEFAULT '0' COMMENT '打扫房间个数',
  `date_pay` datetime DEFAULT NULL COMMENT '工资月份\n',
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_pay_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='员工薪资';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_pay`
--

LOCK TABLES `staff_pay` WRITE;
/*!40000 ALTER TABLE `staff_pay` DISABLE KEYS */;
INSERT INTO `staff_pay` VALUES (1,NULL,1,'1900',NULL,NULL,NULL,NULL,'2021-09-01 00:00:00');
/*!40000 ALTER TABLE `staff_pay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户真实姓名\n',
  `phone` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '联系方式',
  `address` text COLLATE utf8mb4_bin COMMENT '员工的家庭住址\n',
  `qq` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userinfo_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户详细信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinfo`
--

LOCK TABLES `userinfo` WRITE;
/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
INSERT INTO `userinfo` VALUES (1,'谢瑞雪','1234567891',NULL,'None'),(2,'test','12345612310',NULL,NULL),(3,'customer',NULL,NULL,NULL),(4,'zgq',NULL,NULL,NULL);
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-13 11:24:49

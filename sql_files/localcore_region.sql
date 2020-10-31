-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: stdominfoservices_db
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.16.04.1

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
-- Table structure for table `localcore_region`
--

DROP TABLE IF EXISTS `localcore_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `localcore_region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `country_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `localcore_region_country_id_1aa59e46_fk_localcore_country_id` (`country_id`),
  CONSTRAINT `localcore_region_country_id_1aa59e46_fk_localcore_country_id` FOREIGN KEY (`country_id`) REFERENCES `localcore_country` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localcore_region`
--

LOCK TABLES `localcore_region` WRITE;
/*!40000 ALTER TABLE `localcore_region` DISABLE KEYS */;
INSERT INTO `localcore_region` VALUES (1,'2018-05-02 11:30:23.360952','2018-05-02 11:30:23.361073','BUL','Bas-Uele','bas-uele',NULL,1,1),(2,'2018-05-02 11:34:08.266384','2018-05-02 11:34:08.266561','KIN','Kinshasa','kinshasa',NULL,1,1),(3,'2018-05-02 11:38:41.188957','2018-05-02 11:38:41.189143','HKT','Haut-Katanga','haut-katanga',NULL,1,1),(4,'2018-05-02 11:40:11.425239','2018-05-02 11:40:11.425325','KSC','Kasai-central','kasai-central',NULL,1,1),(5,'2018-05-02 11:41:51.681126','2018-05-02 11:41:51.681310','KSO','Kasai-Oriental','kasai-oriental',NULL,1,1),(6,'2018-05-02 11:45:19.189028','2018-05-02 11:45:19.189125','LMM','Lomami','lomami',NULL,1,1),(85,'2018-09-02 23:24:22.818260','2018-09-02 23:24:22.818357','','Bas-Uele','bas-uele',NULL,1,0),(86,'2018-09-02 23:39:29.509038','2018-09-02 23:39:29.509202','','Bas-Uele','bas-uele',NULL,1,0),(87,'2018-09-02 23:39:30.179191','2018-09-02 23:39:30.179292','','Équateur','equateur',NULL,1,0),(88,'2018-09-02 23:39:31.054342','2018-09-02 23:39:31.054505','','Haut-Katanga','haut-katanga',NULL,1,0),(89,'2018-09-02 23:39:32.154391','2018-09-02 23:39:32.154532','','Haut-Lomami','haut-lomami',NULL,1,0),(90,'2018-09-02 23:39:32.664476','2018-09-02 23:39:32.664572','','Haut-Uele','haut-uele',NULL,1,0),(91,'2018-09-02 23:39:33.006322','2018-09-02 23:39:33.007349','','Ituri','ituri',NULL,1,0),(92,'2018-09-02 23:39:33.322570','2018-09-02 23:39:33.322700','','Kasaï','kasai',NULL,1,0),(93,'2018-09-02 23:39:34.150340','2018-09-02 23:39:34.150467','','Kasaï-Central','kasai-central',NULL,1,0),(94,'2018-09-02 23:39:34.200623','2018-09-02 23:39:34.200752','','Kasaï-Oriental','kasai-oriental',NULL,1,0),(95,'2018-09-02 23:39:34.842604','2018-09-02 23:39:34.842714','','Kinshasa','kinshasa',NULL,1,0),(96,'2018-09-02 23:39:36.427592','2018-09-02 23:39:36.427721','','Kongo-Central','kongo-central',NULL,1,0),(97,'2018-09-02 23:39:36.477889','2018-09-02 23:39:36.477979','','Kwango','kwango',NULL,1,0),(98,'2018-09-02 23:39:36.894642','2018-09-02 23:39:36.894753','','Kwilu','kwilu',NULL,1,0),(99,'2018-09-02 23:39:38.124909','2018-09-02 23:39:38.124999','','Lomami','lomami',NULL,1,0),(100,'2018-09-02 23:39:38.703522','2018-09-02 23:39:38.703760','','Lualaba','lualaba',NULL,1,0),(101,'2018-09-02 23:39:39.537117','2018-09-02 23:39:39.537209','','Mai-Ndombe','mai-ndombe',NULL,1,0),(102,'2018-09-02 23:39:40.418615','2018-09-02 23:39:40.418706','','Maniema','maniema',NULL,1,0),(103,'2018-09-02 23:39:41.276745','2018-09-02 23:39:41.276863','','Mongala','mongala',NULL,1,0),(104,'2018-09-02 23:39:41.538095','2018-09-02 23:39:41.538183','','Nord-Kivu','nord-kivu',NULL,1,0),(105,'2018-09-02 23:39:41.593488','2018-09-02 23:39:41.593584','','Nord-Ubangi','nord-ubangi',NULL,1,0),(106,'2018-09-02 23:39:42.079061','2018-09-02 23:39:42.079496','','Sankuru','sankuru',NULL,1,0),(107,'2018-09-02 23:39:43.223619','2018-09-02 23:39:43.223763','','Sud-Kivu','sud-kivu',NULL,1,0),(108,'2018-09-02 23:39:43.280550','2018-09-02 23:39:43.280650','','Sud-Ubangi','sud-ubangi',NULL,1,0),(109,'2018-09-02 23:39:43.777139','2018-09-02 23:39:43.777227','','Tanganyika','tanganyika',NULL,1,0),(110,'2018-09-02 23:39:44.213227','2018-09-02 23:39:44.213311','','Tshopo','tshopo',NULL,1,0),(111,'2018-09-02 23:39:45.073177','2018-09-02 23:39:45.073284','','Tshuapa','tshuapa',NULL,1,0);
/*!40000 ALTER TABLE `localcore_region` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-22 16:28:38

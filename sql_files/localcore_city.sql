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
-- Table structure for table `localcore_city`
--

DROP TABLE IF EXISTS `localcore_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `localcore_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `slug` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `country_id` int(11) NOT NULL,
  `region_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `city_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `localcore_city_country_id_1e9c58c2_fk_localcore_country_id` (`country_id`),
  KEY `localcore_city_region_id_77ad6b4a_fk_localcore_region_id` (`region_id`),
  CONSTRAINT `localcore_city_country_id_1e9c58c2_fk_localcore_country_id` FOREIGN KEY (`country_id`) REFERENCES `localcore_country` (`id`),
  CONSTRAINT `localcore_city_region_id_77ad6b4a_fk_localcore_region_id` FOREIGN KEY (`region_id`) REFERENCES `localcore_region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localcore_city`
--

LOCK TABLES `localcore_city` WRITE;
/*!40000 ALTER TABLE `localcore_city` DISABLE KEYS */;
INSERT INTO `localcore_city` VALUES (1,'2018-05-02 12:21:44.906490','2018-05-02 12:21:44.906612','KIN','Kinshasa','kinshasa',NULL,1,2,1,''),(2,'2018-05-02 12:25:27.974364','2018-05-02 12:25:27.974530','LSHI','Lubumbashi','lubumbashi',NULL,1,3,1,''),(3,'2018-05-02 12:28:15.915700','2018-05-02 12:28:15.915890','KNG','Kananga','kananga',NULL,1,4,1,''),(4,'2018-05-02 12:30:07.073504','2018-05-02 12:30:07.073709','MBJM','Mbujimayi','mbujimayi',NULL,1,5,1,''),(5,'2018-05-02 12:33:19.005109','2018-05-02 12:33:19.005312','KBD','Kabinda','kabinda',NULL,1,6,1,''),(108,'2018-09-02 23:39:29.601747','2018-09-02 23:39:29.601871','','Bas-Uele District','bas-uele-district',NULL,1,86,0,'District'),(109,'2018-09-02 23:39:30.246484','2018-09-02 23:39:30.248205','','Équateur District','equateur-district',NULL,1,87,0,'District'),(110,'2018-09-02 23:39:30.903286','2018-09-02 23:39:30.903398','','Mbandaka','mbandaka',NULL,1,87,0,'City'),(111,'2018-09-02 23:39:31.103749','2018-09-02 23:39:31.103878','','Haut-Katanga District','haut-katanga-district',NULL,1,88,0,'District'),(112,'2018-09-02 23:39:31.454238','2018-09-02 23:39:31.454369','','Likasi','likasi',NULL,1,88,0,'City'),(113,'2018-09-02 23:39:31.703940','2018-09-02 23:39:31.704039','','Lubumbashi','lubumbashi',NULL,1,88,0,'City'),(114,'2018-09-02 23:39:32.262666','2018-09-02 23:39:32.262749','','Haut-Lomami District','haut-lomami-district',NULL,1,89,0,'District'),(115,'2018-09-02 23:39:32.706247','2018-09-02 23:39:32.706339','','Haut-Uele District','haut-uele-district',NULL,1,90,0,'District'),(116,'2018-09-02 23:39:33.047968','2018-09-02 23:39:33.049028','','Ituri District','ituri-district',NULL,1,91,0,'District'),(117,'2018-09-02 23:39:33.373161','2018-09-02 23:39:33.373292','','Kasaï District','kasai-district',NULL,1,92,0,'District'),(118,'2018-09-02 23:39:33.723196','2018-09-02 23:39:33.723335','','Tshikapa','tshikapa',NULL,1,92,0,'City'),(119,'2018-09-02 23:39:34.251605','2018-09-02 23:39:34.251707','','Mbuji-Mayi','mbuji-mayi',NULL,1,94,0,'City'),(120,'2018-09-02 23:39:34.550810','2018-09-02 23:39:34.550944','','Tshilenge District','tshilenge-district',NULL,1,94,0,'District'),(121,'2018-09-02 23:39:34.884641','2018-09-02 23:39:34.884749','','Funa District','funa-district',NULL,1,95,0,'District'),(122,'2018-09-02 23:39:35.476984','2018-09-02 23:39:35.477094','','Lukunga District','lukunga-district',NULL,1,95,0,'District'),(123,'2018-09-02 23:39:35.885625','2018-09-02 23:39:35.885731','','Mont Amba District','mont-amba-district',NULL,1,95,0,'District'),(124,'2018-09-02 23:39:36.152381','2018-09-02 23:39:36.152510','','Tshangu District','tshangu-district',NULL,1,95,0,'District'),(125,'2018-09-02 23:39:36.527913','2018-09-02 23:39:36.528046','','Kwango District','kwango-district',NULL,1,97,0,'District'),(126,'2018-09-02 23:39:36.944823','2018-09-02 23:39:36.944951','','Kikwit','kikwit',NULL,1,98,0,'City'),(127,'2018-09-02 23:39:37.246339','2018-09-02 23:39:37.246467','','Kwilu District','kwilu-district',NULL,1,98,0,'District'),(128,'2018-09-02 23:39:38.168179','2018-09-02 23:39:38.168368','','Kabinda District','kabinda-district',NULL,1,99,0,'District'),(129,'2018-09-02 23:39:38.477755','2018-09-02 23:39:38.477848','','Mwene-Ditu','mwene-ditu',NULL,1,99,0,'City'),(130,'2018-09-02 23:39:38.793056','2018-09-02 23:39:38.793147','','Kolwezi','kolwezi',NULL,1,100,0,'City'),(131,'2018-09-02 23:39:38.972582','2018-09-02 23:39:38.972678','','Kolwezi District','kolwezi-district',NULL,1,100,0,'District'),(132,'2018-09-02 23:39:39.337463','2018-09-02 23:39:39.337601','','Lualaba District','lualaba-district',NULL,1,100,0,'District'),(133,'2018-09-02 23:39:39.587401','2018-09-02 23:39:39.587548','','Bandundu','bandundu',NULL,1,101,0,'City'),(134,'2018-09-02 23:39:39.787198','2018-09-02 23:39:39.787316','','Mai-Ndombe District','mai-ndombe-district',NULL,1,101,0,'District'),(135,'2018-09-02 23:39:40.177528','2018-09-02 23:39:40.177642','','Plateaux District','plateaux-district',NULL,1,101,0,'District'),(136,'2018-09-02 23:39:40.492324','2018-09-02 23:39:40.492493','','','',NULL,1,102,0,''),(137,'2018-09-02 23:39:41.052053','2018-09-02 23:39:41.052170','','Kindu','kindu',NULL,1,102,0,'City'),(138,'2018-09-02 23:39:41.337206','2018-09-02 23:39:41.337299','','Mongala District','mongala-district',NULL,1,103,0,'District'),(139,'2018-09-02 23:39:41.643904','2018-09-02 23:39:41.643986','','Gbadolite','gbadolite',NULL,1,105,0,'City'),(140,'2018-09-02 23:39:41.844509','2018-09-02 23:39:41.844675','','Nord-Ubangi District','nord-ubangi-district',NULL,1,105,0,'District'),(141,'2018-09-02 23:39:42.236059','2018-09-02 23:39:42.236262','','Sankuru District','sankuru-district',NULL,1,106,0,'District'),(142,'2018-09-02 23:39:43.329731','2018-09-02 23:39:43.329867','','Sud-Ubangi District','sud-ubangi-district',NULL,1,108,0,'District'),(143,'2018-09-02 23:39:43.597601','2018-09-02 23:39:43.597857','','Zongo','zongo',NULL,1,108,0,'City'),(144,'2018-09-02 23:39:43.831069','2018-09-02 23:39:43.831303','','Tanganyika District','tanganyika-district',NULL,1,109,0,'District'),(145,'2018-09-02 23:39:44.264760','2018-09-02 23:39:44.264844','','Kisangani','kisangani',NULL,1,110,0,'City'),(146,'2018-09-02 23:39:44.648036','2018-09-02 23:39:44.648175','','Tshopo District','tshopo-district',NULL,1,110,0,'District'),(147,'2018-09-02 23:39:45.152432','2018-09-02 23:39:45.152565','','Tshuapa District','tshuapa-district',NULL,1,111,0,'District');
/*!40000 ALTER TABLE `localcore_city` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-22 16:31:10

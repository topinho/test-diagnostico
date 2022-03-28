-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: diagnostico
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `inspeccion`
--

DROP TABLE IF EXISTS `inspeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspeccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `revision_id` int NOT NULL,
  `tipo_inspeccion_id` int NOT NULL,
  `observaciones` varchar(200) NOT NULL,
  `estado` varchar(45) NOT NULL,
  `persona_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_inspeccion_id_fk_idx` (`tipo_inspeccion_id`),
  KEY `persona_id_idx` (`persona_id`),
  KEY `revision_id_fk_idx` (`revision_id`),
  CONSTRAINT `persona_id_inspec_fk` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`),
  CONSTRAINT `revision_id_fk` FOREIGN KEY (`revision_id`) REFERENCES `revision` (`id`),
  CONSTRAINT `tipo_inspeccion_id_fk` FOREIGN KEY (`tipo_inspeccion_id`) REFERENCES `tipo_inspeccion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspeccion`
--

LOCK TABLES `inspeccion` WRITE;
/*!40000 ALTER TABLE `inspeccion` DISABLE KEYS */;
INSERT INTO `inspeccion` VALUES (4,1,2,'Ninguna','Ok',2),(6,1,1,'Ninguna','Pendiente',2),(7,1,3,'Ninguna','Pendiente',2),(9,4,3,'Ninguna','Pendiente',2);
/*!40000 ALTER TABLE `inspeccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identificacion` varchar(10) DEFAULT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identificacion_UNIQUE` (`identificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'252937986','German','Torres'),(2,'251103712','Marianella','Lemus');
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revision`
--

DROP TABLE IF EXISTS `revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `revision` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehiculo_id` int NOT NULL,
  `aprobado` int DEFAULT NULL,
  `observaciones` varchar(200) NOT NULL,
  `fecha_revision` date NOT NULL,
  `persona_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vehiculo_id_fk_idx` (`vehiculo_id`),
  KEY `persona_encargado_id_fk_idx` (`persona_id`),
  CONSTRAINT `persona_encargada_id_fk` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`),
  CONSTRAINT `vehiculo_id_fk` FOREIGN KEY (`vehiculo_id`) REFERENCES `vehiculo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revision`
--

LOCK TABLES `revision` WRITE;
/*!40000 ALTER TABLE `revision` DISABLE KEYS */;
INSERT INTO `revision` VALUES (1,1,NULL,'Ninguna','2021-03-28',2),(2,1,NULL,'Ninguna','2022-03-28',2),(3,2,NULL,'Ninguna','2022-03-28',2),(4,3,NULL,'Ninguna','2022-03-28',2);
/*!40000 ALTER TABLE `revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_inspeccion`
--

DROP TABLE IF EXISTS `tipo_inspeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_inspeccion` (
  `id` int NOT NULL,
  `nombre_tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_inspeccion`
--

LOCK TABLES `tipo_inspeccion` WRITE;
/*!40000 ALTER TABLE `tipo_inspeccion` DISABLE KEYS */;
INSERT INTO `tipo_inspeccion` VALUES (1,'Frenos'),(2,'Gases'),(3,'Luces');
/*!40000 ALTER TABLE `tipo_inspeccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiculo`
--

DROP TABLE IF EXISTS `vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiculo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `marca` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `patente` varchar(45) DEFAULT NULL,
  `anio` int DEFAULT NULL,
  `persona_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_id_fk_idx` (`persona_id`),
  CONSTRAINT `persona_id_fk` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiculo`
--

LOCK TABLES `vehiculo` WRITE;
/*!40000 ALTER TABLE `vehiculo` DISABLE KEYS */;
INSERT INTO `vehiculo` VALUES (1,'Toyota','Corolla','BBC-818',2000,1),(2,'Toyota','Carry','AAA-198',2008,1),(3,'Ford','Ka','PPP-911',2019,1);
/*!40000 ALTER TABLE `vehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'diagnostico'
--

--
-- Dumping routines for database 'diagnostico'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-28  9:50:44

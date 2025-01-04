-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: db_copd
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_ii_patient_data`
--

DROP TABLE IF EXISTS `tb_ii_patient_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ii_patient_data` (
  `patient_data_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `ho` tinyint NOT NULL,
  `khac_dom` tinyint NOT NULL,
  `kho_tho` tinyint NOT NULL,
  `tuoi_tren_40` tinyint NOT NULL,
  `hut_thuoc` tinyint NOT NULL,
  `ket_qua` text,
  PRIMARY KEY (`patient_data_id`),
  KEY `tb_ii_patient_data_fk_patient_id_idx` (`patient_id`),
  CONSTRAINT `tb_ii_patient_data_fk_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `tb_patient_info` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_iii_lung_function_data`
--

DROP TABLE IF EXISTS `tb_iii_lung_function_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_iii_lung_function_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `fev1_fvc` float DEFAULT NULL,
  `copd` tinyint DEFAULT NULL,
  `fev1` float DEFAULT NULL,
  `GOLD_stage` varchar(10) DEFAULT NULL,
  `GOLD_stage_description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `tb_iii_lung_function_data_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `tb_patient_info` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_patient_info`
--

DROP TABLE IF EXISTS `tb_patient_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_patient_info` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(45) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `patient_id_UNIQUE` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_v_symptom_assessment_data`
--

DROP TABLE IF EXISTS `tb_v_symptom_assessment_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_v_symptom_assessment_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `mMRC` int DEFAULT NULL,
  `CAT` int DEFAULT NULL,
  `exacerbations` int DEFAULT NULL,
  `hospitalizations` int DEFAULT NULL,
  `grp` text,
  `specific_treatment` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `tb_v_symptom_assessment_data_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `tb_patient_info` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_vi_treatment_protocol_data`
--

DROP TABLE IF EXISTS `tb_vi_treatment_protocol_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_vi_treatment_protocol_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `initial_response` text,
  `status` text,
  `current_treatment` text,
  `second_bronchodilator_effective` tinyint(1) DEFAULT NULL,
  `eosinophils` int DEFAULT NULL,
  `fev1` float DEFAULT NULL,
  `chronic_bronchitis` int DEFAULT NULL,
  `smoker` int DEFAULT NULL,
  `severe_side_effects` int DEFAULT NULL,
  `result` text,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `tb_vi_treatment_protocol_data_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `tb_patient_info` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-04 23:55:13

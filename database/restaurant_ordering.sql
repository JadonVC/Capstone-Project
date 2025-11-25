-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: restaurant_ordering
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'jadon@gmail.com','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','Jadon','Admin','2025-11-16 01:49:39','2025-11-16 02:47:57'),(2,'alexyep345@gmail.com','816cba3be2d18fdfcc6aa7ff4b2167b597bdb52c73f431a4b82933c808b84a3c','Alex','R','2025-11-23 20:01:26','2025-11-23 20:01:26'),(3,'jenayamo@gmail.com','24920ea9bf0f0aa8e151c8883cefd1a62cbf21609ddbf95685fab4c386aed79a','Jenaya','Mo','2025-11-23 21:24:38','2025-11-23 21:24:38'),(4,'sanvik@gmail.com','24920ea9bf0f0aa8e151c8883cefd1a62cbf21609ddbf95685fab4c386aed79a','Sanvi','Karhade','2025-11-23 21:25:33','2025-11-23 21:25:33');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_items`
--

DROP TABLE IF EXISTS `menu_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_items`
--

LOCK TABLES `menu_items` WRITE;
/*!40000 ALTER TABLE `menu_items` DISABLE KEYS */;
INSERT INTO `menu_items` VALUES (1,'Classic Cheeseburger','Juicy beef patty with cheddar cheese, lettuce, tomato, and our special sauce',12.99,'burgers','2025-09-27 20:07:38'),(2,'Chicken Caesar Salad','Fresh romaine lettuce with grilled chicken, parmesan cheese, croutons, and caesar dressing',10.99,'salads','2025-09-27 20:07:38'),(3,'Margherita Pizza','Traditional pizza with tomato sauce, fresh mozzarella, basil, and olive oil',14.99,'pizza','2025-09-27 20:07:38'),(4,'Fish and Chips','Beer-battered cod with golden fries and tartar sauce',16.99,'seafood','2025-09-27 20:07:38'),(5,'Chocolate Brownie','Warm chocolate brownie served with vanilla ice cream',6.99,'desserts','2025-09-27 20:07:38'),(6,'Coca Cola','Ice-cold Coca Cola served in a chilled glass',2.99,'drinks','2025-09-27 20:07:38'),(7,'Chicken wings','8 piece fried wings',10.99,'Wings','2025-09-27 20:07:38'),(8,'Greek Salad','Mixed greens with feta cheese, olives, tomatoes, cucumbers, and olive oil dressing',9.99,'salads','2025-09-27 20:07:38'),(42,'Buffalo Wings','8 piece spicy buffalo wings',12.99,'Wings','2025-11-24 02:15:48');
/*!40000 ALTER TABLE `menu_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `menu_item_id` int NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `item_price` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `menu_item_id` (`menu_item_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`menu_item_id`) REFERENCES `menu_items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,6,'Coca Cola',2.99,1,2.99),(2,2,6,'Coca Cola',2.99,1,2.99),(3,2,5,'Chocolate Brownie',6.99,1,6.99),(4,2,1,'Classic Cheeseburger',12.99,1,12.99),(5,3,6,'Coca Cola',2.99,1,2.99),(6,3,5,'Chocolate Brownie',6.99,1,6.99),(7,3,1,'Classic Cheeseburger',12.99,1,12.99),(8,3,4,'Fish and Chips',16.99,2,33.98),(9,4,5,'Chocolate Brownie',6.99,1,6.99),(10,4,6,'Coca Cola',2.99,1,2.99),(11,4,8,'Greek Salad',9.99,1,9.99),(12,5,1,'Classic Cheeseburger',12.99,1,12.99),(13,5,5,'Chocolate Brownie',6.99,1,6.99),(14,5,6,'Coca Cola',2.99,1,2.99),(15,6,6,'Coca Cola',2.99,1,2.99),(16,6,5,'Chocolate Brownie',6.99,1,6.99),(17,6,4,'Fish and Chips',16.99,1,16.99),(18,7,5,'Chocolate Brownie',6.99,2,13.98),(19,7,6,'Coca Cola',2.99,2,5.98),(20,7,4,'Fish and Chips',16.99,2,33.98),(21,8,6,'Coca Cola',2.99,1,2.99),(22,8,4,'Fish and Chips',16.99,1,16.99),(23,8,5,'Chocolate Brownie',6.99,1,6.99),(24,9,6,'Coca Cola',2.99,1,2.99),(25,9,5,'Chocolate Brownie',6.99,1,6.99),(26,9,4,'Fish and Chips',16.99,1,16.99),(27,10,5,'Chocolate Brownie',6.99,1,6.99),(28,10,6,'Coca Cola',2.99,1,2.99),(29,10,8,'Greek Salad',9.99,1,9.99),(30,11,5,'Chocolate Brownie',6.99,1,6.99),(31,11,6,'Coca Cola',2.99,1,2.99),(32,11,4,'Fish and Chips',16.99,1,16.99),(33,12,7,'BBQ Bacon Burger',15.99,1,15.99),(34,12,5,'Chocolate Brownie',6.99,2,13.98),(35,12,8,'Greek Salad',9.99,2,19.98),(36,13,5,'Chocolate Brownie',6.99,1,6.99),(37,13,6,'Coca Cola',2.99,1,2.99),(38,14,6,'Coca Cola',2.99,1,2.99),(39,14,5,'Chocolate Brownie',6.99,1,6.99),(40,15,6,'Coca Cola',2.99,1,2.99),(41,15,5,'Chocolate Brownie',6.99,1,6.99),(42,16,6,'Coca Cola',2.99,1,2.99),(43,16,5,'Chocolate Brownie',6.99,1,6.99),(44,16,4,'Fish and Chips',16.99,1,16.99);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `customer_address` varchar(500) DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  `order_status` varchar(50) DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `idx_phone` (`customer_phone`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'jadon','91095235','',2.99,'2025-10-30 06:25:26',NULL,'pending'),(2,'Jadon','704 122 233','',22.97,'2025-10-30 06:46:12',NULL,'pending'),(3,'Jadon ','727 454 578','',56.95,'2025-10-30 06:57:14',NULL,'pending'),(4,'jaodn','23423','',19.97,'2025-10-31 04:15:07',NULL,'pending'),(5,'Blake','704 123423 423','',22.97,'2025-10-31 04:23:28',NULL,'pending'),(6,'jadon','235523 235','',26.97,'2025-10-31 04:51:12',NULL,'pending'),(7,'gjhj','5467','',53.94,'2025-11-01 00:11:33',NULL,'pending'),(8,'gjhj','5467','',26.97,'2025-11-01 00:18:01',NULL,'pending'),(9,'dfghdf','6346','',26.97,'2025-11-01 00:24:09',NULL,'pending'),(10,'Jadon ','2345324','',19.97,'2025-11-01 01:28:22',NULL,'pending'),(11,'Jadon ','2345324','',26.97,'2025-11-01 01:38:05',NULL,'pending'),(12,'Sanvi','485 2945','242 Charlotte Ave',49.95,'2025-11-01 01:43:35',NULL,'pending'),(13,'wefg','324','',9.98,'2025-11-01 02:17:17',NULL,'pending'),(14,'Jadon ','9109755626','',9.98,'2025-11-15 22:41:14',NULL,'ready'),(15,'awef','34534543','',9.98,'2025-11-15 23:00:31',1,'completed'),(16,'jake chan','910 435 2524','',26.97,'2025-11-21 03:24:42',2,'preparing');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'jadon@gmail.com','910 124 2147','ee49d153241fa82f2dfdbb6c6293402ba60b995ef21263e48241a40eaaebdfd5','Jadon','V','2025-11-01 02:27:59','2025-11-01 02:27:59'),(2,'jakechan@gmail.com','910 956 4328','def52d5ab6e204a3e1e8b00bb8b69bdd8b9cd34d09697630ce06cf0b17b52917','Jake','Chan','2025-11-21 03:24:03','2025-11-21 03:24:03');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 20:35:04

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2024 at 10:34 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dietdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `logindetails`
--

CREATE TABLE `logindetails` (
  `u_id` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Email` text NOT NULL,
  `Password` text NOT NULL
  `ProfileImage` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `logindetails`
--

INSERT INTO `logindetails` (`u_id`, `Name`, `Email`, `Password`) VALUES
(1, 'test', 'test1@gmail.com', '1234'),
(2, 'test', 'test@gmail.com', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `test1@gmail.com`
--

CREATE TABLE `test1@gmail.com` (
  `User_Table_id` int(11) NOT NULL,
  `DietName` varchar(255) DEFAULT NULL,
  `dietType` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `foodName` varchar(255) DEFAULT NULL,
  `carbs` int(20) DEFAULT NULL,
  `protein` int(20) DEFAULT NULL,
  `calories` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `test1@gmail.com`
--

INSERT INTO `test1@gmail.com` (`User_Table_id`, `DietName`, `dietType`, `image_url`, `foodName`, `carbs`, `protein`, `calories`) VALUES
(1, 'Select_Diet', 'Select Diet Type', 'https://blissfullylowcarb.com/wp-content/uploads/2021/08/almond-flour-keto-pancakes-feature.jpg', 'Almond Flour Pancakes', 9, 11, 242),
(2, 'Select_Diet', 'Select Diet Type', 'https://tmbidigitalassetsazure.blob.core.windows.net/wpthumbnailsprod/CauliflowerCheddarSoup%20DIYD%203493%20062821%20H_thumbnail.jpeg', 'Cauliflower and Cheese Soup', 25, 15, 270),
(4, 'Select_Diet', 'Select Diet Type', 'https://www.delishdlites.com/wp-content/uploads/2018/03/DSC_0663labelled-1024x682-1024x682.jpg', 'Grilled Lamb Chops', 43, 52, 980),
(5, 'Select_Diet', 'Select Diet Type', 'https://blissfullylowcarb.com/wp-content/uploads/2021/08/almond-flour-keto-pancakes-feature.jpg', 'Almond Flour Pancakes', 9, 11, 242);

-- --------------------------------------------------------

--
-- Table structure for table `test@gmail.com`
--

CREATE TABLE `test@gmail.com` (
  `User_Table_id` int(11) NOT NULL,
  `DietName` varchar(255) DEFAULT NULL,
  `dietType` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `foodName` varchar(255) DEFAULT NULL,
  `carbs` int(20) DEFAULT NULL,
  `protein` int(20) DEFAULT NULL,
  `calories` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `testt@gmail.com`
--

CREATE TABLE `testt@gmail.com` (
  `User_Table_id` int(11) NOT NULL,
  `DietName` varchar(255) DEFAULT NULL,
  `dietType` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `foodName` varchar(255) DEFAULT NULL,
  `carbs` int(20) DEFAULT NULL,
  `protein` int(20) DEFAULT NULL,
  `calories` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `zak@gmail.com`
--

CREATE TABLE `zak@gmail.com` (
  `User_Table_id` int(11) NOT NULL,
  `DietName` varchar(255) DEFAULT NULL,
  `dietType` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `foodName` varchar(255) DEFAULT NULL,
  `carbs` int(20) DEFAULT NULL,
  `protein` int(20) DEFAULT NULL,
  `calories` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `logindetails`
--
ALTER TABLE `logindetails`
  ADD PRIMARY KEY (`u_id`);

--
-- Indexes for table `test1@gmail.com`
--
ALTER TABLE `test1@gmail.com`
  ADD PRIMARY KEY (`User_Table_id`);

--
-- Indexes for table `test@gmail.com`
--
ALTER TABLE `test@gmail.com`
  ADD PRIMARY KEY (`User_Table_id`);

--
-- Indexes for table `testt@gmail.com`
--
ALTER TABLE `testt@gmail.com`
  ADD PRIMARY KEY (`User_Table_id`);

--
-- Indexes for table `zak@gmail.com`
--
ALTER TABLE `zak@gmail.com`
  ADD PRIMARY KEY (`User_Table_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `logindetails`
--
ALTER TABLE `logindetails`
  MODIFY `u_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `test1@gmail.com`
--
ALTER TABLE `test1@gmail.com`
  MODIFY `User_Table_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `test@gmail.com`
--
ALTER TABLE `test@gmail.com`
  MODIFY `User_Table_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `testt@gmail.com`
--
ALTER TABLE `testt@gmail.com`
  MODIFY `User_Table_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `zak@gmail.com`
--
ALTER TABLE `zak@gmail.com`
  MODIFY `User_Table_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

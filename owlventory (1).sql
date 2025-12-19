-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2025 at 04:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `owlventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminID` varchar(10) NOT NULL,
  `Fn` varchar(50) NOT NULL,
  `Mn` varchar(50) DEFAULT NULL,
  `Ln` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminID`, `Fn`, `Mn`, `Ln`, `password`) VALUES
('A001', 'John', 'Doe', 'Dough', '123');

-- --------------------------------------------------------

--
-- Table structure for table `computer`
--

CREATE TABLE `computer` (
  `pcNo` int(11) NOT NULL,
  `status` varchar(20) DEFAULT 'Inactive',
  `assignedEmp` int(11) DEFAULT NULL,
  `dateAssigned` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `computer`
--

INSERT INTO `computer` (`pcNo`, `status`, `assignedEmp`, `dateAssigned`) VALUES
(13, 'Active', 6, '2025-12-19'),
(14, 'Active', 7, '2025-12-19');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `employeeID` int(11) NOT NULL,
  `Fn` varchar(50) NOT NULL,
  `Mn` varchar(50) DEFAULT NULL,
  `Ln` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`employeeID`, `Fn`, `Mn`, `Ln`, `password`) VALUES
(6, 'Jane', 'Doe', 'Dough', '123'),
(7, 'Lois', 'Lane', 'Clark', '123');

-- --------------------------------------------------------

--
-- Table structure for table `hardware`
--

CREATE TABLE `hardware` (
  `hardwareID` int(11) NOT NULL,
  `hardwareName` varchar(50) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hardware`
--

INSERT INTO `hardware` (`hardwareID`, `hardwareName`, `brand`, `quantity`) VALUES
(1, 'Monitor', 'Lenovo', 2),
(2, 'Keyboard & Mouse', 'Logitech', 2),
(3, 'GPU', 'Nvidia', 2),
(4, 'Motherboard', 'ROG', 2),
(5, 'RAM', 'Kingston', 2);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `requestID` int(11) NOT NULL,
  `pcNo` int(11) DEFAULT NULL,
  `employeeID` int(11) DEFAULT NULL,
  `hardware` varchar(100) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `dateAction` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `validator` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stock_logs`
--

CREATE TABLE `stock_logs` (
  `hardwareID` int(11) NOT NULL,
  `quantityChanged` int(11) NOT NULL,
  `adminID` varchar(50) NOT NULL,
  `dateAdded` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock_logs`
--

INSERT INTO `stock_logs` (`hardwareID`, `quantityChanged`, `adminID`, `dateAdded`) VALUES
(1, 1, 'A001', '2025-12-19 22:43:39'),
(2, 1, 'A001', '2025-12-19 22:43:40'),
(3, 1, 'A001', '2025-12-19 22:43:42'),
(4, 1, 'A001', '2025-12-19 22:43:43'),
(5, 1, 'A001', '2025-12-19 22:43:45'),
(1, 1, 'A001', '2025-12-19 22:43:46'),
(2, 1, 'A001', '2025-12-19 22:43:47'),
(3, 1, 'A001', '2025-12-19 22:43:49'),
(4, 1, 'A001', '2025-12-19 22:43:51'),
(5, 1, 'A001', '2025-12-19 22:43:53'),
(1, 1, 'A001', '2025-12-19 22:43:54'),
(2, 1, 'A001', '2025-12-19 22:43:55'),
(3, 1, 'A001', '2025-12-19 22:43:56'),
(4, 1, 'A001', '2025-12-19 22:43:58'),
(5, 1, 'A001', '2025-12-19 22:44:00'),
(1, 1, 'A001', '2025-12-19 22:44:01'),
(2, 1, 'A001', '2025-12-19 22:44:02'),
(3, 1, 'A001', '2025-12-19 22:44:04'),
(4, 1, 'A001', '2025-12-19 22:44:06'),
(5, 1, 'A001', '2025-12-19 22:44:07'),
(1, -1, 'A001', '2025-12-19 22:44:11'),
(2, -1, 'A001', '2025-12-19 22:44:11'),
(3, -1, 'A001', '2025-12-19 22:44:11'),
(4, -1, 'A001', '2025-12-19 22:44:11'),
(5, -1, 'A001', '2025-12-19 22:44:11'),
(1, -1, 'A001', '2025-12-19 22:44:14'),
(2, -1, 'A001', '2025-12-19 22:44:14'),
(3, -1, 'A001', '2025-12-19 22:44:14'),
(4, -1, 'A001', '2025-12-19 22:44:14'),
(5, -1, 'A001', '2025-12-19 22:44:14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminID`);

--
-- Indexes for table `computer`
--
ALTER TABLE `computer`
  ADD PRIMARY KEY (`pcNo`),
  ADD KEY `assignedEmp` (`assignedEmp`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`employeeID`);

--
-- Indexes for table `hardware`
--
ALTER TABLE `hardware`
  ADD PRIMARY KEY (`hardwareID`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`requestID`),
  ADD KEY `pcNo` (`pcNo`),
  ADD KEY `employeeID` (`employeeID`);

--
-- Indexes for table `stock_logs`
--
ALTER TABLE `stock_logs`
  ADD KEY `hardwareID` (`hardwareID`),
  ADD KEY `adminID` (`adminID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `computer`
--
ALTER TABLE `computer`
  MODIFY `pcNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `employeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `hardware`
--
ALTER TABLE `hardware`
  MODIFY `hardwareID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `requestID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `computer`
--
ALTER TABLE `computer`
  ADD CONSTRAINT `computer_ibfk_1` FOREIGN KEY (`assignedEmp`) REFERENCES `employee` (`employeeID`);

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`pcNo`) REFERENCES `computer` (`pcNo`) ON DELETE CASCADE,
  ADD CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`employeeID`) REFERENCES `employee` (`employeeID`) ON DELETE CASCADE;

--
-- Constraints for table `stock_logs`
--
ALTER TABLE `stock_logs`
  ADD CONSTRAINT `stock_logs_ibfk_1` FOREIGN KEY (`hardwareID`) REFERENCES `hardware` (`hardwareID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stock_logs_ibfk_2` FOREIGN KEY (`adminID`) REFERENCES `admin` (`adminID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

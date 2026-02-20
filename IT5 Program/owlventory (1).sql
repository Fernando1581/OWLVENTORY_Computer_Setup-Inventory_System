-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2026 at 12:49 PM
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
('A001', 'John', 'Doe', 'Manager', '****');

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
(1, 'Active', 1, '2026-02-09'),
(2, 'Active', 2, '2026-02-09'),
(3, 'Active', 3, '2026-02-10'),
(4, 'Available', NULL, NULL),
(5, 'Available', NULL, NULL);

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
(1, 'Vert', 'Lurt', 'Kurt', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
(2, 'Spenz', 'Kenz', 'Lenz', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
(3, 'levi', 'dann', 'alicaya', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

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
(1, 'Monitor', 'Lenovo', 9),
(2, 'Keyboard & Mouse', 'Logitech', 10),
(3, 'GPU', 'Nvidia', 10),
(4, 'Motherboard', 'ROG', 10),
(5, 'RAM', 'Kingston', 9);

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
  `dateStarted` datetime DEFAULT NULL,
  `dateFinished` datetime DEFAULT NULL,
  `validator` varchar(10) DEFAULT NULL,
  `is_read` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`requestID`, `pcNo`, `employeeID`, `hardware`, `reason`, `status`, `dateAction`, `dateStarted`, `dateFinished`, `validator`, `is_read`) VALUES
(1, 1, 1, 'Keyboard & Mouse', 'Broken keyboard', 'Marlo Juan', '2026-02-09 06:36:22', NULL, NULL, 'A001', 0),
(2, 1, 1, 'Motherboard', 'Pc turning off after 10 mins', 'Levi Alicaya', '2026-02-10 08:01:21', NULL, NULL, 'A001', 0),
(3, 3, 3, 'Keyboard & Mouse', 'dili mugana ang letter \"k\' sa kb', 'Marlo Juan', '2026-02-19 03:29:54', NULL, NULL, 'A001', 0),
(4, 1, 1, 'Monitor', 'testing', 'Marlo Juan', '2026-02-19 03:38:32', NULL, NULL, 'A001', 0);

-- --------------------------------------------------------

--
-- Table structure for table `stock_logs`
--

CREATE TABLE `stock_logs` (
  `logID` int(11) NOT NULL,
  `hardwareID` int(11) NOT NULL,
  `quantityChanged` int(11) NOT NULL,
  `adminID` varchar(10) NOT NULL,
  `dateAdded` datetime DEFAULT current_timestamp(),
  `reason` varchar(255) DEFAULT 'Stock Adjustment'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock_logs`
--

INSERT INTO `stock_logs` (`logID`, `hardwareID`, `quantityChanged`, `adminID`, `dateAdded`, `reason`) VALUES
(1, 1, -1, 'A001', '2026-02-09 14:33:15', 'Stock Adjustment'),
(2, 2, -1, 'A001', '2026-02-09 14:33:15', 'Stock Adjustment'),
(3, 3, -1, 'A001', '2026-02-09 14:33:15', 'Stock Adjustment'),
(4, 4, -1, 'A001', '2026-02-09 14:33:15', 'Stock Adjustment'),
(5, 5, -1, 'A001', '2026-02-09 14:33:15', 'Stock Adjustment'),
(6, 1, -1, 'A001', '2026-02-09 14:33:20', 'Stock Adjustment'),
(7, 2, -1, 'A001', '2026-02-09 14:33:20', 'Stock Adjustment'),
(8, 3, -1, 'A001', '2026-02-09 14:33:20', 'Stock Adjustment'),
(9, 4, -1, 'A001', '2026-02-09 14:33:20', 'Stock Adjustment'),
(10, 5, -1, 'A001', '2026-02-09 14:33:20', 'Stock Adjustment'),
(11, 1, -1, 'A001', '2026-02-09 14:33:23', 'Stock Adjustment'),
(12, 2, -1, 'A001', '2026-02-09 14:33:23', 'Stock Adjustment'),
(13, 3, -1, 'A001', '2026-02-09 14:33:23', 'Stock Adjustment'),
(14, 4, -1, 'A001', '2026-02-09 14:33:23', 'Stock Adjustment'),
(15, 5, -1, 'A001', '2026-02-09 14:33:23', 'Stock Adjustment'),
(16, 1, -1, 'A001', '2026-02-09 14:33:27', 'Stock Adjustment'),
(17, 2, -1, 'A001', '2026-02-09 14:33:27', 'Stock Adjustment'),
(18, 3, -1, 'A001', '2026-02-09 14:33:27', 'Stock Adjustment'),
(19, 4, -1, 'A001', '2026-02-09 14:33:27', 'Stock Adjustment'),
(20, 5, -1, 'A001', '2026-02-09 14:33:27', 'Stock Adjustment'),
(21, 1, 1, 'A001', '2026-02-09 14:33:32', 'Stock Adjustment'),
(22, 2, 1, 'A001', '2026-02-09 14:33:35', 'Stock Adjustment'),
(23, 3, 1, 'A001', '2026-02-09 14:33:37', 'Stock Adjustment'),
(24, 4, 1, 'A001', '2026-02-09 14:33:40', 'Stock Adjustment'),
(25, 4, 1, 'A001', '2026-02-09 14:33:42', 'Stock Adjustment'),
(26, 4, 1, 'A001', '2026-02-09 14:33:43', 'Stock Adjustment'),
(27, 4, 1, 'A001', '2026-02-09 14:33:44', 'Stock Adjustment'),
(28, 3, 1, 'A001', '2026-02-09 14:33:46', 'Stock Adjustment'),
(29, 3, 1, 'A001', '2026-02-09 14:33:48', 'Stock Adjustment'),
(30, 3, 1, 'A001', '2026-02-09 14:33:49', 'Stock Adjustment'),
(31, 2, 1, 'A001', '2026-02-09 14:33:51', 'Stock Adjustment'),
(32, 2, 1, 'A001', '2026-02-09 14:33:53', 'Stock Adjustment'),
(33, 2, 1, 'A001', '2026-02-09 14:33:54', 'Stock Adjustment'),
(34, 1, 1, 'A001', '2026-02-09 14:33:56', 'Stock Adjustment'),
(35, 1, 1, 'A001', '2026-02-09 14:33:58', 'Stock Adjustment'),
(36, 1, 1, 'A001', '2026-02-09 14:34:00', 'Stock Adjustment'),
(37, 5, 1, 'A001', '2026-02-09 14:34:03', 'Stock Adjustment'),
(38, 5, 1, 'A001', '2026-02-09 14:34:08', 'Stock Adjustment'),
(39, 5, 1, 'A001', '2026-02-09 14:34:10', 'Stock Adjustment'),
(40, 5, 1, 'A001', '2026-02-09 14:34:12', 'Stock Adjustment'),
(41, 2, -1, 'A001', '2026-02-09 14:36:22', 'Stock Adjustment'),
(42, 1, 1, 'A001', '2026-02-10 15:54:30', 'Stock Adjustment'),
(43, 1, 1, 'A001', '2026-02-10 15:54:34', 'Stock Adjustment'),
(44, 1, -1, 'A001', '2026-02-10 15:55:36', 'Stock Adjustment'),
(45, 1, -1, 'A001', '2026-02-10 15:55:56', 'Stock Adjustment'),
(46, 1, -1, 'A001', '2026-02-10 15:57:29', 'Stock Adjustment'),
(47, 2, -1, 'A001', '2026-02-10 15:57:29', 'Stock Adjustment'),
(48, 3, -1, 'A001', '2026-02-10 15:57:29', 'Stock Adjustment'),
(49, 4, -1, 'A001', '2026-02-10 15:57:29', 'Stock Adjustment'),
(50, 5, -1, 'A001', '2026-02-10 15:57:29', 'Stock Adjustment'),
(51, 4, -1, 'A001', '2026-02-10 16:01:21', 'Stock Adjustment'),
(52, 2, -1, 'A001', '2026-02-19 11:29:54', 'Used for repair'),
(53, 1, -1, 'A001', '2026-02-19 11:38:32', 'Used for repair'),
(54, 1, 1, 'A001', '2026-02-19 11:39:17', 'Stocking'),
(55, 1, 1, 'A001', '2026-02-19 11:39:19', 'Stocking'),
(56, 2, 1, 'A001', '2026-02-19 11:39:21', 'Stocking'),
(57, 2, 1, 'A001', '2026-02-19 11:39:23', 'Stocking'),
(58, 2, 1, 'A001', '2026-02-19 11:39:25', 'Stocking'),
(59, 3, 1, 'A001', '2026-02-19 11:39:26', 'Stocking'),
(60, 4, 1, 'A001', '2026-02-19 11:39:28', 'Stocking'),
(61, 4, 1, 'A001', '2026-02-19 11:39:30', 'Stocking'),
(62, 5, 1, 'A001', '2026-02-19 11:39:32', 'Stocking'),
(63, 5, 1, 'A001', '2026-02-19 11:39:34', 'Stocking'),
(64, 5, 1, 'A001', '2026-02-19 11:39:36', 'Stocking'),
(65, 5, 1, 'A001', '2026-02-19 11:39:38', 'Stocking'),
(66, 5, 1, 'A001', '2026-02-19 11:39:41', 'Stocking'),
(67, 1, -1, 'A001', '2026-02-19 11:39:46', 'Damaged/Defective'),
(68, 1, -1, 'A001', '2026-02-19 11:39:50', 'Transfered'),
(69, 1, 1, 'A001', '2026-02-19 11:39:53', 'Stocking'),
(70, 1, 1, 'A001', '2026-02-19 11:39:54', 'Stocking'),
(71, 1, -1, 'A001', '2026-02-19 14:43:12', 'Damaged/Defective');

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
  ADD KEY `employeeID` (`employeeID`),
  ADD KEY `validator` (`validator`);

--
-- Indexes for table `stock_logs`
--
ALTER TABLE `stock_logs`
  ADD PRIMARY KEY (`logID`),
  ADD KEY `hardwareID` (`hardwareID`),
  ADD KEY `adminID` (`adminID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `computer`
--
ALTER TABLE `computer`
  MODIFY `pcNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `employeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `hardware`
--
ALTER TABLE `hardware`
  MODIFY `hardwareID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `requestID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `stock_logs`
--
ALTER TABLE `stock_logs`
  MODIFY `logID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `computer`
--
ALTER TABLE `computer`
  ADD CONSTRAINT `computer_ibfk_1` FOREIGN KEY (`assignedEmp`) REFERENCES `employee` (`employeeID`) ON DELETE SET NULL;

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`pcNo`) REFERENCES `computer` (`pcNo`) ON DELETE CASCADE,
  ADD CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`employeeID`) REFERENCES `employee` (`employeeID`) ON DELETE CASCADE,
  ADD CONSTRAINT `requests_ibfk_3` FOREIGN KEY (`validator`) REFERENCES `admin` (`adminID`) ON DELETE SET NULL;

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

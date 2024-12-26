-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 26, 2024 at 06:31 AM
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
-- Database: `minimarket_semesta`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_akun`
--
-- Creation: Dec 24, 2024 at 06:56 PM
-- Last update: Dec 24, 2024 at 06:57 PM
--

CREATE TABLE `tbl_akun` (
  `id_akun` int(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `role` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELATIONSHIPS FOR TABLE `tbl_akun`:
--

--
-- Dumping data for table `tbl_akun`
--

INSERT INTO `tbl_akun` (`id_akun`, `username`, `password`, `email`, `role`) VALUES
(1, 'indra', 'indra123', 'indra@minimarketseme', 'admin'),
(2, 'yaya', 'yaya123', 'yaya@minimarketsemesta.com', 'kasir'),
(3, 'dini', 'dini123', 'dini@minimarketsemesta.com', 'kasir'),
(4, 'vito', 'vito123', 'vito@minimarketsemesta.com', 'kasir');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_chat`
--
-- Creation: Dec 24, 2024 at 06:26 PM
-- Last update: Dec 25, 2024 at 06:15 PM
--

CREATE TABLE `tbl_chat` (
  `id_chat` int(10) NOT NULL,
  `pengirim` varchar(50) NOT NULL,
  `penerima` varchar(50) NOT NULL,
  `chat` varchar(50) NOT NULL,
  `waktu_chat` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELATIONSHIPS FOR TABLE `tbl_chat`:
--

--
-- Dumping data for table `tbl_chat`
--

INSERT INTO `tbl_chat` (`id_chat`, `pengirim`, `penerima`, `chat`, `waktu_chat`) VALUES
(1, 'yaya', 'admin', 'yaya123', '2024-12-25 01:25:04'),
(2, 'dini', '', 'dini123', '2024-12-25 01:25:04'),
(7, 'coba', '', '1', '2024-12-25 01:25:04'),
(8, 'yaya', 'yaya', 'aaa', '2024-12-26 00:29:20'),
(9, 'yaya', 'yaya', 'a', '2024-12-26 00:29:24'),
(10, 'indra', 'yaya', 'hallo', '2024-12-26 00:38:42'),
(11, 'yaya', 'yaya', 'iya kak admin', '2024-12-26 00:38:51'),
(12, 'indra', 'yaya', 'nnn', '2024-12-26 00:40:34'),
(13, 'indra', 'indra', 'iya', '2024-12-26 00:40:40'),
(14, 'indra', 'yaya', 'hallo', '2024-12-26 00:42:16'),
(15, 'yaya', 'yaya', 'iya kak', '2024-12-26 00:42:25'),
(16, 'indra', 'yaya', 'tidak masuk', '2024-12-26 00:42:40'),
(17, 'yaya', 'yaya', 'kaloo', '2024-12-26 00:42:50'),
(18, 'indra', 'yaya', 'halo', '2024-12-26 00:58:35'),
(19, 'indra', 'yaya', 'halo', '2024-12-26 00:58:51'),
(20, 'yaya', 'indra', 'iya kak', '2024-12-26 00:59:00'),
(21, 'indra', 'yaya', 'stok produk sudah saya update', '2024-12-26 00:59:30'),
(22, 'indra', 'yaya', 'halo', '2024-12-26 01:00:41'),
(23, 'yaya', 'indra', 'iya kak', '2024-12-26 01:00:50'),
(24, 'indra', 'yaya', 'stok produk sudah saya update', '2024-12-26 01:01:07'),
(25, 'yaya', 'indra', 'halo kak', '2024-12-26 01:04:00'),
(26, 'indra', 'dini', 'halo dini', '2024-12-26 01:04:28'),
(27, 'indra', 'yaya', 'halo', '2024-12-26 01:10:11'),
(28, 'yaya', 'indra', 'iya kak', '2024-12-26 01:10:17'),
(29, 'indra', 'vito', 'kontol', '2024-12-26 01:15:05');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_produk`
--
-- Creation: Dec 23, 2024 at 07:19 AM
--

CREATE TABLE `tbl_produk` (
  `id_produk` varchar(50) NOT NULL,
  `nama_produk` varchar(50) NOT NULL,
  `harga_satuan` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELATIONSHIPS FOR TABLE `tbl_produk`:
--

--
-- Dumping data for table `tbl_produk`
--

INSERT INTO `tbl_produk` (`id_produk`, `nama_produk`, `harga_satuan`) VALUES
('A02', 'Lifeboy', 3000),
('A03', 'Rejoice shampo', 12000),
('A04', 'Pantene Shampo', 12000),
('A05', 'Formula Sikat Gigi', 5000),
('A06', 'Tissue Panda', 7000),
('A07', 'Nabati', 10000),
('A08', 'Sabun Pepaya', 5000),
('A09', 'pisang goreng', 10000),
('A10', 'Tanggo', 7000),
('A11', 'Kusuka Kripik singkong', 15000),
('A12', 'Sari Roti', 10000),
('A13', 'Ice Cream pedolpop', 5000),
('A14', 'Taro Kripik', 6000),
('A15', 'Kelly Pearl Cream', 8000),
('A16', 'Skintific Cushion', 150000),
('A17', 'Scarlet Handbody', 50000),
('A18', 'Citra Body Serum', 25000),
('A19', 'Bulu Mata Palsu', 35000),
('A20', 'Kuteks Tiya', 50000),
('A21', 'Pomade Krim Rambut', 35000),
('A22', 'Parfum Posh men', 20000),
('A23', 'Gillete Cukur', 7000),
('A24', 'Sunscreen Emina', 25000);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_transaksi`
--
-- Creation: Dec 24, 2024 at 07:14 PM
--

CREATE TABLE `tbl_transaksi` (
  `id_transaksi` int(11) NOT NULL,
  `no_nota` int(10) NOT NULL,
  `id_akun` int(11) NOT NULL,
  `id_produk` varchar(11) NOT NULL,
  `kuantitas_produk` int(11) NOT NULL,
  `harga_satuan` int(10) NOT NULL,
  `sub_total` int(10) NOT NULL,
  `tanggal_transaksi` datetime NOT NULL,
  `total_pembayaran` int(10) NOT NULL,
  `dibayarkan` int(11) NOT NULL,
  `kembalian` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELATIONSHIPS FOR TABLE `tbl_transaksi`:
--   `id_akun`
--       `tbl_akun` -> `id_akun`
--   `id_produk`
--       `tbl_produk` -> `id_produk`
--

--
-- Dumping data for table `tbl_transaksi`
--

INSERT INTO `tbl_transaksi` (`id_transaksi`, `no_nota`, `id_akun`, `id_produk`, `kuantitas_produk`, `harga_satuan`, `sub_total`, `tanggal_transaksi`, `total_pembayaran`, `dibayarkan`, `kembalian`) VALUES
(1, 1, 1, 'A04', 5, 12000, 60000, '2024-07-09 00:00:00', 60000, 100000, 40000),
(2, 1, 1, 'A22', 1, 50000, 50000, '2024-07-18 00:00:00', 50000, 50000, 0),
(3, 1, 1, 'A20', 1, 5000, 5000, '2024-07-01 11:00:00', 5000, 5000, 0),
(4, 2, 2, 'A02', 5, 10000, 50000, '2024-07-01 11:30:00', 50000, 55000, 5000),
(5, 4, 1, 'A11', 4, 3000, 12000, '2024-07-01 12:00:00', 12000, 15000, 3000),
(6, 5, 2, 'A21', 2, 5000, 10000, '2024-07-01 12:30:00', 10000, 10000, 0),
(7, 6, 1, 'A03', 3, 10000, 30000, '2024-07-01 13:00:00', 30000, 35000, 5000),
(8, 7, 2, 'A12', 1, 3000, 3000, '2024-07-01 13:30:00', 3000, 5000, 2000),
(9, 8, 1, 'A22', 4, 5000, 20000, '2024-07-01 14:00:00', 20000, 25000, 5000),
(10, 9, 2, 'A20', 2, 5000, 10000, '2024-07-01 14:30:00', 10000, 10000, 0),
(11, 10, 1, 'A02', 3, 3000, 9000, '2024-07-01 15:00:00', 9000, 10000, 1000),
(12, 11, 2, 'A03', 1, 5000, 5000, '2024-07-01 15:30:00', 5000, 5000, 0),
(13, 12, 1, 'A10', 5, 10000, 50000, '2024-07-01 16:00:00', 50000, 60000, 10000),
(14, 13, 2, 'A02', 4, 3000, 12000, '2024-07-01 16:30:00', 12000, 15000, 3000),
(15, 14, 1, 'A03', 2, 5000, 10000, '2024-07-01 17:00:00', 10000, 12000, 2000),
(16, 14, 1, 'A10', 2, 3000, 6000, '2024-07-01 10:00:00', 6000, 10000, 4000),
(17, 15, 2, 'A10', 3, 3000, 9000, '2024-07-01 10:30:00', 9000, 10000, 1000),
(18, 16, 1, 'A10', 2, 7000, 14000, '2024-07-25 00:00:00', 28000, 30000, 2000),
(19, 16, 1, 'A10', 2, 7000, 14000, '2024-07-25 00:00:00', 28000, 30000, 2000),
(20, 17, 1, 'A10', 2, 7000, 14000, '2024-07-26 00:00:00', 28000, 30000, 2000),
(21, 17, 1, 'A20', 1, 8000, 8000, '2024-07-26 00:00:00', 28000, 30000, 2000),
(22, 18, 1, 'A02', 2, 3000, 6000, '2024-07-24 00:00:00', 56000, 60000, 4000),
(23, 18, 1, 'A22', 1, 50000, 50000, '2024-07-24 00:00:00', 56000, 60000, 4000),
(24, 1, 1, 'A02', 2, 3000, 6000, '2024-12-24 00:00:00', 6000, 10000, 4000),
(25, 1, 1, 'A02', 10, 3000, 30000, '2024-12-24 00:00:00', 30000, 50000, 20000),
(26, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000),
(27, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000),
(28, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000),
(29, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000),
(30, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 25000, 10000),
(31, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000),
(32, 1, 1, 'A02', 5, 3000, 15000, '2024-12-24 00:00:00', 15000, 20000, 5000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_akun`
--
ALTER TABLE `tbl_akun`
  ADD PRIMARY KEY (`id_akun`);

--
-- Indexes for table `tbl_chat`
--
ALTER TABLE `tbl_chat`
  ADD PRIMARY KEY (`id_chat`);

--
-- Indexes for table `tbl_produk`
--
ALTER TABLE `tbl_produk`
  ADD PRIMARY KEY (`id_produk`);

--
-- Indexes for table `tbl_transaksi`
--
ALTER TABLE `tbl_transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_kasir` (`id_akun`),
  ADD KEY `id_produk` (`id_produk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_chat`
--
ALTER TABLE `tbl_chat`
  MODIFY `id_chat` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `tbl_transaksi`
--
ALTER TABLE `tbl_transaksi`
  MODIFY `id_transaksi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_transaksi`
--
ALTER TABLE `tbl_transaksi`
  ADD CONSTRAINT `tbl_transaksi_ibfk_1` FOREIGN KEY (`id_akun`) REFERENCES `tbl_akun` (`id_akun`),
  ADD CONSTRAINT `tbl_transaksi_ibfk_2` FOREIGN KEY (`id_produk`) REFERENCES `tbl_produk` (`id_produk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

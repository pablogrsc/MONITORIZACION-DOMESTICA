-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 04-04-2021 a las 18:48:14
-- Versión del servidor: 10.3.25-MariaDB-0+deb10u1
-- Versión de PHP: 7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `homemonitor_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hosts`
--

CREATE TABLE `hosts` (
  `id` int(11) NOT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `mac` varchar(17) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `isp`
--

CREATE TABLE `isp` (
  `id` int(11) NOT NULL,
  `hour` datetime DEFAULT NULL,
  `latency` double DEFAULT NULL,
  `download` double DEFAULT NULL,
  `download_ratio` double DEFAULT NULL,
  `upload` double DEFAULT NULL,
  `upload_ratio` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `snmp_linux`
--

CREATE TABLE `snmp_linux` (
  `id` int(11) NOT NULL,
  `hour` datetime DEFAULT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `load1` double DEFAULT NULL,
  `load5` double DEFAULT NULL,
  `load15` double DEFAULT NULL,
  `user_cpu` double DEFAULT NULL,
  `system_cpu` double DEFAULT NULL,
  `idle_cpu` double DEFAULT NULL,
  `ram_total` double DEFAULT NULL,
  `ram_free` double DEFAULT NULL,
  `ram_buffer` double DEFAULT NULL,
  `ram_cache` double DEFAULT NULL,
  `disk_total` double DEFAULT NULL,
  `disk_free` double DEFAULT NULL,
  `disk_used` double DEFAULT NULL,
  `disk_percent` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `snmp_windows`
--

CREATE TABLE `snmp_windows` (
  `id` int(11) NOT NULL,
  `hour` datetime DEFAULT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `cpu_usage` double DEFAULT NULL,
  `ram_total` double DEFAULT NULL,
  `ram_used` double DEFAULT NULL,
  `disk_total` double DEFAULT NULL,
  `disk_used` double DEFAULT NULL,
  `disk_free` double DEFAULT NULL,
  `disk_percent` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `hosts`
--
ALTER TABLE `hosts`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `isp`
--
ALTER TABLE `isp`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `snmp_linux`
--
ALTER TABLE `snmp_linux`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `snmp_windows`
--
ALTER TABLE `snmp_windows`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `hosts`
--
ALTER TABLE `hosts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=125;
--
-- AUTO_INCREMENT de la tabla `isp`
--
ALTER TABLE `isp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5756;
--
-- AUTO_INCREMENT de la tabla `snmp_linux`
--
ALTER TABLE `snmp_linux`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=494;
--
-- AUTO_INCREMENT de la tabla `snmp_windows`
--
ALTER TABLE `snmp_windows`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=955;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

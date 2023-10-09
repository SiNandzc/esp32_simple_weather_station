/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : wms

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 21/09/2023 12:26:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for h_t_table
-- ----------------------------
DROP TABLE IF EXISTS `h_t_table`;
CREATE TABLE `h_t_table`  (
  `dateTime` datetime NULL DEFAULT NULL,
  `humidity` tinyint(11) NULL DEFAULT NULL,
  `temperature` tinyint(11) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

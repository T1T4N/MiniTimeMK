-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Feb 06, 2015 at 03:31 PM
-- Server version: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `timemk`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_cas`
--

CREATE TABLE IF NOT EXISTS `auth_cas` (
`id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_event`
--

CREATE TABLE IF NOT EXISTS `auth_event` (
`id` int(11) NOT NULL,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
`id` int(11) NOT NULL,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_membership`
--

CREATE TABLE IF NOT EXISTS `auth_membership` (
`id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
`id` int(11) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
`id` int(11) NOT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
`id` int(5) NOT NULL,
  `category` varchar(30) COLLATE utf8_bin NOT NULL,
  `factor` int(11) NOT NULL DEFAULT '1',
  `static_name` varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `category`, `factor`, `static_name`) VALUES
(1, 'Македонија', 1, 'makedonija'),
(2, 'Свет', 1, 'svet'),
(3, 'Спорт', 1, 'sport'),
(4, 'Забава', 1, 'zabava'),
(5, 'Живот', 1, 'zivot'),
(6, 'Технологија', 2, 'tehnologija'),
(7, 'Култура', 2, 'kultura'),
(8, 'Економија', 2, 'ekonomija'),
(9, 'Скопје', 2, 'skopje'),
(10, 'Црна Хроника', 2, 'crna_hronika');

-- --------------------------------------------------------

--
-- Table structure for table `cluster`
--

CREATE TABLE IF NOT EXISTS `cluster` (
`id` int(11) NOT NULL,
  `score` float NOT NULL,
  `master_post` int(11) NOT NULL,
  `category` int(11) NOT NULL,
  `size` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `persons`
--

CREATE TABLE IF NOT EXISTS `persons` (
`id` int(11) NOT NULL,
  `name` int(11) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `persons`
--

INSERT INTO `persons` (`id`, `name`) VALUES
(1, 1),
(2, 2),
(3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE IF NOT EXISTS `posts` (
`id` int(11) NOT NULL,
  `link` varchar(512) COLLATE utf8_bin NOT NULL,
  `cluster` int(11) DEFAULT NULL,
  `category` int(5) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_bin NOT NULL,
  `text` varchar(10024) COLLATE utf8_bin NOT NULL,
  `description` varchar(10024) COLLATE utf8_bin NOT NULL,
  `imageurl` varchar(512) COLLATE utf8_bin DEFAULT NULL,
  `pubdate` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `rssfeeds`
--

CREATE TABLE IF NOT EXISTS `rssfeeds` (
`id` int(11) NOT NULL,
  `source` int(11) NOT NULL,
  `category` int(5) NOT NULL,
  `feed` varchar(512) COLLATE utf8_bin NOT NULL,
  `recode` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `rssfeeds`
--

INSERT INTO `rssfeeds` (`id`, `source`, `category`, `feed`, `recode`) VALUES
(1, 2, 3, 'http://sitel.com.mk/feed/11', 1),
(2, 2, 3, 'http://sitel.com.mk/feed/10', 1),
(3, 2, 3, 'http://sitel.com.mk/feed/9', 1),
(4, 2, 3, 'http://sitel.com.mk/feed/8', 1),
(5, 2, 3, 'http://sitel.com.mk/feed/7', 1),
(6, 2, 3, 'http://sitel.com.mk/feed/6', 1),
(7, 5, 3, 'http://feeds.feedburner.com/kurir/sport/fudbal?format=xml', 1),
(8, 5, 3, 'http://feeds.feedburner.com/kurir/sport/kosarka?format=xml', 1),
(9, 5, 3, 'http://feeds.feedburner.com/kurir/sport/rakomet?format=xml', 1),
(10, 5, 3, 'http://feeds.feedburner.com/kurir/sport/ostanatisportovi?format=xml', 1),
(11, 5, 3, 'http://feeds.feedburner.com/kurir/sport?format=xml', 1),
(12, 7, 3, 'http://kajgana.com/feed/10', 1),
(13, 7, 3, 'http://kajgana.com/feed/11', 1),
(14, 7, 3, 'http://kajgana.com/feed/12', 1),
(15, 7, 3, 'http://kajgana.com/feed/13', 1),
(16, 7, 3, 'http://kajgana.com/feed/14', 1),
(17, 7, 3, 'http://kajgana.com/feed/15', 1),
(18, 8, 3, 'http://tocka.com.mk/rss.php?k=avtomobili', 0),
(19, 8, 3, 'http://tocka.com.mk/rss.php?k=drugi_sportovi', 0),
(20, 8, 3, 'http://tocka.com.mk/rss.php?k=motosport', 0),
(21, 8, 3, 'http://tocka.com.mk/rss.php?k=rakomet', 0),
(22, 8, 3, 'http://tocka.com.mk/rss.php?k=kosarka', 0),
(23, 8, 3, 'http://tocka.com.mk/rss.php?k=fudbal', 0),
(24, 8, 3, 'http://tocka.com.mk/rss.php?k=sport', 0),
(25, 9, 3, 'http://a1on.mk/wordpress/archives/category/sport/formula1/feed', 1),
(26, 9, 3, 'http://a1on.mk/wordpress/archives/category/sport/tennis/feed', 1),
(27, 9, 3, 'http://a1on.mk/wordpress/archives/category/sport/handball/feed', 1),
(28, 9, 3, 'http://a1on.mk/wordpress/archives/category/sport/basketball/feed', 1),
(29, 9, 3, 'http://a1on.mk/wordpress/archives/category/sport/footbal/feed', 1),
(30, 2, 2, 'http://sitel.com.mk/feed/4', 1),
(31, 3, 2, 'http://vecer.mk/feeds/category/4', 1),
(32, 4, 2, 'http://plusinfo.mk/rss/svet', 1),
(33, 5, 2, 'http://feeds.feedburner.com/kurir/svet?format=xml', 1),
(34, 6, 2, 'http://press24.mk/taxonomy/term/6/feed', 1),
(35, 7, 2, 'http://kajgana.com/feed/5', 1),
(36, 8, 2, 'http://tocka.com.mk/rss.php?k=svet', 0),
(37, 9, 2, 'http://a1on.mk/wordpress/archives/category/world/feed', 1),
(38, 10, 2, 'http://novatv.mk/rss.xml?tip=5', 1),
(39, 2, 1, 'http://sitel.com.mk/feed/2', 1),
(40, 3, 1, 'http://vecer.mk/feeds/category/1', 1),
(41, 4, 1, 'http://plusinfo.mk/rss/makedonija', 1),
(42, 5, 1, 'http://feeds.feedburner.com/kurir/republika?format=xml', 1),
(43, 5, 1, 'http://feeds.feedburner.com/kurir/makedonija?format=xml', 1),
(44, 5, 1, 'http://feeds.feedburner.com/kurir/analizi?format=xml', 1),
(45, 5, 1, 'http://feeds.feedburner.com/kurir/kolumni?format=xml', 1),
(46, 6, 1, 'http://press24.mk/taxonomy/term/3/feed', 1),
(47, 7, 1, 'http://kajgana.com/feed/2', 1),
(48, 8, 1, 'http://tocka.com.mk/rss.php?k=makedonija', 0),
(49, 9, 1, 'http://a1on.mk/wordpress/archives/category/macedonia/feed', 1),
(50, 10, 1, 'http://novatv.mk/rss.xml?tip=2', 1),
(51, 10, 1, 'http://novatv.mk/rss.xml?tip=23', 1),
(52, 10, 1, 'http://novatv.mk/rss.xml?tip=16', 1),
(53, 2, 4, 'http://sitel.com.mk/feed/13', 1),
(54, 2, 4, 'http://sitel.com.mk/feed/19', 1),
(55, 3, 4, 'http://vecer.mk/feeds/category/7', 1),
(56, 5, 4, 'http://feeds.feedburner.com/kurir/magazin/zanimlivosti?format=xml', 1),
(57, 8, 4, 'http://tocka.com.mk/rss.php?k=moda_ubavina', 0),
(58, 8, 4, 'http://tocka.com.mk/rss.php?k=film', 0),
(59, 8, 4, 'http://tocka.com.mk/rss.php?k=muzika', 0),
(60, 8, 4, 'http://tocka.com.mk/rss.php?k=patuvanje', 0),
(61, 8, 4, 'http://tocka.com.mk/rss.php?k=zabava', 0),
(62, 9, 4, 'http://a1on.mk/wordpress/archives/category/fun/fashion-fun/feed', 1),
(63, 9, 4, 'http://a1on.mk/wordpress/archives/category/fun/traveling/feed', 1),
(64, 9, 4, 'http://a1on.mk/wordpress/archives/category/fun/feed', 1),
(65, 2, 5, 'http://sitel.com.mk/feed/14', 1),
(66, 2, 5, 'http://sitel.com.mk/feed/16', 1),
(67, 2, 5, 'http://sitel.com.mk/feed/15', 1),
(68, 3, 7, 'http://vecer.mk/feeds/category/5', 1),
(69, 3, 5, 'http://vecer.mk/feeds/category/9', 1),
(70, 4, 5, 'http://plusinfo.mk/rss/zdravje', 1),
(71, 4, 5, 'http://plusinfo.mk/rss/scena', 1),
(72, 4, 7, 'http://plusinfo.mk/rss/kultura', 1),
(73, 5, 5, 'http://feeds.feedburner.com/kurir/magazin/scena?format=xml', 1),
(74, 5, 5, 'http://feeds.feedburner.com/kurir/magazin/zivot?format=xml', 1),
(75, 5, 7, 'http://feeds.feedburner.com/kurir/makedonija/kultura?format=xml', 1),
(76, 6, 5, 'http://press24.mk/taxonomy/term/26/feed', 1),
(77, 6, 5, 'http://press24.mk/taxonomy/term/70/feed', 1),
(78, 7, 7, 'http://kajgana.com/feed/8', 1),
(79, 7, 7, 'http://kajgana.com/feed/23', 1),
(80, 8, 5, 'http://tocka.com.mk/rss.php?k=showbiz', 0),
(81, 8, 5, 'http://tocka.com.mk/rss.php?k=erotika', 0),
(82, 8, 5, 'http://tocka.com.mk/rss.php?k=kulinarstvo', 0),
(83, 8, 5, 'http://tocka.com.mk/rss.php?k=zdravje', 0),
(84, 8, 5, 'http://tocka.com.mk/rss.php?k=ljubov_seks', 0),
(85, 8, 5, 'http://tocka.com.mk/rss.php?k=patuvanje', 0),
(86, 8, 5, 'http://tocka.com.mk/rss.php?k=zivot', 0),
(87, 9, 7, 'http://a1on.mk/wordpress/archives/category/fun/culture/feed', 1),
(88, 9, 5, 'http://a1on.mk/wordpress/archives/category/fun/jetset/feed', 1),
(89, 9, 5, 'http://a1on.mk/wordpress/archives/category/fun/traveling/feed', 1),
(90, 10, 7, 'http://novatv.mk/rss.xml?tip=4', 1),
(91, 10, 5, 'http://novatv.mk/rss.xml?tip=1', 1),
(92, 2, 6, 'http://sitel.com.mk/feed/18', 1),
(93, 5, 6, 'http://feeds.feedburner.com/kurir/magazin/tehnologija?format=xml', 1),
(94, 6, 6, 'http://press24.mk/taxonomy/term/7/feed', 1),
(95, 8, 6, 'http://tocka.com.mk/rss.php?k=planeta', 0),
(96, 9, 6, 'http://a1on.mk/wordpress/archives/category/technology/feed', 1),
(97, 2, 8, 'http://sitel.com.mk/feed/5', 1),
(98, 3, 8, 'http://vecer.mk/feeds/category/2', 1),
(99, 4, 8, 'http://plusinfo.mk/rss/biznis', 1),
(100, 5, 8, 'http://feeds.feedburner.com/kurir/svet/biznis?format=xml', 1),
(101, 5, 8, 'http://feeds.feedburner.com/kurir/makedonija/ekonomija?format=xml', 1),
(102, 6, 8, 'http://press24.mk/taxonomy/term/4/feed', 1),
(103, 7, 8, 'http://kajgana.com/feed/6', 1),
(104, 9, 8, 'http://a1on.mk/wordpress/archives/category/economy/feed', 1),
(105, 10, 8, 'http://novatv.mk/rss.xml?tip=7', 1),
(106, 3, 9, 'http://vecer.mk/feeds/category/3', 1),
(107, 4, 9, 'http://plusinfo.mk/rss/skopje', 1),
(108, 5, 9, 'http://feeds.feedburner.com/kurir/republika/skopje?format=xml', 1),
(109, 6, 9, 'http://press24.mk/taxonomy/term/25/feed', 1),
(110, 5, 10, 'http://feeds.feedburner.com/kurir/makedonija/crnahronika?format=xml', 1),
(111, 6, 10, 'http://press24.mk/taxonomy/term/13/feed', 1),
(112, 7, 10, 'http://kajgana.com/feed/7', 1),
(113, 2, 2, 'http://sitel.com.mk/feed/3', 1),
(114, 3, 2, 'http://vecer.mk/feeds/category/10', 1),
(115, 5, 2, 'http://feeds.feedburner.com/kurir/svet/region?format=xml', 1),
(116, 6, 2, 'http://press24.mk/taxonomy/term/11/feed', 1),
(117, 7, 2, 'http://kajgana.com/feed/3', 1),
(118, 8, 2, 'http://tocka.com.mk/rss.php?k=region', 0),
(119, 1, 1, 'http://kanal5.com.mk/rss/vestixml-makedonija.asp', 1),
(120, 1, 2, 'http://kanal5.com.mk/rss/vestixml-svet.asp', 1),
(121, 1, 5, 'http://kanal5.com.mk/rss/vestixml-zivot.asp', 1),
(122, 1, 7, 'http://kanal5.com.mk/rss/vestixml-kultura.asp', 1),
(123, 1, 4, 'http://kanal5.com.mk/rss/vestixml-zabava.asp', 1),
(124, 1, 5, 'http://kanal5.com.mk/rss/vestixml-soubiznis.asp', 1),
(125, 1, 3, 'http://kanal5.com.mk/rss/sportxml-drugi.asp', 1),
(126, 1, 3, 'http://kanal5.com.mk/rss/sportxml-skijanje.asp', 1),
(127, 1, 3, 'http://kanal5.com.mk/rss/sportxml-tenis.asp', 1),
(128, 1, 3, 'http://kanal5.com.mk/rss/sportxml-formula.asp', 1),
(129, 1, 3, 'http://kanal5.com.mk/rss/sportxml-rakomet.asp', 1),
(130, 1, 3, 'http://kanal5.com.mk/rss/sportxml-nba.asp', 1),
(131, 1, 3, 'http://kanal5.com.mk/rss/sportxml-kosarka.asp', 1),
(132, 1, 3, 'http://kanal5.com.mk/rss/sportxml-fudbal.asp', 1);

-- --------------------------------------------------------

--
-- Table structure for table `sources`
--

CREATE TABLE IF NOT EXISTS `sources` (
`id` int(11) NOT NULL,
  `website` varchar(255) COLLATE utf8_bin NOT NULL,
  `contentFlag` tinyint(4) NOT NULL,
  `contentselector` varchar(255) COLLATE utf8_bin NOT NULL,
  `imageFlag` tinyint(4) NOT NULL,
  `imageselector` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `sources`
--

INSERT INTO `sources` (`id`, `website`, `contentFlag`, `contentselector`, `imageFlag`, `imageselector`) VALUES
(1, 'Канал 5', 0, 'div.entry div:not(.fb-like-box):not(.post_carousel)', 0, 'div.entry div.frame_box img'),
(2, 'Сител', 0, 'div.content div.field-item', 0, 'div.content div.field-item img:first-child'),
(3, 'Вечер', 0, 'div.region.region-75.region-first article div.content', 0, 'div.region.region-75.region-first article div.content img:first-child'),
(4, 'Плусинфо', 0, 'div.glavna_text', 0, '#MainContent_imgVest'),
(5, 'Курир', 0, '#component div.article h2, #component div.article p', 0, 'div.article img:first-child'),
(6, 'Прес24', 0, 'div.field-name-body div.field-item.even', 0, 'div.content div.field-item img:first-child'),
(7, 'Кајгана', 0, 'div.content div.field-item.even', 0, 'div.content div.field-item.even img:first-child'),
(8, 'Точка', 0, '#sodrzina_vest', 0, '#td_body_levo table:nth-of-type(3) img:first-child'),
(9, 'А1он', 0, 'div.entry-content div.post p', 0, 'div.entry-content div.post div.single-post-img img:first-child'),
(10, 'НоваТВ', 0, 'div.content p.news_text', 0, 'div.content div.news_video img:first-child');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_cas`
--
ALTER TABLE `auth_cas`
 ADD PRIMARY KEY (`id`), ADD KEY `user_id__idx` (`user_id`);

--
-- Indexes for table `auth_event`
--
ALTER TABLE `auth_event`
 ADD PRIMARY KEY (`id`), ADD KEY `user_id__idx` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_membership`
--
ALTER TABLE `auth_membership`
 ADD PRIMARY KEY (`id`), ADD KEY `user_id__idx` (`user_id`), ADD KEY `group_id__idx` (`group_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
 ADD PRIMARY KEY (`id`), ADD KEY `group_id__idx` (`group_id`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cluster`
--
ALTER TABLE `cluster`
 ADD PRIMARY KEY (`id`), ADD KEY `master_post` (`master_post`), ADD KEY `category` (`category`);

--
-- Indexes for table `persons`
--
ALTER TABLE `persons`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
 ADD PRIMARY KEY (`id`), ADD KEY `cluster` (`cluster`), ADD KEY `category` (`category`), ADD KEY `source` (`source`);

--
-- Indexes for table `rssfeeds`
--
ALTER TABLE `rssfeeds`
 ADD PRIMARY KEY (`id`), ADD KEY `source` (`source`), ADD KEY `category` (`category`);

--
-- Indexes for table `sources`
--
ALTER TABLE `sources`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_cas`
--
ALTER TABLE `auth_cas`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_event`
--
ALTER TABLE `auth_event`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_membership`
--
ALTER TABLE `auth_membership`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
MODIFY `id` int(5) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `cluster`
--
ALTER TABLE `cluster`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `persons`
--
ALTER TABLE `persons`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `rssfeeds`
--
ALTER TABLE `rssfeeds`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=133;
--
-- AUTO_INCREMENT for table `sources`
--
ALTER TABLE `sources`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_cas`
--
ALTER TABLE `auth_cas`
ADD CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_event`
--
ALTER TABLE `auth_event`
ADD CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_membership`
--
ALTER TABLE `auth_membership`
ADD CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
ADD CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `cluster`
--
ALTER TABLE `cluster`
ADD CONSTRAINT `fk_cluster_category` FOREIGN KEY (`category`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `fk_master_post` FOREIGN KEY (`master_post`) REFERENCES `posts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
ADD CONSTRAINT `fk_posts_category` FOREIGN KEY (`category`) REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
ADD CONSTRAINT `fk_posts_cluster` FOREIGN KEY (`cluster`) REFERENCES `cluster` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
ADD CONSTRAINT `fk_posts_source` FOREIGN KEY (`source`) REFERENCES `sources` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `rssfeeds`
--
ALTER TABLE `rssfeeds`
ADD CONSTRAINT `fk_rssfeeds_categories` FOREIGN KEY (`category`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `fk_rssfeeds_sources` FOREIGN KEY (`source`) REFERENCES `sources` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

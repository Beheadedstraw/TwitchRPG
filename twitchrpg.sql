-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 16, 2018 at 04:33 AM
-- Server version: 5.7.19
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `twitchrpg`
--

-- --------------------------------------------------------

--
-- Table structure for table `characters`
--

DROP TABLE IF EXISTS `characters`;
CREATE TABLE IF NOT EXISTS `characters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `level` int(11) NOT NULL,
  `energy` int(11) NOT NULL,
  `skillPoints` int(11) NOT NULL,
  `currentXP` int(11) NOT NULL,
  `levelXP` int(11) NOT NULL,
  `hp` int(11) NOT NULL,
  `maxHP` int(11) NOT NULL,
  `mana` int(11) NOT NULL,
  `maxMana` int(11) NOT NULL,
  `str` int(11) NOT NULL,
  `wis` int(11) NOT NULL,
  `vit` int(11) NOT NULL,
  `weapon` int(11) NOT NULL,
  `shield` int(11) NOT NULL,
  `armor` int(11) NOT NULL,
  `inCombat` int(11) NOT NULL COMMENT 'bool (1/0) if character is in combat.',
  `inCombatID` int(11) NOT NULL COMMENT 'ID of the Combat row that contains the battle data.',
  `location` int(11) NOT NULL,
  `whisperMode` int(11) NOT NULL,
  `inventory` text NOT NULL,
  `money` bigint(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `characters`
--

INSERT INTO `characters` (`id`, `name`, `level`, `energy`, `skillPoints`, `currentXP`, `levelXP`, `hp`, `maxHP`, `mana`, `maxMana`, `str`, `wis`, `vit`, `weapon`, `shield`, `armor`, `inCombat`, `inCombatID`, `location`, `whisperMode`, `inventory`, `money`) VALUES
(1, 'beheadedstraw', 2, 10, 6, 0, 20, 20, 20, 10, 5, 1, 1, 1, 2, 3, 1, 0, 0, 2, 0, '1,2,3', 8),
(2, 'blueshadowz03', 2, 10, 0, 0, 20, 20, 40, 10, 10, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, '1,2,3', 0),
(32, 'greymanerealms', 2, 10, 0, 3, 20, 16, 40, 10, 10, 1, 1, 1, 2, 3, 1, 0, 0, 4, 0, '1,2,3', 0),
(33, 'cmdr_lorentius', 1, 10, 0, 0, 20, 20, 20, 5, 5, 1, 1, 1, 2, 3, 1, 0, 0, 3, 1, '1,2,3', 0);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
CREATE TABLE IF NOT EXISTS `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `type` int(11) NOT NULL,
  `damage` int(11) NOT NULL,
  `armor` int(11) NOT NULL,
  `str` int(11) NOT NULL,
  `vit` int(11) NOT NULL,
  `wis` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `name`, `description`, `type`, `damage`, `armor`, `str`, `vit`, `wis`) VALUES
(1, 'Basic Cloth Armor', 'Your basic rags that you start out with in every other RPG you\'ve played.', 1, 0, 1, 0, 0, 0),
(2, 'Butter Knife', 'It\'s a butter knife. You use it to spread butter... and kill things... very... very slowly.', 2, 1, 0, 0, 0, 0),
(3, 'Basic Wooden Shield', 'It\'s a Basic Wood shield... what else did you expect?', 3, 0, 1, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
CREATE TABLE IF NOT EXISTS `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) NOT NULL,
  `hasMonsters` int(11) NOT NULL,
  `maxMonsterLevel` int(11) NOT NULL,
  `north` int(11) NOT NULL,
  `south` int(11) NOT NULL,
  `east` int(11) NOT NULL,
  `west` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `location_id`, `name`, `description`, `hasMonsters`, `maxMonsterLevel`, `north`, `south`, `east`, `west`) VALUES
(1, 1, 'Southshire', 'Full of patrons young and old, the Bar of Twitch is the main gathering of all the adventurers of the land. To the south is an exit to the market.', 0, 2, 0, 2, 0, 3),
(2, 2, 'Southshire Vineyards', 'The Twitch Market is where new and old adventurers alike buy and sell their goods they get from monsters they slay. To the north is the bar, to the south is the practice grounds and to the east is the Fields of Plains.', 1, 2, 1, 0, 0, 0),
(3, 3, 'Southshire Valley', 'The Practice Grounds are where you can practice your battle tactics and spell casting without fear of dying. To the north is the market.', 1, 2, 4, 6, 1, 0),
(4, 4, 'Windstorm City', 'Plains as far the eye can see! All types of creatures live here, including sickly ones that may have to be put our of their misery. To the west is the Twitch Market, and to the East is the small town of Whatchacallit.', 0, 0, 0, 3, 0, 5),
(5, 5, 'Stockades', 'Whatchamcallit is a small town with it\'s own small town problems. It has a broken down inn and a couple of shops. Maybe you can talk to some people and do some work? To the west is the Field of Plains.', 1, 0, 0, 0, 4, 0),
(6, 6, 'Silvershire', 'Travelers, merchants, adventurers, Windstorm guards, and priests from the abbey all stop and make regular visits to the town on their way to and from Windstorm, usually enjoying the hospitality of the Lion\'s Pride Inn, one of the most respectable ale houses in Azurath.', 0, 0, 3, 17, 8, 7),
(7, 8, 'Obsidian Lake', 'Obsidian Lake is a lake, located directly east of Silvershire in Belwynne Forest. It is crawling with gurlocs, and may be quite dangerous for the inexperienced adventurer.', 1, 4, 0, 16, 9, 6),
(8, 9, 'Azure Tower', 'The Azure Tower is a small mage tower in eastern Belwynne Forest. The tower is run by a number of servants of Azura, who all appear to be Gnomish, and who are in turn presided over by the Archmage of Azura, Bob. The denizens of the tower are in a constant feud with the inhabitants of the Galor Tower in Blueridge Mountains, ruled over by the evil sorcerer Morgan. The two towers are constantly spying on one another through magical means.', 1, 5, 0, 15, 10, 8),
(9, 10, 'Northvale Logging Camp', 'Because of its location in more hostile wilderness, wild animals are proving to be troublesome. Wolves and bears in the area have become a menace, chasing off workers and threatening to cause delays in delivery deadlines. The problem has become significant enough that the Windstorm Guard has become involved, recruiting adventurers to collect abandoned lumber and eradicate some of the aggressive wildlife.', 1, 6, 11, 14, 13, 9),
(10, 11, 'Pebble Cairn Pond', 'Pebble Cairn Pond is situated in northeastern Belwynne Forest, and holds one large island that gives the lake a characteristic ring shape. The lake is named after Heroes\' Statue, the pebble cairn monument erected upon the island to commemorate the huge loss of life during the First War against the orcs.', 1, 6, 12, 10, 0, 0),
(11, 12, 'Heroes\' Statue', 'Heroes\' Statue is the central area of the Pebble Cairn Lake island in eastern Belwynne Forest. It features a ring of stones, and a monument called the Stone of Remembrance which commemorates the dead from the orcs\' sacking of Silvershire and other nearby regions during the First War.\r\n\r\nThe island itself is controlled by Defiant Rogue Wizards who can be quite dangerous to inexperienced adventurers.', 1, 7, 0, 11, 0, 0),
(12, 13, 'Tri-Corners', 'Tri-Corners is the pathway that connects Muskwood, Blueridge Mountains and Belwynne Forest. Adventurers are reminded to take care when traveling due to the multitude of Defiant, Orcs, and Undead that are nearby.', 1, 8, 0, 0, 21, 10),
(13, 14, 'Ridgepoint Tower', 'Ridgepoint Tower is one of the guard towers constructed in Belwynne Forest after the Second War. These towers are well defended against any enemies who encroach into Human lands. Ridgepoint in particular serves as a watchpost against encroachment by gnolls and orcs from Blueridge Mountains, undead from Muskwood, as well as Defiant from nearby camps.', 1, 7, 10, 0, 0, 15),
(14, 15, 'Brackwell Melon Patch', 'Brackwell Melon Patch lies in southeast Belwynne Forest. It has been taken over by the Defiant Brotherhood and their agents patrol the two buildings. The smaller house also houses Morgan the Collector, Earl Drudge and Selena Caldon.', 1, 6, 9, 0, 14, 16),
(15, 16, 'Maclure\'s Farm', 'The Maclure Farms, located in southern Belwynne Forest, belong to the Maclure Family. The Maclures are in a bitter rivalry with the nearby Stonefield Family, but despite their intense dislike of each other, a child from both families has fallen in love with each other in true Romeo and Juliet fashion. There is hope their love can bring the two families together, and there are several quests that involve the feuding families. ', 1, 5, 8, 0, 15, 17),
(16, 17, 'Fargo Mine', 'The Fargo Mine is an abandoned gold mine located in Belwynne Forest, which has been overrun by kobolds.', 1, 5, 6, 19, 16, 18),
(17, 18, 'Forest\'s Edge', 'Forest\'s Edge is a peninsula-like swath of forest southwest of Windstorm City, located between Flat Lake Orchard, the Nazeriti River and the small northern river near Westclimb.', 1, 8, 7, 0, 17, 20),
(18, 7, 'Flat Lake Orchard', 'Flat Lake Orchard is situated in western Belwynne Forest, on the southern banks of Flat Lake. Although the trees growing here used to produce fresh fruit, they have all been picked and eaten by Defiant Bandits who have taken possession of the orchard as well as the nearby cottage where their local captain, Tim the Sly resides. Whoever lived here is long gone, another victim of the growing banditry in the region.', 1, 5, 0, 18, 6, 0),
(19, 19, 'Stonepatch Farm', 'The Stonepatch Farm is one of two rival farmsteads in southern Belwynne Forest. The Stonepatch family is in a bitter rivalry with the nearby Maclure family. Despite their intense dislike of each other, a child from each family has fallen in love with one another in true \"Romeo and Juliet\" fashion. There is hope their love can bring the two families together and, to that end, there are several quests that involve the feuding families.', 1, 7, 17, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `monsters`
--

DROP TABLE IF EXISTS `monsters`;
CREATE TABLE IF NOT EXISTS `monsters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `level` int(11) NOT NULL,
  `hp` int(11) NOT NULL,
  `damage` int(11) NOT NULL,
  `xp` int(11) NOT NULL,
  `loot` varchar(0) NOT NULL,
  `money` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `monsters`
--

INSERT INTO `monsters` (`id`, `name`, `level`, `hp`, `damage`, `xp`, `loot`, `money`) VALUES
(1, 'Rabid Squirrel', 1, 10, 2, 3, '', 2),
(2, 'Sickly Deer', 1, 5, 1, 2, '', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

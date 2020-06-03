-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 02, 2020 at 03:59 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `todo`
--

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `task` mediumtext NOT NULL,
  `category` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `description` longtext NOT NULL,
  `files` mediumtext NOT NULL,
  `status` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`id`, `email`, `task`, `category`, `date`, `description`, `files`, `status`) VALUES
(1, 'mouryasiddharth8@gmail.com', 'Get a haircut ', 'Home', '2020-05-31', 'I will get a haircut like shahid some day and i have set a reminder .', '|30-05-2020-19-13-280', 'no'),
(6, 'pareekdhiraj97@gmail.com', 'go to gym', 'Home', '2020-05-31', '', '', 'no'),
(11, 'mouryasiddharth8@gmail.com', 'make  corona tracker', 'Others', '2020-06-03', 'I have to make a corona tracker using covid19api.org and and android app with that.', '|31-05-2020-13-54-490|31-05-2020-13-54-491', 'no'),
(12, 'mouryasiddharth8@gmail.com', 'Submit this website project', 'Office', '2020-06-02', 'This is a project that i have made as a part of contest named stackhack 1.0 hosted by hackerEarth Many students are taking part in it and hacking to develop amazing web app.', '|01-06-2020-09-52-330|01-06-2020-09-52-331|01-06-2020-09-52-332', 'yes'),
(13, 'mouryasiddharth8@gmail.com', 'I have to visit a gym some day maybe tomorrow ', 'Others', '2020-06-02', '\"Gym\" is also slang for \"fitness centre\", which is often an area for indoor recreation. A gym may be open air as well.', '|01-06-2020-10-02-310|01-06-2020-10-02-311|01-06-2020-10-02-312', 'no'),
(14, 'mouryasiddharth8@gmail.com', 'Go for  a walk tommorow', 'Home', '2020-06-02', 'Walking can help your mental health. Studies show it can help reduce anxiety, depression, and a negative mood. It can also boost self-esteem and reduce symptoms of social withdrawal.', '|01-06-2020-10-04-570|01-06-2020-10-04-571', 'no'),
(15, 'mouryasiddharth8@gmail.com', 'Get a new book for my office', 'Office', '2020-06-05', 'Reading lists begin as a shelf full of hope until the year flies by, and you find yourself flooded with procrastination. ', '|01-06-2020-10-07-430', 'no'),
(16, 'mouryasiddharth8@gmail.com', 'got a work to do for office ', 'Office', '2020-06-04', '“Be nice to nerds. “The Seven Social Sins are: “Some women choose to follow men, and some women choose to follow their dreams. ', '|01-06-2020-10-09-190|01-06-2020-10-09-191', 'no'),
(17, 'mouryasiddharth8@gmail.com', 'Buy my mother some jaggery for ladoos', 'Home', '2020-06-03', 'Laddu or laddoo or avinsh is a sphere-shaped sweet originating from the Indian subcontinent; the name originated from the Sanskrit word Lattika.', '|01-06-2020-10-11-180|01-06-2020-10-11-181', 'no'),
(18, 'mouryasiddharth8@gmail.com', 'I have to buy myself  a mask as it is corona time', 'Drugs', '2020-06-07', 'WHO\'s guidance and advice on the use of masks to protect against and limit the spread of COVID-19.', '|01-06-2020-10-13-020', 'yes'),
(19, 'mouryasiddharth8@gmail.com', 'MY friends birthday is coming', 'Social', '2020-06-01', 'A birthday is the anniversary of the birth of a person, or figuratively of an institution. Birthdays of people are celebrated in numerous cultures', '|01-06-2020-10-15-560|01-06-2020-10-15-561', 'no'),
(20, 'mouryasiddharth8@gmail.com', 'I have to plant trees', 'Home', '2020-06-01', 'Tree-planting is the process of transplanting tree seedlings, generally for forestry, land reclamation, or landscaping purpose', '|01-06-2020-10-17-090', 'yes'),
(21, 'mouryasiddharth8@gmail.com', 'Buy sugar', 'Groceries', '2020-06-01', 'Hey my mom is making ladoo i have to buy a sugar', '|01-06-2020-10-18-030', 'yes'),
(22, 'mouryasiddharth8@gmail.com', 'I have remind my friend for PSK', 'Social', '2020-06-01', 'Reminder for my friend and how are you this is just a test text nothing more than that', '|01-06-2020-10-19-180', 'no'),
(23, 'mouryasiddharth8@gmail.com', 'Buy some groceries from DMART ', 'Groceries', '2020-06-07', 'Dals & Pulses (36) Salt / Sugar / Jaggery (9) Rice & Rice Products (16) Rice & Rice Products. Rice. Dry Fruits (22) Masala & Spices (49) Flours & Grains (16) Cooking Oil & Ghee (2)', '|01-06-2020-10-21-330|01-06-2020-10-21-331|01-06-2020-10-21-332|01-06-2020-10-21-333', 'no'),
(24, 'mouryasiddharth8@gmail.com', 'Remind my office guard to come for a birthday party ', 'Office', '2020-06-05', 'A birthday is the anniversary of the birth of a person, or figuratively of an institution. Birthdays of people are celebrated in numerous cultures, often with birthday ...', '|01-06-2020-10-22-580', 'no'),
(25, 'mouryasiddharth8@gmail.com', 'I have to boook phone on 5th ', 'Home', '2020-06-05', 'Find here the list of all mobile phones brands of India and Worldwide, Also check latest smartphones from top & best company like Samsung, Apple, Xiaomi, ...\r\n', '|01-06-2020-10-24-310|01-06-2020-10-24-311', 'no'),
(26, 'mouryasiddharth8@gmail.com', 'Have to buy my mothers meds', 'Drugs', '2020-06-04', 'Cyblex M40\r\nTelmikind 40 \r\njoint plus\r\nlupical 500\r\nmetsmall 1000mg', '|01-06-2020-10-26-510', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int(10) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(30) NOT NULL,
  `hashedpwd` longtext NOT NULL,
  `salt` mediumtext NOT NULL,
  `phone` varchar(12) NOT NULL,
  `category` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `name`, `email`, `hashedpwd`, `salt`, `phone`, `category`) VALUES
(5, 'Siddharth Mourya', 'mouryasiddharth8@gmail.com', '$2b$12$qKZ.O23H8IS9o7ROieCtyOaxpXBbJ1wyNxBgrU8x7z2VfwCyQaV.q', '$2b$12$qKZ.O23H8IS9o7ROieCtyO', '7415274813', '|Groceries|Office|Home|Drugs|Others'),
(6, 'Shubham Sharma', 'shubhsharma5055@gmail.com', '$2b$12$Euy99L23ZAD0MobSgMXBi./h0/kgG9evb1CCq3rBtyEz0Y.ryz6vW', '$2b$12$Euy99L23ZAD0MobSgMXBi.', '8319091155', '|Groceries|Office|Home|Drugs|Others'),
(7, 'dhiraj pareek', 'pareekdhiraj97@gmail.com', '$2b$12$0V/bfQCHK2YBXyDSRjnEKenUwXxKurmbpLISHYRqsAY4TCo5SnVfi', '$2b$12$0V/bfQCHK2YBXyDSRjnEKe', '8839322677', '|Groceries|Office|Home|Drugs|Others');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

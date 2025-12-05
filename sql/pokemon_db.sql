-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 05/12/2025 às 04:12
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `pokemon_db`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `pokemon`
--

CREATE TABLE `pokemon` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `imagem_url` varchar(255) DEFAULT NULL,
  `altura` decimal(5,2) DEFAULT NULL,
  `peso` decimal(5,2) DEFAULT NULL,
  `evolucao` varchar(100) DEFAULT NULL,
  `hp` int(11) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `special_attack` int(11) DEFAULT NULL,
  `special_defense` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `pokemon`
--

INSERT INTO `pokemon` (`id`, `nome`, `imagem_url`, `altura`, `peso`, `evolucao`, `hp`, `attack`, `defense`, `special_attack`, `special_defense`, `speed`) VALUES
(1, 'bulbasaur', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png', 7.00, 69.00, 'ivysaur', 45, 49, 49, 65, 65, 45),
(4, 'charmander', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png', 6.00, 85.00, 'charmeleon', 39, 52, 43, 60, 50, 65),
(6, 'charizard', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png', 17.00, 905.00, NULL, 78, 84, 78, 109, 85, 100),
(7, 'squirtle', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png', 5.00, 90.00, 'wartortle', 44, 48, 65, 50, 64, 43),
(9, 'blastoise', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png', 16.00, 855.00, NULL, 79, 83, 100, 85, 105, 78),
(25, 'pikachu', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png', 4.00, 60.00, 'raichu', 35, 55, 40, 50, 50, 90),
(39, 'jigglypuff', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png', 5.00, 55.00, 'wigglytuff', 115, 45, 20, 45, 25, 20),
(59, 'arcanine', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/59.png', 19.00, 999.99, NULL, 90, 110, 80, 100, 80, 95),
(94, 'gengar', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png', 15.00, 405.00, NULL, 60, 65, 60, 130, 75, 110),
(129, 'magikarp', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/129.png', 9.00, 100.00, 'gyarados', 20, 10, 55, 15, 20, 80),
(131, 'lapras', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/131.png', 25.00, 999.99, NULL, 130, 85, 80, 85, 95, 60),
(133, 'eevee', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png', 3.00, 65.00, 'vaporeon', 55, 55, 50, 45, 65, 55),
(134, 'vaporeon', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/134.png', 10.00, 290.00, NULL, 130, 65, 60, 110, 95, 65),
(135, 'jolteon', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/135.png', 8.00, 245.00, NULL, 65, 65, 60, 110, 95, 130),
(143, 'snorlax', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png', 21.00, 999.99, NULL, 160, 110, 65, 65, 110, 30),
(149, 'dragonite', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/149.png', 22.00, 999.99, NULL, 91, 134, 95, 100, 100, 80),
(150, 'mewtwo', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png', 20.00, 999.99, NULL, 106, 110, 90, 154, 90, 130),
(151, 'mew', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png', 4.00, 40.00, NULL, 100, 100, 100, 100, 100, 100),
(175, 'togepi', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/175.png', 3.00, 15.00, 'togetic', 35, 20, 65, 40, 65, 20),
(196, 'espeon', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/196.png', 9.00, 265.00, NULL, 65, 65, 60, 130, 95, 110),
(197, 'umbreon', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/197.png', 10.00, 270.00, NULL, 95, 65, 110, 60, 130, 65),
(257, 'blaziken', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/257.png', 19.00, 520.00, NULL, 80, 120, 70, 110, 70, 80),
(282, 'gardevoir', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/282.png', 16.00, 484.00, NULL, 68, 65, 65, 125, 115, 80),
(384, 'rayquaza', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/384.png', 70.00, 999.99, NULL, 105, 150, 90, 150, 90, 95),
(445, 'garchomp', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/445.png', 19.00, 950.00, NULL, 108, 130, 95, 80, 85, 102),
(448, 'lucario', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/448.png', 12.00, 540.00, NULL, 70, 110, 70, 115, 70, 90),
(658, 'greninja', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/658.png', 15.00, 400.00, NULL, 72, 95, 67, 103, 71, 122),
(700, 'sylveon', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/700.png', 10.00, 235.00, NULL, 95, 65, 65, 110, 130, 60);

-- --------------------------------------------------------

--
-- Estrutura para tabela `pokemon_tipo`
--

CREATE TABLE `pokemon_tipo` (
  `pokemon_id` int(11) NOT NULL,
  `tipo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `pokemon_tipo`
--

INSERT INTO `pokemon_tipo` (`pokemon_id`, `tipo_id`) VALUES
(1, 4),
(1, 12),
(4, 10),
(6, 3),
(6, 10),
(7, 11),
(9, 11),
(25, 13),
(39, 1),
(39, 18),
(59, 10),
(94, 4),
(94, 8),
(129, 11),
(131, 11),
(131, 15),
(133, 1),
(134, 11),
(135, 13),
(143, 1),
(149, 3),
(149, 16),
(150, 14),
(151, 14),
(175, 18),
(196, 14),
(197, 17),
(257, 2),
(257, 10),
(282, 14),
(282, 18),
(384, 3),
(384, 16),
(445, 5),
(445, 16),
(448, 2),
(448, 9),
(658, 11),
(658, 17),
(700, 18);

-- --------------------------------------------------------

--
-- Estrutura para tabela `tipo`
--

CREATE TABLE `tipo` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tipo`
--

INSERT INTO `tipo` (`id`, `nome`) VALUES
(7, 'bug'),
(17, 'dark'),
(16, 'dragon'),
(13, 'electric'),
(18, 'fairy'),
(2, 'fighting'),
(10, 'fire'),
(3, 'flying'),
(8, 'ghost'),
(12, 'grass'),
(5, 'ground'),
(15, 'ice'),
(1, 'normal'),
(4, 'poison'),
(14, 'psychic'),
(6, 'rock'),
(9, 'steel'),
(19, 'stellar'),
(20, 'unknown'),
(11, 'water');

-- --------------------------------------------------------

--
-- Estrutura para tabela `treinador`
--

CREATE TABLE `treinador` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `cpf` char(11) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `treinador`
--

INSERT INTO `treinador` (`id`, `nome`, `email`, `cpf`, `foto`, `cidade`) VALUES
(1, 'becker', 'lucas.gabriel.becker.08@gmail.com', '123', 'https://media.istockphoto.com/id/177228186/pt/foto/jovem-capivara.jpg?s=612x612&w=0&k=20&c=HIaHC5JhfE3zobczCLIEY6bdy2NdOLq0sskZkuXsM9w=', 'Teste');

-- --------------------------------------------------------

--
-- Estrutura para tabela `treinador_pokemon`
--

CREATE TABLE `treinador_pokemon` (
  `id` int(11) NOT NULL,
  `treinador_id` int(11) NOT NULL,
  `pokemon_id` int(11) NOT NULL,
  `local` enum('time','box') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `pokemon`
--
ALTER TABLE `pokemon`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `pokemon_tipo`
--
ALTER TABLE `pokemon_tipo`
  ADD PRIMARY KEY (`pokemon_id`,`tipo_id`),
  ADD KEY `tipo_id` (`tipo_id`);

--
-- Índices de tabela `tipo`
--
ALTER TABLE `tipo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Índices de tabela `treinador`
--
ALTER TABLE `treinador`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `cpf` (`cpf`);

--
-- Índices de tabela `treinador_pokemon`
--
ALTER TABLE `treinador_pokemon`
  ADD PRIMARY KEY (`id`),
  ADD KEY `treinador_id` (`treinador_id`),
  ADD KEY `pokemon_id` (`pokemon_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `pokemon`
--
ALTER TABLE `pokemon`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=701;

--
-- AUTO_INCREMENT de tabela `tipo`
--
ALTER TABLE `tipo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de tabela `treinador`
--
ALTER TABLE `treinador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `treinador_pokemon`
--
ALTER TABLE `treinador_pokemon`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `pokemon_tipo`
--
ALTER TABLE `pokemon_tipo`
  ADD CONSTRAINT `pokemon_tipo_ibfk_1` FOREIGN KEY (`pokemon_id`) REFERENCES `pokemon` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pokemon_tipo_ibfk_2` FOREIGN KEY (`tipo_id`) REFERENCES `tipo` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `treinador_pokemon`
--
ALTER TABLE `treinador_pokemon`
  ADD CONSTRAINT `treinador_pokemon_ibfk_1` FOREIGN KEY (`treinador_id`) REFERENCES `treinador` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `treinador_pokemon_ibfk_2` FOREIGN KEY (`pokemon_id`) REFERENCES `pokemon` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

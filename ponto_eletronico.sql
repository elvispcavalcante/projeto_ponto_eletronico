CREATE DATABASE ponto_eletronico;
USE ponto_eletronico;

CREATE TABLE horarios_trabalho(
	id_horario int auto_increment not null,
    descricao_horario varchar(100) not null,
    horario_inicial_manha time, 
    horario_final_manha time,
    horario_inicial_tarde time,
    horario_final_tarde time,
    primary key (id_horario)
);
INSERT INTO horarios_trabalho (descricao_horario, horario_inicial_manha, 
horario_final_manha, horario_inicial_tarde, horario_final_tarde) 
VALUES ('Horário Normal - 8hs - 08hs as 12hs / 13hs as 17hs', 
'08:00:00', '12:00:00', '13:00', '17:00');

CREATE TABLE funcionarios (
	id_funcionario int auto_increment not null,
    nome varchar(120) not null,
    cpf varchar(11) not null,
    matricula varchar(15) not null,
    pis_pasep varchar(15),
    id_horario int not null,
    PRIMARY KEY (id_funcionario),
    CONSTRAINT fk_horario FOREIGN KEY (id_horario) REFERENCES horarios_trabalho(id_horario)
);
INSERT INTO funcionarios (nome, cpf, matricula, pis_pasep, id_horario) 
VALUES ('ELVIS CAVALCANTE', '11111111111', '12345', '999999999999', 1);

INSERT INTO funcionarios (nome, cpf, matricula, pis_pasep, id_horario) 
VALUES ('MARIA CHARLENE DA SILVA BRANDAO', '22222222222', '54321', '1010101010', 1);

CREATE TABLE login(
	id_login int auto_increment not null,
    id_funcionario int,
    login varchar(11) not null,
    senha varchar(255) not null,
    PRIMARY KEY (id_login),
    CONSTRAINT fk_id_funcionario FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
);

INSERT INTO login (id_funcionario, login, senha) VALUES (1, '11111111111','123456');
INSERT INTO login (id_funcionario, login, senha) VALUES (2, '22222222222','123456');

CREATE TABLE dias_uteis_ano(
	id_data varchar(10) not null unique,
    data date not null,
    cod_dia_semana int not null,
    dia_semana varchar(40) not null,
    feriado int,
    tipo_feriado varchar(40),
    PRIMARY KEY (id_data)
);

CREATE TABLE registros_pontos(
	id_registro_pontos bigint auto_increment not null,
    id_funcionario int not null,
    data_registro date not null,
    registro_turno_manha_inicial time,
    registro_turno_manha_final time,
    registro_turno_tarde_inicial time,
    registro_turno_tarde_final time,
    PRIMARY KEY (id_registro_pontos),
    CONSTRAINT fk_id_funcionario_registro FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
);

SELECT * FROM horarios_trabalho;

SELECT * FROM registros_pontos;

INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial,
registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final)
VALUES (1, '2022-06-13', '07:51:20', '12:25:39', '13:30:28', '17:25:10');

INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial,
registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final)
VALUES (1, '2022-06-23', '07:53:28', '12:14:02', '13:15:47', '17:18:08');

UPDATE registros_pontos SET registro_turno_manha_inicial = '07:48:15', registro_turno_manha_final='12:03:15',
registro_turno_tarde_inicial='13:07:40', registro_turno_tarde_final = '17:02:13' WHERE id_registro_pontos = 21;

UPDATE registros_pontos SET registro_turno_tarde_final = '17:03:26' WHERE id_registro_pontos = 22;
UPDATE registros_pontos SET id_funcionario = 1 WHERE id_registro_pontos = 18;

DELETE FROM registros_pontos WHERE id_registro_pontos=9;

select * from registros_pontos WHERE registro_turno_tarde_inicial is null;

select * from dias_uteis_ano where data='2022-06-17';
select * from dias_uteis_ano where month(data) = 6 and feriado = 0;
update dias_uteis_ano set feriado=2, tipo_feriado = 'PONTO FACULTATIVO' where data='2022-06-17';

UPDATE dias_uteis_ano SET dia_semana="Terça-Feira" where cod_dia_semana=3;

-- Desativar o SQL SAFE UPDATE
SET SQL_SAFE_UPDATES = 0;
-- Ativar o SQL SAFE UPDATE
SET SQL_SAFE_UPDATES = 1;


CREATE VIEW qtde_horas_mes AS
	SELECT month(data) as mes, year(data) as ano, count(*) as dias_uteis, 
    count(*) * 480 as minutos_a_trabalhar, round((count(*) * 480)/60,0) as qtde_horas_a_trabalhar 
    FROM dias_uteis_ano 
    WHERE year(data)=2022 and feriado = 0
    GROUP BY month(data);
    
SELECT * FROM qtde_horas_mes;


# Criando visão
CREATE VIEW relatorio_registros AS
	SELECT cf.id_data as data_mensal, month(cf.id_data) as mes, year(cf.id_data) as ano, 
    cf.id_funcionario, f.nome, f.cpf, f.matricula, rp.data_registro,
	rp.registro_turno_manha_inicial, rp.registro_turno_manha_final, rp.registro_turno_tarde_inicial, 
	rp.registro_turno_tarde_final,
	if(rp.registro_turno_manha_final is null or rp.registro_turno_manha_inicial is null,
		'00:00:00', timediff(rp.registro_turno_manha_final, rp.registro_turno_manha_inicial)) as horas_trabalhadas_manha, 
		if(rp.registro_turno_tarde_final is null or rp.registro_turno_tarde_inicial is null, '00:00:00',
		timediff(rp.registro_turno_tarde_final, rp.registro_turno_tarde_inicial)) as horas_trabalhadas_tarde, 
		if(rp.registro_turno_manha_inicial is null or rp.registro_turno_manha_final is null or 
		rp.registro_turno_tarde_inicial is null or rp.registro_turno_tarde_final is null, '00:00:00',
		sec_to_time(time_to_sec(timediff(rp.registro_turno_manha_final, rp.registro_turno_manha_inicial))
		+ time_to_sec(timediff(rp.registro_turno_tarde_final, rp.registro_turno_tarde_inicial)))) as total_horas_trabalhadas,
		if(rp.registro_turno_manha_inicial is null or rp.registro_turno_manha_final is null or 
		rp.registro_turno_tarde_inicial is null or rp.registro_turno_tarde_final is null, 0.00,
		round((time_to_sec(timediff(rp.registro_turno_manha_final, rp.registro_turno_manha_inicial))
		+ time_to_sec(timediff(rp.registro_turno_tarde_final, rp.registro_turno_tarde_inicial)))/3600,2)) as total_horas_trabalhadas_decimal
	FROM calendario_trabalho_funcionario cf
	LEFT JOIN registros_pontos rp ON date_format(rp.data_registro, '%Y-%m-%d') = cf.id_data and rp.id_funcionario = cf.id_funcionario 
	INNER JOIN funcionarios f ON f.id_funcionario = cf.id_funcionario;
   
SELECT * FROM relatorio_registros where mes=6 order by id_funcionario, data_mensal;

SELECT * FROM qtde_horas_mes where mes;

SELECT d.data, r.id_funcionario FROM dias_uteis_ano d
LEFT JOIN relatorio_registros r ON r.data = d.data or d.data is null
WHERE month(d.data) = 6 and (r.id_funcionario = 1 OR r.id_funcionario is null);

SELECT * FROM relatorio_registros where mes = 6 and id_funcionario = 1 ORDER BY data;

CREATE TABLE calendario_trabalho_funcionario (
	id_calendario bigint primary key auto_increment,
    id_data varchar(10) not null,
    id_funcionario int not null,
    CONSTRAINT fk_id_dias_uteis_calendario FOREIGN KEY (id_data) REFERENCES dias_uteis_ano (id_data),
    CONSTRAINT fk_id_funcionario_calendario FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
);

INSERT INTO calendario_trabalho_funcionario (id_data, id_funcionario)
(SELECT d.id_data, f.id_funcionario FROM dias_uteis_ano d
LEFT JOIN funcionarios f ON f.id_funcionario = f.id_funcionario 
WHERE feriado = 0
ORDER BY id_funcionario, d.data);

SELECT * FROM calendario_trabalho_funcionario;

SELECT * FROM calendario_trabalho_funcionario WHERE id_data='2022-06-17';

DELETE FROM calendario_trabalho_funcionario WHERE id_data='2022-06-17';

SELECT sum(total_horas_trabalhadas_decimal) FROM relatorio_registros;

SELECT * FROM qtde_horas_mes;

CREATE DATABASE eventos;

USE eventos;

#-------------------------------------------------------------------------------


CREATE TABLE evento (

	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	latitud FLOAT(20) NOT NULL,
	longitud FLOAT(20) NOT NULL,
	fecha TIMESTAMP NOT NULL,
	fenomeno VARCHAR(40) NOT NULL,

	CONSTRAINT pk_evento
	PRIMARY KEY (id)

) ENGINE = InnoDB;


CREATE TABLE afectacion (

	nombre VARCHAR(40) NOT NULL,

	CONSTRAINT pk_afectacion
	PRIMARY KEY (nombre)

) ENGINE = InnoDB;


CREATE TABLE imagen (

	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(40) NOT NULL,
	path VARCHAR(100) NOT NULL,

	CONSTRAINT pk_imagen
	PRIMARY KEY (id)

) ENGINE = InnoDB;

CREATE TABLE evento_imagen (

	id_evento INT UNSIGNED NOT NULL,
	id_imagen INT UNSIGNED NOT NULL,

	CONSTRAINT pk_evento_imagen
 	PRIMARY KEY (id_evento, id_imagen),

	CONSTRAINT FK_evento_imagen_evento
	FOREIGN KEY (id_evento) REFERENCES evento (id)
	ON DELETE RESTRICT ON UPDATE CASCADE,

	CONSTRAINT FK_evento_imagen_imagen
	FOREIGN KEY (id_imagen) REFERENCES imagen (id)
	ON DELETE RESTRICT ON UPDATE CASCADE

) ENGINE = InnoDB;


CREATE TABLE evento_afectacion (

	id_evento INT UNSIGNED NOT NULL,
	nombre_afectacion VARCHAR(40) NOT NULL,

	CONSTRAINT pk_evento_afectacion
 	PRIMARY KEY (id_evento, nombre_afectacion),

	CONSTRAINT FK_evento_afectacion_evento
	FOREIGN KEY (id_evento) REFERENCES evento (id)
	ON DELETE RESTRICT ON UPDATE CASCADE,

	CONSTRAINT FK_evento_afectacion_afectacion
	FOREIGN KEY (nombre_afectacion) REFERENCES afectacion (nombre)
	ON DELETE RESTRICT ON UPDATE CASCADE

) ENGINE = InnoDB;


#-----------------------------------------------------------------------------------
#Datos

INSERT INTO afectacion VALUES ("Alambrado");
INSERT INTO afectacion VALUES ("Puente");
INSERT INTO afectacion VALUES ("Edificacion");
INSERT INTO afectacion VALUES ("Alcantarilla");
INSERT INTO afectacion VALUES ("Vegetacion");
INSERT INTO afectacion VALUES ("Señalizacion");
INSERT INTO afectacion VALUES ("Animal");
INSERT INTO afectacion VALUES ("Persona");



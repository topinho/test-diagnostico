CREATE TABLE `diagnostico`.`persona` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `identificacion` VARCHAR(10) NULL,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `identificacion_UNIQUE` (`identificacion` ASC) VISIBLE);

  CREATE TABLE `diagnostico`.`vehiculo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `marca` VARCHAR(45) NULL,
  `modelo` VARCHAR(45) NULL,
  `patente` VARCHAR(45) NULL,
  `anio` INT NULL,
  `persona_id` INT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `persona_id`
    FOREIGN KEY (`id`)
    REFERENCES `diagnostico`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
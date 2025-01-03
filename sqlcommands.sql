CREATE TABLE training (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	startTime TIMESTAMP,
	endTime TIMESTAMP
);

CREATE TABLE excercises (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	trainingId INT(6) UNSIGNED,
	name VARCHAR(20),
	startTime TIMESTAMP,
	endTime TIMESTAMP,
	pauseLength INT(4),
	upLength INT(3),
	downLength INT(3),
	FOREIGN KEY(trainingId) REFERENCES training(id)
	);
	
CREATE TABLE sets (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	excerciseId INT(6) UNSIGNED,
	doneReps INT(4),
	plannedReps INT(4),
	FOREIGN KEY (excerciseId) REFERENCES excercises(id)
);

ALTER TABLE excercises
	ADD trainingId INT(6) UNSIGNED 
		AFTER id,
	ADD FOREIGN KEY(trainingId) REFERENCES training(id)
	



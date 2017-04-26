<?php
$DATABASE_PATH = 'ts3stats.db';

$db = NULL;
setup();

function setup(){
	global $DATABASE_PATH, $db;
	try {
		$db = new PDO('sqlite:' . $DATABASE_PATH);
		$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
		$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); //ERRMODE_SILENT ; ERRMODE_EXCEPTION
	} catch (PDOException $e) {
		die();
	}
}

function executeQuerry($query, $params = array(), $single = false){
	global $db;
    $stmt = $db->prepare($query);
	$stmt->execute($params);
	if($single){
		return $stmt;
	}
	return $stmt->fetchAll();
}

function ouputTable($query, $params = array(), $links = array(), $header = true){
	echo "<table>";
	$result = executeQuerry($query, $params);
	foreach ($result as $row) {
		if($header){
			echo "<tr>";
			foreach ($row as $col => $value){
				echo "<th>" . htmlspecialchars($col, ENT_QUOTES, 'UTF-8') . '</th>';
			}
			echo "</tr>";
			$header = false;
		}

		echo "<tr>";
		$item = 1;

		foreach ($row as $col => $value){
			echo "<td>";
			if (isset($links[$item])) { //
				echo str_replace('%', $value, $links[$item]);
			}
			else{
				echo $value;
			}
			echo '</td>';
			$item++;
		}
		echo "</tr>";
	}		
	echo "</table>";
}
?>
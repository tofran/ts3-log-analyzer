<?php
$DATABASE_PATH = 'ts3stats.db';

$db = NULL;
try {
	$db = new PDO('sqlite:' . $DATABASE_PATH);
	$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
	die($e->getMessage());
}

function executeQuerry($query, $params = array()){
	global $db;
    $stmt = $db->prepare($query);
	$stmt->execute($params);
	return $stmt->fetchAll();
}

function ouputTable($query, $header = true){
	echo "<table>";
	$result = executeQuerry($query);
	foreach ($result as $row) {
		if($header){
			echo "<tr>";
			foreach ($row as $col => $value){
				echo "<th>" . $col . '</th>';
			}
			echo "</tr>";
			$header = false;
		}

		echo "<tr>";
		foreach ($row as $col => $value){
			echo "<td>" . $value . '</td>';
		}
		echo "</tr>";
	}		
	echo "</table>";
}
?>
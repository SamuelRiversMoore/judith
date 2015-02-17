// echo"<br>on teste si il y a une limite de coté dans ".$coup[0];		
$result = strpos($coup[0], "|");
	if ($result!==false){
	//echo"=> oui.";
	//echo"<br>on teste si il y a un jocker en plus de la limite de coté";	
		$result = strpos($coup[0], "(*)");
		if ($result>0){
		//echo"=> oui.";
			$coup2=explode("|", $coup[0]);
			if($coup2[0] == "")
			{
			//echo"<br>La limite est à gauche. On coupe avant le jocker et teste normalement.";
			$coup2=explode("(*)", $coup2[1]);
			//echo"<br>Teste si ".$coup2[0]." correspond au début de ".$_POST['usersay'];
			$result=strpos($_POST['usersay'], $coup2[0]);
			//echo$result;
				if($result===false)
				{
				//echo"<br>Rien ne correspond....";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;				
				}
				if($result==0 && $result !== false )
				{
				//echo"<br>C'est bien juste le début.";
				}
				if($result>0)
				{
				//echo"<br>C'est pas le début.";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;	
				}
			}
			$coup2=explode("|", $coup[0]);
			if($coup2[count($coup2)-1] == "")
			{
			//echo"<br>La limite est à droite. On coupe après le jocker et teste normalement.";
			$coup2=explode("(*)", $coup2[count($coup2)-2]);
			//echo"<br>Teste si la longueur de ".$_POST['usersay']." correspond à l'endroit où on a trouvé ".$coup2[count($coup2)-1]."moins la taille de ".$coup2[count($coup2)-2];			
			$result=strpos($_POST['usersay'], $coup2[count($coup2)-1]);
			//echo$result;
				if($result===false)
				{
				//echo"<br>Rien ne correspond....";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;				
				}
				//echo strlen($_POST['usersay']);
				//echo$result+strlen($coup2[count($coup2)-1]);
				//si usersay est égal à la position où on a détecté le début de la ligne plus la chaine à chercher
				if(strlen($_POST['usersay'])==$result+strlen($coup2[count($coup2)-1])){
				//echo"<br>C'est bien la fin.";
				}
				else
				{
				//echo"=>Nope, fin de l'analyse.";
				$continueanalyse=false;	
				}
			}
			
		}
		else{
		//echo"=>Non.";
		$coup2=explode("|", $coup[0]);
			if($coup2[0] == "")
			{
			//echo"<br>La limite est à gauche.";
			//echo"<br>Teste si ".$coup2[1]." correspond au début de ".$_POST['usersay'];
			$result=strpos($_POST['usersay'], $coup2[1]);
			//echo$result;
				if($result===false)
				{
				//echo"<br>Rien ne correspond....";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;				
				}
				if($result==0 && $result !== false )
				{
				//echo"<br>C'est bien juste le début.";
				}
				if($result>0)
				{
				//echo"<br>C'est pas le début.";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;	
				}				
			}
			$coup2=explode("|", $coup[0]);			
			if($coup2[count($coup2)-1] == "")
			{
			//echo"<br>La limite est à droite.";
			//echo"<br>Teste si la longueur de ".$_POST['usersay']." correspond à l'endroit où on a trouvé ".$coup2[count($coup2)-2]." moins la taille de ".$coup2[count($coup2)-2];
			$result=strpos($_POST['usersay'], $coup2[count($coup2)-2]);
			//echo$result;
				if($result===false)
				{
				//echo"<br>Rien ne correspond....";
				//echo"=>fin de l'analyse.";
				$continueanalyse=false;				
				}
				//si usersay est égal à la position où on a détecté le début de la ligne plus la chaine à chercher
				//echo strlen($_POST['usersay']);
				//echo$result+strlen($coup2[count($coup2)-2]);
				if(strlen($_POST['usersay'])==$result+strlen($coup2[count($coup2)-2])){
				//echo"<br>C'est bien la fin.";
				}
				else
				{
				//echo"=>Nope, fin de l'analyse.";
				$continueanalyse=false;	
				}
			}
		}
		
		$coup[0]=str_replace("|", "", $coup[0]);
	}
}	
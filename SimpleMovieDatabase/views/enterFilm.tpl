<html><head><title>Add a Movie</title></head>
	<body>
		<p><strong>Add a New Film to the Database</strong></p>

		<form action = "/enterFilm" method = "post">

			<p><input name = "title" type = "text" size = "40"> Movie Title </p>
			<p><input name = "description" type = "text" size = "80"> Movie Description </p>
			<p> Release_year will be your default value. </p>
			<p><input name = "length" type = "text" value = "0" size = "5"> Movie Length </p>
			
			<p><select name = "category"> Category
				<option value = "1">Action</option>
				<option value = "2">Animation</option>
				<option value = "3">Children</option>
				<option value = "4">Classics</option>
				<option value = "5">Comedy</option>
				<option value = "6">Documentary</option>
				<option value = "7">Drama</option>
				<option value = "8">Family</option>
				<option value = "9">Foreign</option>
				<option value = "10">Horror</option>
				<option value = "11">Musical</option>
				<option value = "12">Sci-Fi</option>
				
				</select>
			</p>
			<p><input type = "Submit"></p>
		</form>
	</body>
</html>
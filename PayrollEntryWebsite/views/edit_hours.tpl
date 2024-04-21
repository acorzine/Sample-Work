% rebase("layout.tpl", title = "Edit Hours")
<p>
<h3>Enter emp_id and Hours Worked</h3>
	<form action="/editHours" method="POST">
        <label for="eid">Employee ID:</label>
        <input type="text" id="eid" name="eid" required><br><br>
        <label for="hrs">Hours Worked:</label>
        <input type="text" id="hrs" name="hrs" required><br><br>
        <input type="submit" value="Submit Query">
	</form>
</p>
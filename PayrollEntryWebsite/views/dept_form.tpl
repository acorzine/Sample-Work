% rebase('layout.tpl', title = 'Departments')
 
		<h4>Please Choose Your Department<h4>
		<br>
		<p>
		<form method="post" action="/getDepartment">
		
		   Show Departments: <select name='dept'>
		       <option value="advertising">Advertising</option>
			   <option value="environment">Environment</option>
			   <option value="maintenance">Maintenance</option>
			   <option value="shipping">Shipping</option>
		    </select> &nbsp; 
			
			<input type='submit'>
		<form>
		</p>
    <br>

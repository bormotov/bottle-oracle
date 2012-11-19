<!DOCTYPE html>

<html>
  <head>
    <title>Bottle Oracle Plugin Example</title>
  </head>
  <body>
    <h2>select ... from v$sessions where username = {{user}}</h2>
    <table>
      <tr>
    %for field in fields:
        <th>{{field}}</th>
    %end
      </tr>
    %for session in sessions:
      <tr>
      %for fld in session:
        <td>{{fld}}</td>
      %end
      </tr>
    %end
    </table>
    <hr>
  </body>
</html>

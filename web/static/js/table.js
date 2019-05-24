/*
var headertext = [],
headers = document.querySelectorAll("#miyazaki th"),
tablerows = document.querySelectorAll("#miyazaki th"),
tablebody = document.querySelector("#miyazaki tbody");

for(var i = 0; i < headers.length; i++) {
  var current = headers[i];
  headertext.push(current.textContent.replace(/\r?\n|\r/,""));
} 
for (var i = 0, row; row = tablebody.rows[i]; i++) {
  for (var j = 0, col; col = row.cells[j]; j++) {
    col.setAttribute("data-th", headertext[j]);
  } 
}
*/
/*
<tr>
<td>Princess Mononoke
<td>Nebula Award (Best Script)
<td><img src="static/img/true.png" height="40" width="40">
<td><img src="static/img/false.png" height="40" width="40">
<tr>

*/

function dynamic_db(list_var)
{
    var label_list = new Array(
      "<td><img src='static/img/false.png' height='40' width='40'>",
      "<td><img src='static/img/true.png' height='40' width='40'>"
      );
    var insertDiv = document.getElementById("results_db");
    var insert_string = "";
    for(var i=1;i<list_var['length']+1;i++)
    {
      var temp_str = "";
      temp_str = temp_str + "<tr><td>"+list_var[""+i].id+"<td>"+list_var[""+i].text;
      for (var j=0;j<5;j++)
      {
          if(list_var[""+i].label[j] == 1)
          {
            temp_str = temp_str+label_list[1];
          }
          else
          {
            temp_str = temp_str+label_list[0];
          }
            
      }
      temp_str = temp_str + "<td>" +list_var[""+i].relabel+"<td>"+list_var[""+i].flag;

      
      insert_string = insert_string+temp_str;
    }
    /*alert(insert_string)*/
    insertDiv.innerHTML = insert_string;

};
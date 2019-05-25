function dynamic_checkbox(list_var)
{
    var true_list = new Array(
        "<li><label><input type='checkbox' checked disabled/><span class='lbl padding-8'><img src='static/img/happy.png' height='40' width='40'></span></label></li>", 
        "<li><label><input type='checkbox' checked disabled/><span class='lbl padding-8'><img src='static/img/sad.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' checked disabled/><span class='lbl padding-8'><img src='static/img/angry.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' checked disabled/><span class='lbl padding-8'><img src='static/img/fear.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' checked disabled/><span class='lbl padding-8'><img src='static/img/surprise.png' height='40' width='40'></span></label></li>");
    var false_list = new Array(
        "<li><label><input type='checkbox' disabled/><span class='lbl padding-8'><img src='static/img/happy.png' height='40' width='40'></span></label></li>", 
        "<li><label><input type='checkbox' disabled/><span class='lbl padding-8'><img src='static/img/sad.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' disabled/><span class='lbl padding-8'><img src='static/img/angry.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' disabled/><span class='lbl padding-8'><img src='static/img/fear.png' height='40' width='40'></span></label></li>",
        "<li><label><input type='checkbox' disabled/><span class='lbl padding-8'><img src='static/img/surprise.png' height='40' width='40'></span></label></li>");
    
    var insertDiv = document.getElementById("text"); 
    insertDiv.innerText = list_var.text;
    var insertDiv = document.getElementById("ul_form");   
    var insert_string = ""; 
    for (var j=0;j<5;j++)
    {
        if(list_var.label[j] == 1)
        {
            insert_string = insert_string+'\n'+true_list[j];
        }
        else
        {
            insert_string = insert_string+'\n'+false_list[j];
        }
    }
    insertDiv.innerHTML = insert_string;

};




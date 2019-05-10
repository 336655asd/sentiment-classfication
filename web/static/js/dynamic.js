function dynamic_list(list_var)
{
    var label_list = new Array(
        "<div style='background:#EA0000;color:#fff;cursor:default; display: inline-block; width:auto;height:auto;'><span>喜悦</span></div>", 
        "<div style='background:#2828FF;color:#fff;cursor:default; display: inline-block; width:auto;height:auto;'><span>悲伤</span></div>",
        "<div style='background:#F75000;color:#fff;cursor:default; display: inline-block; width:auto;height:auto;'><span>生气</span></div>",
        "<div style='background:#8600FF;color:#fff;cursor:default; display: inline-block; width:auto;height:auto;'><span>恐惧</span></div>",
        "<div style='background:#00DB00;color:#fff;cursor:default; display: inline-block; width:auto;height:auto;'><span>惊讶</span></div>");
        
    for(var i=0;i<4;i++)
    {
        var element_id = "list"+i;
        var insertDiv = document.getElementById(element_id);
        var insert_string = "";
        for (var j=0;j<5;j++)
        {
            if(list_var[element_id].label[j] == 1)
            {
                insert_string = insert_string+'\n'+label_list[j];
            }
            
        }
        insertDiv.innerHTML = insert_string;
    }

};


function SwapTxt()
 {
     var txt = document.getElementById("search-input").value;
     document.getElementById("get_text").innerHTML=txt;
 };


var json_data;
var page_anims;
var next_anim_idx;

function load_page(idx){
    page_g_id = json_data["pages"][idx]["page_id"];
    // Hide all SVG top level groups apart from this page and its background
    $('svg > g[id^=page]').css('display', 'none');
    $('#' + page_g_id).css('display','block');
    $('#' + page_g_id + '_bg').css('display','block');

    hidden_ids = json_data["pages"][idx]["init_hidden"];
    // Make all elements of the page visible
    for(var i = 0; i < $("#"+ page_g_id).children().length; i++){
        elt = $($("#" + page_g_id).children()[i]);
        elt.attr("visibility", "visible");
    }
    // Hide all those elements of the page that are initially hidden
    for(var j=0; j < hidden_ids.length; j++){
        elt = $("#" + hidden_ids[j]);
        elt.attr("visibility", "hidden");
    }
    page_anims = json_data["pages"][idx]["animations"];
    next_anim_idx = 0;
}

function next_animation(){
    if (next_anim_idx < page_anims.length){
        anim_id = page_anims[next_anim_idx]["id"];
        document.getElementById(anim_id).beginElement();
        next_anim_idx++;
    }
}

$(document).ready(function(){
    $.getJSON("http://localhost:8000/test.json", function(data){
        json_data = data;
        load_page(0);
    });
});

$(document).on('keydown', function(e){
    key_code = e.which ? e.which : e.keyCode;
    let tag = e.target.tagName.toLowerCase();
    switch(key_code){
        case 78: // N
            next_animation();
            break;
    }
});
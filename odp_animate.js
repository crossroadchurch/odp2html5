var json_data;
var page_anims;
var cur_page_idx;
var next_anim_idx;

function load_page(idx){
    if (0 <= idx && idx < json_data["pages"].length){
        cur_page_idx = idx;
        page_g_id = json_data["pages"][idx]["page_id"];
        // Hide all SVG top level groups apart from this page and its background
        $('svg > g[id^=page]').css('display', 'none');
        $('#' + page_g_id).css('display','block');
        $('#' + page_g_id + '_bg').css('display','block');
        hidden_ids = json_data["pages"][idx]["init_hidden"];
        visible_ids = json_data["pages"][idx]["init_visible"];
        // Show animated elements that are initially visible
        for(var i=0; i < visible_ids.length; i++){
            set_visibility(visible_ids[i], "visible");
        }
        // Hide animated elements that are initially hidden
        for(var j=0; j < hidden_ids.length; j++){
            set_visibility(hidden_ids[j], "hidden");
        }
        page_anims = json_data["pages"][idx]["animations"];
        next_anim_idx = 0;
    }
}

function next_animation(){
    if (next_anim_idx < page_anims.length){
        anim_id = page_anims[next_anim_idx]["id"];
        document.getElementById(anim_id).beginElement();
        next_anim_idx++;
    } else if (cur_page_idx < (json_data["pages"].length - 1)){
        load_page(cur_page_idx + 1);
    }
}

function set_visibility(elt_id, v_state){
    var new_anim_id = elt_id + "_" + v_state;
    elt = document.getElementById(elt_id);
    if (elt.querySelector('#' + new_anim_id) == null) {
        var anim = document.createElementNS("http://www.w3.org/2000/svg", "set");
        anim.setAttribute('attributeName', 'visibility');
        anim.setAttribute('to', v_state);
        anim.setAttribute('begin', 'indefinite');
        anim.setAttribute('id', new_anim_id);
        elt.appendChild(anim);
    }
    document.getElementById(new_anim_id).beginElement();
}

function prev_animation(){
    if (next_anim_idx > 0){
        for (var i=page_anims[next_anim_idx-1]["anim_order"].length-1; i>=0; i--){
            rev_id = page_anims[next_anim_idx-1]["anim_order"][i] + "_rev";
            document.getElementById(rev_id).beginElement();
        }
        next_anim_idx--;
    } else if (cur_page_idx > 0){
        load_page(cur_page_idx - 1);
        next_anim_idx = page_anims.length;
        setTimeout(prev_slide_load_end, 1);
    }
}

function prev_slide_load_end(){
    goto_animation(0);
    goto_animation(page_anims.length);
}

function goto_animation(new_next_idx){
    if (new_next_idx < 0 || new_next_idx > page_anims.length || new_next_idx == next_anim_idx){
        return; // No goto needed or invalid index
    }
    if (new_next_idx > next_anim_idx) {
        for (var i=next_anim_idx; i < new_next_idx; i++){
            for (var j=0; j<page_anims[i]["anim_order"].length; j++){
                fwd_id = page_anims[i]["anim_order"][j] + "_fwd";
                document.getElementById(fwd_id).beginElement();
            }
        }
    } else {
        for (var i=next_anim_idx-1; i >= new_next_idx; i--){
            for (var j=page_anims[i]["anim_order"].length-1; j>=0; j--){
                rev_id = page_anims[i]["anim_order"][j] + "_rev";
                document.getElementById(rev_id).beginElement();
            }
        }
    }
    next_anim_idx = new_next_idx;
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
        case 80: // P
            prev_animation();
            break;
    }
});
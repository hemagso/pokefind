// todo: Add guides over the image when selecting the bounding box
jQuery.noConflict();
let pokemon_selected;
let frame_data;
let pokemon_list;

const get_annotations_json = function() {
    let sel = anno.getAnnotations();
    return sel.map(function(elem) {
        let pkm_id = !elem.pkm_id ? null : elem.pkm_id;
        let bbox = {
            "x": elem.shapes[0].geometry.x,
            "y": elem.shapes[0].geometry.y,
            "height": elem.shapes[0].geometry.height,
            "width": elem.shapes[0].geometry.width
        };
        return {
            "id": pkm_id,
            "bbox": bbox,
            "comment": elem.text
        };
    });
};

const get_new_frame = function() {
    jQuery.ajax({
        "type": "GET",
        "url": "/annotations/get_frame",
        "success": function(data){
            frame_data = JSON.parse(data);
            anno.removeAll();
            jQuery("#main-img").attr("src","/annotations/frame_image/" + frame_data["id"]);
            jQuery("#season-label").text(frame_data["season"]);
            jQuery("#episode-label").text(frame_data["episode"]);
            jQuery("#frame-label").text(frame_data["frame"]);
        }
    });
};

const get_pokemon_list = function() {
    jQuery.ajax({
        "type": "GET",
        "url": "/annotations/get_pokemon_list",
        "success": function(data){
            pokemon_list = JSON.parse(data);
        }
    });
};

function callPlayer(frame_id, func, args) {
    //Source: https://stackoverflow.com/questions/7443578/youtube-iframe-api-how-do-i-control-a-iframe-player-thats-already-in-the-html#7513356
    if (window.jQuery && frame_id instanceof jQuery) frame_id = frame_id.get(0).id;
    var iframe = document.getElementById(frame_id);
    if (iframe && iframe.tagName.toUpperCase() != 'IFRAME') {
        iframe = iframe.getElementsByTagName('iframe')[0];
    }
    if (iframe) {
        // Frame exists,
        iframe.contentWindow.postMessage(JSON.stringify({
            "event": "command",
            "func": func,
            "args": args || [],
            "id": frame_id
        }), "*");
    }
}

jQuery(document).ready(function() {
    get_pokemon_list();
    get_new_frame();
    jQuery("#tutorial-button").popup({
        "popup": jQuery("#tutorial"),
        "on": "click",
        "onHide" : function() {
            callPlayer("tutorial-video", "pauseVideo")
        }
    });
    jQuery("#submit-button").on("click", function() {
        let data = get_annotations_json();
        jQuery.ajax({
            type: "POST",
            url: "/annotations/make",
            data: {
                frame_id: frame_data["id"],
                annotations: JSON.stringify(data),
                csrfmiddlewaretoken: jQuery('[name="csrfmiddlewaretoken"]').val()
            },
            success: function() {
                get_new_frame();
            }
        });
    });
    jQuery("#about-button").on("click", function(){
        jQuery("#about").modal("show");
    });
    jQuery("#faq-button").on("click", function(){
        jQuery("#faq").modal("show");
    });
    jQuery("#skip-button").on("click", function() {
        get_new_frame();
    });
    jQuery("#faq-list").accordion();
});
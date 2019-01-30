
const get_pkm_name = function(id) {
    if (!id) return "No classification";
    else if (id in pokemon_list) return pokemon_list[id];
    else return "Unknown ID";
};

//Creating the plugin that let us use a dropdown to annotate the Pokemons on Annotorious
annotorious.plugin.Pokemon = function(opt_config_options) { };
annotorious.plugin.Pokemon.prototype.onInitAnnotator = function(annotator) {
    //Add the DOM elements for the Pokemon Selector
    annotator.editor.addField(function(annotation) {
        let root = jQuery("<div/>", {
            "id": "pkm_selector",
            "class": "ui fluid search selection dropdown control-element"
        });
        root.append(jQuery("<div/>", {
            "class": "default text",
            "text": "Select Pokemon"
        }));
        root.append(
            jQuery("<i/>", {
                "class" : "dropdown icon"
            }));
        let menu = jQuery("<div/>", {
            "class": "menu"
        });
        for (let pkm_id in pokemon_list) {
            let item = jQuery("<div/>",{
                "class": "item",
                "data-value": pkm_id,
                "text": pokemon_list[pkm_id]
            });

            item.prepend(jQuery("<i/>",{
                "class": "pkm id" + pkm_id
            }));

            menu.append(item);
        }
        root.append(menu);
        return root[0];
    });
    //Add the handler that initialize the semantic dropdown added in the previous step
    annotator.addHandler("onAnnotationCreated", function(annotation) {
       annotation.pkm_id = pokemon_selected;
       pokemon_selected = undefined;
    });

    annotator.addHandler("onEditorClose", function() {
        jQuery("#submit-button").removeClass("disabled");
        jQuery("#skip-button").removeClass("disabled");
    });
    annotator.addHandler("onEditorShown", function(annotation) {

        jQuery("#submit-button").addClass("disabled");
        jQuery("#skip-button").addClass("disabled");

        let elem = jQuery("#pkm_selector");
        elem.dropdown({
            clearable: true,
            fullTextSearch: true,
            onChange: function(val, text, choice) {
                if (annotation) {
                    annotation.pkm_id = val;
                }
                else {
                    pokemon_selected = val;
                }
            }
        });

        if (annotation.pkm_id)
            elem.dropdown("set selected", annotation.pkm_id)
    });
    //Add a field to the popup showing which pokemon was selected for the annotation
    annotator.popup.addField(function(annotation) {
        let elem = jQuery("<div/>", {
            "class": "ui image label",
            "text": get_pkm_name(annotation.pkm_id)
        });
        elem.prepend(
            jQuery("<i/>", {
                "class": "pkm id" + annotation.pkm_id
            })
        );
        return elem[0];
    });
};
anno.addPlugin('Pokemon', {});
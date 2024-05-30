#target Illustrator

/*
 * script.name = exportMultipleSetsLayersAsImages.jsx;
 * script.description = Export layers of each project in a chosen folder as PNG images;
 * script.requirements = Nothing.
 * script.elegant = false;
 */

/**
 * Export layers of each project in a chosen folder as PNG images.
 * Derived from the exportLayersAsImages script to process Ai projects in a folder.
 */

app.preferences.setBooleanPreference("ShowExternalJSXWarning", false);
var RESULT_FOLDER_NAME = 'SETS_EXPORT';
var MAX_RENAMED_LAYERS = 30;

var rename_layers = true;
var hide_fx_layers = false;

if (!String.prototype.includes)
{
    String.prototype.includes = function() {
        'use strict';
        return String.prototype.indexOf.apply(this, arguments) !== -1;
     }
}


//var ai_files = "//andromede.lesfees.lan/anpo/lib/sets/sq021/sq021_bg04000/design/design_ai/v001/sq021_bg04000_design.ai;//andromede.lesfees.lan/anpo/lib/sets/sq021/sq021_bg04020/design/design_ai/v001/sq021_bg04020_design.ai;//andromede.lesfees.lan/anpo/lib/sets/sq021/sq021_bg04030/design/design_ai/v001/sq021_bg04030_design.ai";
//var root_folder = "//andromede.lesfees.lan/anpo";

var ai_files = $.getenv("LIBREFLOW_AI2LAYERS_AILIST");
var root_folder = $.getenv("LIBREFLOW_ROOT_FOLDER");

main();

//var ai_file = new File(ai_path);
//var document = app.open(ai_file, DocumentColorSpace.RGB);




function main() {
    // Disable alert boxes
    app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
    

    var ai_file_list = ai_files.split(";");

    
    for (i = 0; i < ai_file_list.length; i++){
            
            var full_path = ai_file_list[i];
            var base_path = full_path.replace(root_folder, "");
            
            
            var _base_path_split = base_path.split("/");
            
            var asset_family = _base_path_split[3];
            var asset_name = _base_path_split[4].replace("_", "-");
            var asset_revision = _base_path_split[7];
            
            var asset_layers_path = root_folder + "/lib/sets/" + asset_family + "/" + asset_name + "/design/layers/" + asset_revision + "/";
            print(asset_layers_path);
            print();
            
            export_layers(file=full_path, name=asset_name, output_path=null, layers_output_path=asset_layers_path, hide_fx_layers=hide_fx_layers, auto_rename=rename_layers);
            
        }
    // var idquit = charIDToTypeID( "quit" );
    
    // executeAction( idquit, undefined, DialogModes.NO );
    
}



/**
 * Exports an Illustrator project composition and each of its layer as PNG images.
 *
 * This function processes only the document's visible layers.
 *
 * @param file File object representing an Illustrator project
 * @param name Name of the project image result
 * @param output_path Destination path of the project image result
 * @param layers_output_path Destination path of the individual layer images
 * @param hide_fx_layers Indicates whether FX layers must be hidden
 * @param auto_rename Indicates whether invalid characters in layer names must be automatically replaced with '_'
 */
function export_layers(file, name, output_path, layers_output_path, hide_fx_layers, auto_rename) {

    // Open document in RGB color space
    var document = app.open(new File(file), DocumentColorSpace.RGB);

    // Prevent spaces in set name
    //name = document.name.split('.')[0].replace(/[\s()]/gi, '_');

    // Export set

    var options = getExportOptions(100.0, 100.0);
    var optionsJPEG = getJPEGExportOptions(100.0, 100.0);

    // Export layers

    const layer_regex = /^[\d]+_[\w]+$/gi;
    const invalid_chars = /[^\w]/gi;

    // Choose how to rename a layer's invalid name
    rename_layers(auto_rename);

    // Create layers folder
    var layers_folder = new Folder(layers_output_path) // + '/' + name);

    if (!layers_folder.exists)
        layers_folder.create()

    
    // Export preview image
    var preview_path = layers_output_path + name + '_preview.jpg';
    print(preview_path);
    var set_img = new File(preview_path);
    document.exportFile(set_img, ExportType.JPEG, optionsJPEG);

    var sets_paths_file = new File(layers_output_path + '/sets_paths.txt');

    sets_paths_file.encoding = 'UTF-8';
    sets_paths_file.open('a');
    sets_paths_file.write(set_img.fsName + ';' + document.fullName.fsName);

     if (hide_fx_layers)
        hideLayers(/fx/i);

    var visible_layers = getVisibleLayers();
    var visible_count = visible_layers.length;

   
    var layers_paths_file = new File(layers_output_path + '/layers_paths.txt');
	var existing_layers_file = new File(layers_output_path + '/existing_layers.txt');
    layers_paths_file.encoding = 'UTF-8';
    layers_paths_file.open('a');
    existing_layers_file.encoding = 'UTF-8';
    existing_layers_file.open('a');

    hideLayers(null);

    var invalid_layer_names = false;

    for (var i = 0; i < visible_count; ++i)
    {
        var layer = document.layers[visible_layers[i]];
        layer.visible = true;

        // Export layer image
        var layer_path = layers_folder.fsName + '/' + name + '_' + layer.name;

        // Rename layer if another one with the same name already exists
        var layer_img = new File(layer_path + '.png');

        if (layer_img.exists)
            existing_layers_file.writeln(name + '/' + layer.name);

        document.exportFile(layer_img, ExportType.PNG24, options);

        // Export layer data
        layers_paths_file.write(layer_img.fsName + ';');

        layer.visible = false;

        var layer_prefix = layer.name.split('_')[0];
        invalid_layer_names = invalid_layer_names || !layer_prefix.match(/^\d+$/)
    }

    var invalid_layer_names_text;

    if (invalid_layer_names)
        invalid_layer_names_text = ';invalid_layer_names'
    else
        invalid_layer_names_text = ''

    sets_paths_file.writeln(invalid_layer_names_text)
    sets_paths_file.close();
	existing_layers_file.close();

    // Restore visible layers
    showLayers(visible_layers);

    layers_paths_file.writeln('')
    layers_paths_file.close();
    document.close(SaveOptions.DONOTSAVECHANGES);

    /**
     * Returns predefined options for PNG export.
     *
     * @param hscale Result's width scaling factor
     * @param vscale Result's height scaling factor
     */
    function getExportOptions(hscale, vscale)
    {
        var options = new ExportOptionsPNG24();
        var newRGBColor = new RGBColor();

        newRGBColor.red = 0;
        newRGBColor.green = 0;
        newRGBColor.blue = 0;
        options.matteColor = newRGBColor;
        options.antiAliasing = true;
        options.transparency = true;
        options.artBoardClipping = true;
        options.horizontalScale = hscale;
        options.verticalScale = vscale;

        return options
    }

/**
     * Returns predefined options for JPEG export.
     *
     * @param hscale Result's width scaling factor
     * @param vscale Result's height scaling factor
     */
    function getJPEGExportOptions(hscale, vscale)
    {
        var options = new ExportOptionsJPEG();
        var newRGBColor = new RGBColor();

        newRGBColor.red = 0;
        newRGBColor.green = 0;
        newRGBColor.blue = 0;
        options.matteColor = newRGBColor;
        options.antiAliasing = true;
        options.transparency = false;
        options.artBoardClipping = true;
        options.horizontalScale = hscale;
        options.verticalScale = vscale;

        return options
    }

    /**
     * Hides layers whose names match a given pattern.
     *
     * @param regex: The pattern in question
     */
    function hideLayers(regex)
    {
        if (regex != null)
        {
            fn = function(layer) {
                if (layer.name.match(regex))
                    layer.visible = false;
            };
        }
        else
        {
            fn = function(layer) {
                layer.visible = false;
            };
        }
        forEach(document.layers, fn);
    }

    /**
     * Shows a subset of layers in the active document.
     *
     * @param indices: Indices of the layers in the active document's layer array
     */
    function showLayers(indices)
    {
        forEach(indices, function(index) {
            document.layers[index].visible = true;
        });
    }

    /**
     * Returns the visible layers in the active document.
     *
     * @returns: The list of visible layer indices
     */
    function getVisibleLayers()
    {
        var layers = document.layers;
        var visible_layers = [];
        var n = layers.length;

        for (var i = 0; i < n; ++i)
        {
            if (layers[i].visible)
                visible_layers.push(i);
        }

        return visible_layers;
    }

    function rename_layers(auto_rename)
    {
        if (auto_rename)
        {
            forEach(document.layers, function(layer) {
                layer.name = layer.name.replace(invalid_chars, '_');
            });
        }
        else
        {
            forEach(document.layers, function(layer) {
                while (!layer_regex.test(layer.name))
                    layer.name = prompt("Layer name '" + layer.name + "' is invalid. Please rename it following the pattern ORDER_NAME, where ORDER is a series of digits, and NAME is composed of characters from 'a-z', 'A-Z', '0-9', '_' and '-'.", layer.name);
            });
        }
    }

    /**
     * Applies a function to each element of a given collection.
     */
    function forEach(collection, fn)
    {
        var n = collection.length;

        for (var i = 0; i < n; ++i)
        {
            fn(collection[i]);
        }
    }
}



function print(output){
    $.writeln(output);
    }
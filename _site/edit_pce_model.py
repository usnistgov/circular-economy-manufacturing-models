from edit_idef_html import open_html, basic_formatting, save_html 
from edit_idef_html import format_list_pools, remove_extraneous_info, format_diagram_images
from edit_idef_html import add_decomposition_images, remove_from_TOC, update_frontmatter, update_time 
import os

## Running to modify files
if __name__ == "__main__":
    
    ## START GENERAL
    frontmatter_layout = {
            "layout": "default"
    }
    
    currentdict = os.getcwd()
    modelfoldername = "pce/pce" #folder in which model html files are located, relative to this python file
    modeldict = os.path.join(currentdict, modelfoldername)
    
    #modify model pages in specific folder name
    for filename in os.listdir(modeldict):
        if filename.endswith(".html"):
            # Edit Model page type (file starts with "dgm")
            if (filename.startswith("dgm")): 
                s = open_html(os.path.join(modeldict, filename))
                s = basic_formatting(s)
                s = format_list_pools(s)
                s = remove_extraneous_info(s)
                s = format_diagram_images(s)
                save_html(s, os.path.join(modeldict, filename), frontmatter_data=frontmatter_layout)
            # Edit Activity-in-Diagram page type (file starts with "act")
            if (filename.startswith("act")): 
                s = open_html(os.path.join(modeldict, filename))
                s = basic_formatting(s)
                s = format_list_pools(s, icom=True)
                s = remove_extraneous_info(s)
                save_html(s, os.path.join(modeldict, filename), frontmatter_data=frontmatter_layout)
            # Edit Use-of-Concept page type (file starts with "conc")
            if (filename.startswith("conc")): 
                s = open_html(os.path.join(modeldict, filename))
                s = basic_formatting(s)
                s = remove_extraneous_info(s)
                save_html(s, os.path.join(modeldict, filename), frontmatter_data=frontmatter_layout)
    
    #update TOC page
    filename= "_includes/TOC_Hier.html"
    s = open_html(os.path.join(currentdict, filename))
    s = remove_from_TOC(s, modelfoldername)
    save_html(s, os.path.join(currentdict, filename), add_fm=False)
    
    #update last updated for CPD model
    filename="index.html"
    updateid="cpd_update"
    s = open_html(os.path.join(currentdict, filename))
    s = update_time(s, updateid)
    save_html(s, os.path.join(currentdict, filename), add_fm=False)
    ## END GENERAL
    
    ## MODEL SPECIFIC
    
    #add notes that some activities are incomplete; 
    #add in manual decomposition images on the A1 level activities (need to identify the specific files to edit and the relevant images/links to connect to)
    filename = "actuseDesign_Product5512.html"
    updates = {"notetitle": "Note", "note": "This activity is fully described. Click a decomposition, activity, or input/output/control/mechanism for descriptions and examples that are relevant for designing in a circular economy."}
    update_frontmatter(os.path.join(modeldict, filename), frontmatter_updates = updates)
    imagename = "dgm30_DesignProduct.jpeg"
    linktodiagram = "dgmA1COLON_Design_Product4091.html"
    s = open_html(os.path.join(modeldict, filename))
    s = add_decomposition_images(s, imagename, linktodiagram)
    save_html(s, os.path.join(modeldict, filename))
    
    ## Commented out since we may need to update the diagrams for these activities
    filename = "actuseAcquire_Materials5573.html"
    updates = {"notetitle": "Note", "note": "This activity is NOT fully described."}
    update_frontmatter(os.path.join(modeldict, filename), frontmatter_updates = updates)
    # imagename ="dgm161_AcquireMaterials.jpeg"
    # linktodiagram = "dgmA2COLON_Acquire_Materials1830.html"
    # s = open_html(os.path.join(modeldict, filename))
    # s = add_decomposition_images(s, imagename, linktodiagram)
    # save_html(s, os.path.join(modeldict, filename))
    
    filename = "actuseProduce_Product5604.html"
    updates = {"notetitle": "Note", "note": "This activity is NOT fully described."}
    update_frontmatter(os.path.join(modeldict, filename), frontmatter_updates = updates)
    # imagename = "dgm190_ProduceProduct.jpeg"
    # linktodiagram = "dgmA3COLON_Produce_Product54.html"
    # s = open_html(os.path.join(modeldict, filename))
    # s = add_decomposition_images(s, imagename, linktodiagram)
    # save_html(s, os.path.join(modeldict, filename))
    
    filename = "actuseUse_and_Consume5677.html"
    updates = {"notetitle": "Note", "note": "This activity is NOT fully described."}
    update_frontmatter(os.path.join(modeldict, filename), frontmatter_updates = updates)
    # imagename = "dgm206_UseAndConsume.jpeg"
    # linktodiagram = "dgmA4COLON_Use_and_Consume85.html"
    # s = open_html(os.path.join(modeldict, filename))
    # s = add_decomposition_images(s, imagename, linktodiagram)
    # save_html(s, os.path.join(modeldict, filename))
    
    filename = "actuseTreat_at_End_of_Life5738.html"
    updates = {"notetitle": "Note", "note": "This activity is NOT fully described."}
    update_frontmatter(os.path.join(modeldict, filename), frontmatter_updates = updates)
    # imagename = "dgm222_TreatAtEndOfLife.jpeg"
    # linktodiagram = "dgmA5COLON_Treat_at_End_of_Life138.html"
    # s = open_html(os.path.join(modeldict, filename))
    # s = add_decomposition_images(s, imagename, linktodiagram)
    # save_html(s, os.path.join(modeldict, filename))
    
    filename = "actuseProduce_in_a_circular_economy25.html"
    imagename = "dgm23.jpeg"
    linktodiagram = "dgmA0COLON_Produce_in_a_circular_economy2650.html"
    s = open_html(os.path.join(modeldict, filename))
    s = add_decomposition_images(s, imagename, linktodiagram)
    save_html(s, os.path.join(modeldict, filename))
    
    # filename = "index.html"
    # updates = {"notetitle": "Note", "note": "The Circular Product Design (CPD) Activity Model describes a single activity of the broader Production in a Circular Economy (CE) Model in depth, providing examples that are relevant for designing in a circular economy. Further research on downstream activities (Acquire Materials, Produce Product, Use and Consume, and Treat at End of Life) is ongoing and these activities may be missing detailed descriptions within the model."}
    # update_frontmatter(os.path.join(currentdict, filename), frontmatter_updates = updates)
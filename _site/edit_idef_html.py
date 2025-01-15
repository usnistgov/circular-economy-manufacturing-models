##File with functions that update the relevant html files

## Import the libraries
import os
import re
from bs4 import BeautifulSoup as bs
import frontmatter
import datetime 

## Functions to modify files

# Open an html file in BeautifulSoup to parse
def open_html(file):
    with open(file) as fp:
        soup = bs(fp, 'html.parser')
    return soup
    
# Save the edited html file and add frontmatter for markdown files
# example_frontmatter_data = {
#        "title": "My Blog Post",
#        "author": "Your Name",
#        "date": "2024-12-26"}
def save_html(soup, file, add_fm = True, frontmatter_data = None):
    # open the file in w mode 
    # set encoding to UTF-8 
    with open(file, "w", encoding = 'utf-8') as f:
        # prettify the soup object and convert it into a string   
        f.write(soup.prettify(formatter="html"))
        f.close()
    
    if (add_fm == True): #only add frontmatter if we want
        # open file in r mode
        with open(file, 'r') as f:
            content = f.read()
        
        #check if frontmatter (markdown headers) don't exist
        if (frontmatter.checks(content) == False):
            # Make it all jekyll compatible by adding the markdown headers with the default html (all page types)
            # convert to markdown and add frontmatter 
            post = frontmatter.Post(content, **frontmatter_data)
            
            with open(file, "w", encoding = 'utf-8') as f:
                # write the markdown header
                f.write(frontmatter.dumps(post))
                f.close()

# Use function to update frontmatter after it has already been converted to markdown
def update_frontmatter(file, frontmatter_updates = None):
    with open(file, 'r') as f:
        content = f.read()
    
    #check if frontmatter (markdown headers) exist
    if (frontmatter.checks(content) == True):
        # convert to markdown and read frontmatter 
        post = frontmatter.loads(content)
        if frontmatter_updates:
            for k, v in frontmatter_updates.items():
                post[k] = v
            #print(post.metadata)
            with open(file, "w", encoding = 'utf-8') as f:
                    # write the markdown header
                    f.write(frontmatter.dumps(post))
                    f.close()

# Remove extraneous information from the generated tree hierarchy page
def remove_from_TOC(soup, foldername):
    idx = soup.find("a", string='Collapsed Tree ')
    if idx:
        idx.parent.decompose() #removes the auto-generated link to home
    summary = soup.find("a", string='Repository Summary')
    if summary:
        summary.decompose() #removes the auto-generated link to summary and nobr tag that surrounds it
    tocjs = soup.find("a", string='Javascript Tree')
    if tocjs:
        tocjs.parent.decompose() #removes the auto-generated link to javascript TOC and nobr tag that surrounds it
    htmlhead = soup.find('head')
    if htmlhead:
        htmlhead.decompose() #remove HEAD tag and everything in it from the file
    h1 = soup.find('h1')
    if h1:
        h1.decompose() #remove H1 tag and everything in it from the file
    h2 = soup.find('h2')
    if h2:
        h2.parent.decompose() #remove nobr tag surrounding the tag and then remove it
    links = soup.find_all('a', href=True) #find links using <a> tag
    if links:
        for l in links:
            #if the folder isn't in the link path already, add it
            if foldername not in l['href']:
                #add folder nesting to href links, for example like the following: "{{'pce/actuseProduction%5Fin%5Fa%5Fcircular%5Feconomy25.html' | relative_url}}" where pce is the foldername
                # change href attribute 
                l['href'] = "{{" + "'{fn}/".format(fn=foldername) + l['href'] + "' | relative_url}}"
    bodytag = soup.find("body") #remove extraneous breaks at the beginning
    for tag in bodytag.find_all_next():
        if tag.name == "br":
            tag.decompose()
            continue
        else:
            break
    linktree = soup.find("div", id='link-tree')
    if not linktree:
        soup.body.wrap(soup.new_tag("div", attrs={'id':'link-tree','class':'link-tree'})).wrap(soup.new_tag("body"))
        soup.body.body.unwrap()
        viewablelink = soup.find('a', class_='diagram').parent
        linktree = soup.find("div", id='link-tree')
        linktree.insert_before(viewablelink)

    return soup
    
#basic formatting to remove html and body tags from files that will be markdown, remove any styling so it's all done by css
def basic_formatting(soup):
    html = soup.find('html')
    if html:
        html.unwrap() #removes the html tag but keeps its contents
    body = soup.find('body')
    if body:
        body.unwrap() #removes the body tag but keeps its contents
    style = soup.find('style')
    if style:
        style.decompose() #remove STYLE tag and everything in it from the file
    return soup
    
# Edit the div containers for Activities and Concepts to make them into two columns (Model page type)
# If icom = True, similar format but for four columns for the Input, Output, Control, Mechanism(Activity-in-Diagram page type)
def format_list_pools(soup, icom=False):
    #add ids for nav
    if (icom == True):
        inputheading = soup.find('h2', string='Input')
        if inputheading:
            inputheading['id'] = "Input"
        outputheading = soup.find('h2', string='Output')
        if outputheading:
            outputheading['id'] = "Output"
        controlheading = soup.find('h2', string='Control')
        if controlheading:
            controlheading['id'] = "Control"
        mechheading = soup.find('h2', string='Mechanism')
        if mechheading:
            mechheading['id'] = "Mechanism"
        decompheading = soup.find('h2', string='Decomposition')
        if decompheading:
            decompheading['id'] = "Decomposition"
        
        decomptag = soup.find('h2', id='Decomposition')
        inputtag = soup.find('h2', id='Input')
        outputtag = soup.find('h2', id='Output')
        controltag = soup.find('h2', id='Control')
        mechtag = soup.find('h2', id='Mechanism')
        sections = [inputtag, outputtag, controltag, mechtag]
    else:
        activityheading = soup.find('h2', string='Activities')
        if activityheading:
            activityheading['id'] = "Activities"
        conceptheading = soup.find('h2', string='Concepts')
        if conceptheading:
            conceptheading['id'] = "Concepts"
  
        activitytag = soup.find('h2', id='Activities')
        concepttag = soup.find('h2', id='Concepts')
        sections = [activitytag, concepttag]
        
    #remove extraneous bold tags
    for tag in soup.find_all("bold"):
        tag.unwrap()
    
    #wrap into divs
    #start
    flexwrapper = soup.find('div', class_='flex-items')
    if not flexwrapper:
        for section in sections:
            if section: #make sure the section doesn't return None
                startitem = section.find_next_siblings("p")
                # Create a new wrapper element
                wrapper = soup.new_tag('div', attrs={'class': 'flex-items'})

                # Iterate through the next siblings and wrap them
                current_sibling = startitem[0]
                while current_sibling and current_sibling.name == 'p':
                    next_sibling = current_sibling.find_next_sibling()
                    wrapper.append(current_sibling)
                    current_sibling = next_sibling

                # Insert the wrapper after the starting paragraph
                section.insert_after(wrapper)
        
        # Wrap the header and the div with pool items in another div
        for tag in soup.find_all("h2"): 
            if (tag.find_next_sibling()):
                if (tag.find_next_sibling().name == "div"):
                    poolitems = tag.find_next_sibling()
                    last_div = tag.wrap(soup.new_tag("div"))
                    last_div.append(poolitems)
                    
        #wrap all the divs in a flex div so they are responsive
        firsttag = soup.find("div", recursive=False)

        if firsttag:
            followingdivs = firsttag.find_next_siblings("div")
            if (icom == True):
                firstdiv = firsttag.wrap(soup.new_tag('div', attrs={'class': 'flex-container-two'}))
            else:
                firstdiv = firsttag.wrap(soup.new_tag('div', attrs={'class': 'flex-container'}))
            if (followingdivs):
                for nextdiv in followingdivs:
                    firstdiv.append(nextdiv)

    #add nav
    if not soup.find('nav'):
        nav_html = bs("", 'html.parser')
        new_tag = nav_html.new_tag("nav")
        nav_html.append(new_tag)
        
        new_tag = nav_html.new_tag("ul")
        new_tag["class"] = "diag-nav-bar"
        nav_html.nav.append(new_tag)
        
        if (icom == True):
            new_tag = nav_html.new_tag("a", href="#Decomposition", attrs={'class':'navlinks'})
            new_tag.string = "Decomposition"
            nav_html.nav.ul.append(new_tag)
            
            new_tag = nav_html.new_tag("a", href="#Input", attrs={'class':'navlinks'})
            new_tag.string = "ICOM"
            nav_html.nav.ul.append(new_tag)
            
        else:
            new_tag = nav_html.new_tag("a", href="#Activities", attrs={'class':'navlinks'})
            new_tag.string = "Activities"
            nav_html.nav.ul.append(new_tag)
            
            new_tag = nav_html.new_tag("a", href="#Concepts", attrs={'class':'navlinks'})
            new_tag.string = "Concepts"
            nav_html.nav.ul.append(new_tag)
        
        allnavs = nav_html.find_all('a')
        for navelement in allnavs:
            new_tag = nav_html.new_tag("li")
            new_tag["class"] = "diag-nav-item"
            navelement.wrap(new_tag)
        
        soup.h2.insert_before(nav_html)
    return soup

# Remove bullet points from items that are description information, not pool-items by adding the CSS class (all page types)
# Remove extraneous information (Creator, Purpose, View, Context)
# Add class "info" to format body text under all Description headers (all page types)
def remove_extraneous_info(soup):
    keeplist = ['description']
    toremove = soup.find_all('p', class_ = "textfield", id = lambda x: x not in keeplist) # remove textfield class unless it's has id = description
    for item in toremove:
        if item:
            item.decompose()
        
    keepbullets = ['poolitem']
    descriptioninfo = soup.find_all('p', class_ = lambda x: x not in keepbullets)
  
    if not soup.find('p', class_='description-info'):
        for item in descriptioninfo:
            if item:
                item['class'] = ['description-info']
                #add colon after any text right before a link to diagram to make text formatting consistent
                a = item.find('a')
                if a:
                    label = a.find_previous_sibling() #find that tag (it will have a <b> tag since it is bolded
                    if label:
                        labelstring = label.get_text().strip() #text only
                        if labelstring:
                            if ":" not in labelstring: #only if doesn't have a colon already
                                label.string = labelstring+(":") #get the text only and add a colon

    descriptionlabel = soup.find('p', id="description")
    desc = descriptionlabel.find_next_siblings(limit=1)[0]
    if (desc) and (desc.name != 'p'):
        if desc.get_text():
            desc.wrap(soup.new_tag('p', attrs={'class': 'info'}))
    
    #fix some formatting for the descriptions to remove breaks
    descriptioncontent = soup.find('p', class_="info")
    if descriptioncontent:
        for tag in descriptioncontent.find_next_siblings(limit=2):
            if tag.name == "br":
                tag.decompose()
    
    
    return soup
    
def format_diagram_images(soup):
    imgs = soup.find_all('img')
    if not soup.find("div", class_="modelimage"):
        for img in imgs:
            img.wrap(soup.new_tag('div', attrs={'class': 'modelimage'})) #centers diagram images
    return soup
    
def add_decomposition_images(soup, imagename, linktodiagram):
    owner_label = soup.find("div", class_="flex-container-two") #find the last container on page
    if owner_label:
        if not soup.find('div', class_='image_div'):
            image_decomp = bs("", 'html.parser')
            link = image_decomp.new_tag('a') #create link for image
            link['href'] = linktodiagram
            image = image_decomp.new_tag('img', attrs={'alt':"", 'border':"0"}) #set image
            image['src'] = "../manual_images/" + imagename
            image_decomp.append(image)
            image_decomp.append(link)
            wrapped_img = image.wrap(link)  #wrap image in link
            image_div = wrapped_img.wrap(image_decomp.new_tag('div', attrs={'class':'image_div'})) #and then wrap link in div
            owner_label.insert_after(image_decomp) #insert the manually generated diagram after the ICOM lists
    return soup

def update_time(soup, updateid):
    # Returns the current local date
    today = datetime.datetime.now().ctime()
    lastupdated = soup.find('i', id=updateid)
    if lastupdated:
        lastupdated.string.replace_with(today)
    return soup
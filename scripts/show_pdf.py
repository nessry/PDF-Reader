# -*- coding: utf-8 -*-

import fitz                   # this is PyMuPDF
import PySimpleGUI as sg

# Display content of the pdf file in a separate interface
def display_pdf(file, icon, w, max_size):

    doc = fitz.open(file)
    page_count = len(doc)
    
    # allocate storage for page display lists
    dlist_tab = [None] * page_count
    title = "Display of '%s', pages: %i" % (file, page_count)
    
    # read the page data
    def get_page(pno, zoom=False, max_size=None):
        
        dlist = dlist_tab[pno]  # get display list of page number
        if not dlist:  # create if not yet there
            dlist_tab[pno] = doc[pno].getDisplayList()
            dlist = dlist_tab[pno]
        r = dlist.rect  # the page rectangle
        clip = r
        # ensure image fits screen:
        # exploit, but do not exceed width or height
        zoom_0 = 1
        
        if max_size:
            zoom_0 = min(1, max_size[0] / r.width, max_size[1] / r.height)
            if zoom_0 == 1:
                zoom_0 = min(max_size[0] / r.width, max_size[1] / r.height)
                
        mat_0 = fitz.Matrix(zoom_0, zoom_0)

        if not zoom:  # show the total page
            pix = dlist.getPixmap(matrix=mat_0, alpha=False)
        else:
            w2 = r.width / 2
            h2 = r.height / 2
            clip = r * 0.5  # clip rect size is a quarter page
            tl = zoom[0]  # old top-left
            tl.x += zoom[1] * (w2 / 2)
            tl.x = max(0, tl.x)
            tl.x = min(w2, tl.x)
            tl.y += zoom[2] * (h2 / 2)
            tl.y = max(0, tl.y)
            tl.y = min(h2, tl.y)  # the page rect
            clip = fitz.Rect(tl, tl.x + w2, tl.y + h2)
            # clip rect is ready, now fill it
            mat = mat_0 * fitz.Matrix(2, 2)  # zoom matrix
            pix = dlist.getPixmap(alpha=False, matrix=mat, clip=clip)

        img = pix.getImageData("ppm")  # make PPM image from pixmap for tkinter
        
        return img, clip.tl  # return image, clip position
    
    form = sg.FlexForm(
        title, return_keyboard_events=True, location=(w / 3, 0), icon=icon, use_default_focus=False
    )
    
    cur_page = 0
    data, clip_pos = get_page(
        cur_page,  # read first page
        zoom=False,  # not zooming yet
        max_size=max_size,  # image max dim
    )
    
    image_elem = sg.Image(data=data)  # make image element

    goto = sg.InputText(
        str(cur_page + 1), size=(5, 1), do_not_clear=True, key="PageNumber"
    )  # for display & input
    
    layout = [  # the form layout
                [
                        sg.ReadFormButton("Prior"),
                        sg.ReadFormButton("Next"),
                        sg.Text("Page:"),
                        goto,
                        sg.Text("(%i)" % page_count),
                        sg.ReadFormButton("Zoom"),
                        sg.Text("(toggle on/off, use arrows to navigate while zooming)"),
                ],
                [image_elem],
        ]
                
    form.Layout(layout)  # define the form
    
    # define the buttons / events we want to handle
    def is_Enter(btn):
        return btn.startswith("Return:") or btn == chr(13)

    def is_Quit(btn):
        return btn == chr(27) or btn.startswith("Escape:")

    def is_Next(btn):
        return btn.startswith("Next") or btn == "MouseWheel:Down"

    def is_Prior(btn):
        return btn.startswith("Prior") or btn == "MouseWheel:Up"
    
    def is_Up(btn):
        return btn.startswith("Up:")

    def is_Down(btn):
        return btn.startswith("Down:")

    def is_Left(btn):
        return btn.startswith("Left:")

    def is_Right(btn):
        return btn.startswith("Right:")

    def is_Zoom(btn):
        return btn.startswith("Zoom")

    def is_MyKeys(btn):
        return any((is_Enter(btn), is_Next(btn), is_Prior(btn), is_Zoom(btn)))
    
    # zoom toggle
    zoom_active = False
    
    while True:
        btn, value = form.Read()
        if btn is None and (value is None or value["PageNumber"] is None):
            break
        if is_Quit(btn):
            break
        zoom_pressed = False
        zoom = False
        if is_Enter(btn):
            try:
                cur_page = int(value["PageNumber"]) - 1  # check if valid
            except:
                cur_page = 0
        elif is_Next(btn):
            cur_page += 1
        elif is_Prior(btn):
            cur_page -= 1
        elif is_Up(btn) and zoom_active:
            zoom = (clip_pos, 0, -1)
        elif is_Down(btn) and zoom_active:
            zoom = (clip_pos, 0, 1)
        elif is_Left(btn) and zoom_active:
            zoom = (clip_pos, -1, 0)
        elif is_Right(btn) and zoom_active:
            zoom = (clip_pos, 1, 0)
        elif is_Zoom(btn):
            zoom_pressed = True
            if not zoom_active:
                zoom = (clip_pos, 0, 0)
                
        # sanitize page number
        while cur_page >= page_count:
            cur_page -= page_count
            
        while cur_page < 0:
            cur_page += page_count
            
        if zoom_pressed and zoom_active:
            zoom = zoom_pressed = zoom_active = False
            
        data, clip_pos = get_page(cur_page, zoom=zoom, max_size=max_size)
        image_elem.Update(data=data)
        zoom_active = zoom_pressed or zoom
        
        # update page number field
        if is_MyKeys(btn):
            goto.Update(str(cur_page + 1))
            
    doc.close()
    
    

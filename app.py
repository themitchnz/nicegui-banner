from nicegui import app, ui
from PIL import Image, ImageDraw, ImageFont
import time

#make static files available to app
app.add_static_files('/data', 'data')
app.add_static_files('/banners', 'banners')

the_font = ImageFont.truetype('data/swiss.ttf',22)

#create a banner class to hold variables
class Banner:
    def __init__(self):
        self.service = 'Defence'
        self.serviceI = 0 #default to defence
        self.code = 'Course Code'
        self.name = 'Course Name'
        self.colour = '#ffe500'
        self.bannerPath = 'data/nzdf.png'
        self.services = ['Defence','Navy','Army','Air']
        self.colours = ['#ffe500','#0099d8','#c62026','#28b6ea']
        self.banners = ['data/nzdf.png','data/navy.png','data/army.png','data/air.png']

    def updateService(self):
        self.serviceI = self.services.index(self.service)
        self.bannerPath = self.banners[self.serviceI]
        if self.code == "": self.code = 'Course Code'
        if self.name == "": self.name = 'Course Name'

#create instance of a banner
banner = Banner()

#Create banner image and save to disk / update preview
def create_banner():
    banner.updateService()

    #actual image maniupulation
    ban = Image.open(banner.bannerPath)
    img = ImageDraw.Draw(ban)
    img.text((205,130),banner.code,font=the_font, fill=(banner.colours[banner.serviceI]))
    img.text((205,160),banner.name,font=the_font, fill=(255,255,255))
    banner_name = 'banners/' + banner.code + '.png'
    ban.save(banner_name) #save to disk
    ban.close()

    banner.bannerPath = banner_name
    timestamp = '?time=' +  str(time.time()) #stops image from caching in the browser
    img_ban.set_source(banner_name + timestamp)

def clearUI():
    code.set_value('')
    name.set_value('')
    service.set_value('Defence')

img_ban = ui.image(banner.bannerPath)

with ui.card() as card:
    ui.label('Select Service')
    service = ui.radio(['Defence','Navy','Army','Air'], value='Defence', on_change=create_banner).props('inline').bind_value_to(banner, 'service')
    code = ui.input ( label='Course Code', placeholder='Course Code',  on_change=create_banner).bind_value_to(banner, 'code')
    name = ui.input ( label='Course Name', placeholder='Course Name',  on_change=create_banner).bind_value_to(banner, 'name')
    with ui.row():
        ui.button('Clear', on_click=clearUI)
        ui.button('Save', on_click=lambda: ui.download(banner.bannerPath)).props('align=right')

ui.run(title='Totara Banner Creator')








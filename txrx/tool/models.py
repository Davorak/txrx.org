from django.db import models
from django.conf import settings
from lablackey.photo.models import Photo
from lablackey.main.models import SlugModel,OrderedModel
from lablackey.utils import cached_method
from sorl.thumbnail import ImageField

_order_default = 9999

class Lab(SlugModel):
    _folder = settings.UPLOAD_DIR+'/photos/lab/%Y-%m'
    src = ImageField("Thumbnail",max_length=300,upload_to=_folder,null=True,blank=True)
    order = models.IntegerField(default=_order_default)
    width = 560
    height = 420
    dimensions = lambda self: "%sx%s"%(self.width,self.height)
    wrapper_width = lambda self: self.width*self.tools.count()
    tools = property(lambda self: self.tool_set.all())
    class Meta:
        ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(SlugModel):
    lab = models.ForeignKey(Lab)
    make = models.CharField(max_length=64,null=True,blank=True)
    model = models.CharField(max_length=32,null=True,blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=_order_default)
    _folder = settings.UPLOAD_DIR+'/photos/tools/%Y-%m'
    thumbnail = ImageField(max_length=300,upload_to=_folder,null=True,blank=True,
                           help_text=_help%"first")
    @property
    def src(self):
        if self.thumbnail: return self.thumbnail
        return self.toolphoto_set.all()[0].src
    links = lambda self: self.toollink_set.all()
    slides = lambda self: self.toolslide_set.all()
    videos = lambda self: self.toolvideo_set.all()
    project = lambda self: self.project_set.all()
    class Meta:
        ordering = ("order",)

class ToolVideo(models.Model):
    from project.models import Project
    tool = models.ForeignKey(Tool)
    order = models.IntegerField(default=_order_default)
    title = models.CharField(max_length=64)
    embed_code = models.TextField()
    _folder = settings.UPLOAD_DIR+'/photos/tools/%Y-%m'
    thumbnail = ImageField(max_length=300,upload_to=_folder,null=True,blank=True,
                           help_text=_help%"project")
    project = models.ForeignKey(Project,null=True,blank=True)
    @property
    def src(self):
        if self.thumbnail: return self.thumbnail
        return self.project.first_photo
    __unicode__ = lambda self: self.title
    class Meta:
        ordering = ("order",)

class ToolLink(models.Model):
    tool = models.ForeignKey(Tool)
    order = models.IntegerField(default=_order_default)
    title = models.CharField(max_length=64)
    url = models.URLField(verify_exists=False)
    __unicode__ = lambda self: self.title
    class Meta:
        ordering = ("order",)

class ToolPhoto(Photo):
    tool = models.ForeignKey(Tool)
    order = models.IntegerField(default=_order_default)
    class Meta:
        ordering = ("order",)
    __unicode__ = lambda self: self.title   

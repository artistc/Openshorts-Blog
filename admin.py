from django.contrib import admin 
 
from blog.models import Category
from blog.models import Entry
 
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
 
	# *** Admin list display ***	
	# Set list_display to control which fields are displayed on the change list page of the admin (default is __unicode__()).
	# http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
	# Usually, elements of list_display that aren't actual database fields can't be used in sorting (because Django does all the sorting at the database level).
	# However, if an element of list_display represents a certain database field, you can indicate this fact by setting the admin_order_field attribute of the item.
	list_display = ('title', 'format_description')
 
	def format_description(self, modelCategory):
		#return obj.__class__.__name__
		if len(modelCategory.description) < 100: 
			return modelCategory.description
		else:
			return modelCategory.description[0:100]+'...'
 
	format_description.admin_order_field = 'description' # if sort by 'format_description' needed, sort by 'description' field.
 
 
class EntryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
 
	# *** multiply-select field ***
	# http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal
	filter_horizontal = ['categories']
	#filter_vertical = ['categories']
 
	# *** Admin list display ***
	# http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
	list_display = ('title', 'author', 'pub_date', 'excerpt', 'colored_status')
	def colored_status(self, modelEntry):
		status_str = modelEntry.get_status_display()	#http://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_FOO_display
		color_str = "Black"
		if modelEntry.status == modelEntry.LIVE_STATUS: color_str = "Green"
		elif modelEntry.status == modelEntry.DRAFT_STATUS: color_str = "Red"
		elif modelEntry.status == modelEntry.HIDDEN_STATUS: color_str = "Gray"
		return '<span style="color: %s;">%s</span>' % (color_str, status_str)
	colored_status.allow_tags = True
	colored_status.admin_order_field = 'status'	
 
 
admin.site.register(Category, CategoryAdmin) 
admin.site.register(Entry, EntryAdmin)
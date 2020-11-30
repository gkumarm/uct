from django import template

register = template.Library()


@register.filter(name='get_name_by_index')
def get_name_by_index(nlist, pos):
#	print (pos-2, "->", type (nlist), list (list (nlist)[0])[1][2])
	return nlist[pos-1]

@register.filter(name='multadd')
def multadd(a,b,c):
#	print (pos-2, "->", type (nlist), list (list (nlist)[0])[1][2])
	return (a*b)+c
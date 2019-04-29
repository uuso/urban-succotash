# coding: utf-8
from django.core.management import BaseCommand
from tasks.models import TodoItem
from django.contrib.auth.models import User

def bubblesort(source, comparisonfunc):
	slist = [] + source
	for i in range(len(slist)):
		# print(f'Pre: {slist}, {i}')
		for j in range(i+1, len(slist)):
			if comparisonfunc(slist[i],slist[j]):
				temp = slist[i]
				slist[i] = slist[j]
				slist[j] = temp
	return slist

def ulist_lt(a, b):
	return a[1] < b[1]

class Command(BaseCommand):
	help = u"Display every user's tasks amount"

	def add_arguments(self, parser):
		parser.add_argument('--top', dest='top', type=int, default=25)

	def handle(self, *args, **options):
		ulist = []
		for u in User.objects.all():
			# curr = ( u, len(u.tasks.filter(is_completed = False)) )
			curr = ( u, len(u.tasks.all()) )
			ulist.append(curr)

		sulist = bubblesort(ulist, ulist_lt)

		i = 1
		ic = 0
		for _ in sulist[:options['top']]:
			incomp = len(_[0].tasks.all().filter(is_completed = False))
			if incomp < 20:
				ic += 1
			print(f'#{i}. {_} incomp: {incomp} icnum: {ic}')
			i += 1


	# # def handle(self, *args, **options):
	# 	less20 = 0
	# 	for u in User.objects.all():
	# 		count = 0
	# 		for t in u.tasks.all():
	# 			if t.is_completed == False:
	# 				count += 1
	# 		if count <= 20:
	# 			less20 += 1
	# 	print(less20)
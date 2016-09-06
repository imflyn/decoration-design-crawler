li = [' ', '     ', '', 'a']
for s in li[:]:
	if s.strip() == '':
		li.remove(s)
print(li)

import sys

def directives(code: str) -> list[str]:
	labels = {}
	dir_start_sym = '$'

	code = code.split('\n')

	i = 0
	while i < len(code):
		isDefine = code[i].startswith(f'{dir_start_sym}DEFINE')
		isLabel = code[i].startswith(f'{dir_start_sym}LABEL')

		if isDefine:
			parts = code[i].split(' ', 2)
			if len(parts) == 3:
				label, value = parts[1], parts[2]
				labels[label] = value
			code.pop(i)
			i -= 1

		elif isLabel:
			parts = code[i].split(' ', 1)
			if len(parts) == 2:
				label = parts[1]
				labels[label] = str(i)
		
			code.pop(i)
			i -= 1

		i += 1

	code = '\n'.join(code)
		
	for label, value in labels.items():
		code = code.replace(label, value)

	return code

def preprocessor(code: str) -> str:
	code = code.split('\n')

	i = 0

	while i < len(code):
		code[i] = code[i].split(';', 1)[0]
		code[i] = code[i].strip()
		code[i] = code[i].upper()
		if code[i] == '': 
			code.pop(i)
			i -= 1
		
		i += 1

	code = directives('\n'.join(code)).split('\n')
	
	return code

# For testing purposes. Not intended to be run independently.

if __name__ == '__main__':
	with open(sys.argv[1], 'r') as file:
		code = file.read()
	print(preprocessor(code))
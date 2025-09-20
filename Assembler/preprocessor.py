import sys
import re

def directives(code: str) -> list[str]:
	labels = {}
	dir_start_sym = '$'

	code = code.split('\n')

	i = 0
	while i < len(code):
		isDefine = code[i].startswith(f'{dir_start_sym}DEFINE')
		isLabel = code[i].startswith(f'{dir_start_sym}LABEL')
		isInclude = code[i].startswith(f'{dir_start_sym}INCLUDE')

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
		
		elif isInclude:
			parts = code[i].split(' ', 1)
			if len(parts) == 2:
				filename = parts[1]
				try:
					with open(filename, 'r') as f:
						included_code = f.read()
					included_code = directives(included_code)
					code.pop(i)
					for line in reversed(included_code):
						code.insert(i, line)
					i -= 1
				except FileNotFoundError:
					print(f'Error: Included file "{filename}" not found.')
					code.pop(i)
					i -= 1
			else:
				code.pop(i)
				i -= 1

		i += 1

	code = '\n'.join(code)
		
	for label, value in labels.items():
		code = code.replace(label, value)

	return code

def macros(code: str) -> str:
	code = re.sub(r'(LDI|ADD|SUB|MUL|DIV|NEG|SHL|SHR|AND|OR|NAND|NOR|NOT|XOR|XNOR) (\w+), \[([0X]?\w+)\]', r'LDI RAM_PTR, \3\n\1 \2, RAM', code)
	code = re.sub(r'(LDI|ADD|SUB|MUL|DIV|NEG|SHL|SHR|AND|OR|NAND|NOR|NOT|XOR|XNOR) \[([0X]?\w+)\], ([0X]?\w+)', r'LDI RAM_PTR, \2\n\1 RAM, \3', code)
	code = re.sub(r'STACK_INIT\n', r'LDI SP, 0\n', code)
	code = re.sub(r'PUSH (\w+)', r'SUB SP, 1\nLDI RAM_PTR, SP\nLDI RAM, \1', code)
	code = re.sub(r'POP (\w+)', r'LDI RAM_PTR, SP\nLDI \1, RAM\nADD SP, 1', code)
	code = re.sub(r'\nPOP\n', r'\nADD SP, 1\n', code)
	
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

	code = directives('\n'.join(code))
	code = macros(code)
	code = code.split('\n')
	
	return code

# For testing purposes. Not intended to be run independently.

if __name__ == '__main__':
	with open(sys.argv[1], 'r') as file:
		code = file.read()
	print(preprocessor(code))
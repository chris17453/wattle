import sys


arguments = len(sys.argv) - 1

json_arguments=json.dumps(arguments)

print (json_arguments)
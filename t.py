import os
root = os.getcwd()
files = ['..']+os.listdir(root)
arr = '\r\n'.join(['<a link="{0}">{0}</a>'.format(file) for file in files])
print(bytes(arr))

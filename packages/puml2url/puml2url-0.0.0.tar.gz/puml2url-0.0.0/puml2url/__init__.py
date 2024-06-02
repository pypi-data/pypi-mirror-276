import base64, string, httplib2, six
from zlib import compress
from six.moves.urllib.parse import urlencode

if six.PY2:
	from string import maketrans
    from urllib import urlretrieve
else:
	maketrans = bytes.maketrans
    from urllib.request import urlretrieve

def convert_diagram_to_url(plantuml_text,_type='png', server_url='https://www.plantuml.com/plantuml'):
	if _type not in ['svg', 'png', 'txt']:
		return None

	base = server_url + "/" + _type + "/"

	plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
	base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
	b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))

	"""zlib compress the plantuml text and encode it for the plantuml server."""
	zlibbed_str = compress(plantuml_text.encode('utf-8'))
	compressed_string = zlibbed_str[2:-4]
	output = base+base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')
    return output

def download_image_from_url(url, download_file_as):
    try:
        urlretrieve(url, download_file_as)
        return True
    except Exception as e:
        print(e)
        return False

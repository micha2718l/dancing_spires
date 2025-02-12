
from pathlib import Path
import tempfile
import json

from flask import Flask, send_file, request, send_from_directory
from flask_cors import CORS

import dancing_spires as ds


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

#app = Flask(__name__, static_url_path='/spires-nuxt/dist')
'''
spires_nuxt_path = 'spires-nuxt/dist'

@app.route('/<path:path>')
@app.route('/')
def send_nuxt(path=None):
    print(path)
    if not path:
        path = 'index.html'
    return send_from_directory(spires_nuxt_path, path)

@app.route('/_nuxt/<path:path>')
def send__nuxt(path):
    return send_from_directory(f'{spires_nuxt_path}/_nuxt', path)
'''



@app.route("/spire_dance_custom.gif", methods=['GET', 'POST'])
def doom_spire_lightning_custom():
    frames = request.args.get('frames', default = ds.frames_default, type = int)
    width = request.args.get('width', default = ds.width_default, type = int)
    height = request.args.get('height', default = ds.height_default, type = int)
    duration = request.args.get('duration', default = ds.duration_default, type = int)
    setupStr = request.args.get('setup', default=None)
    #print(json.dumps(setupStr))
    if setupStr is None:
        images = ds.SpireDanceV2(frames=frames, width=width, height=height, setup=ds.default_setupV2)
    else:
        images = ds.SpireDanceV2(frames=frames, width=width, height=height, setup=json.loads(setupStr))
    

    file_name = "spire_dance_custom.gif"

    with tempfile.TemporaryDirectory() as tmpdirname:
        path = Path(tmpdirname) / Path(file_name)
        images[0].save(path,
            save_all=True,
            append_images=images[1:],
            optimize=True,
            duration=duration,
            loop=0)
        return send_file(path, mimetype='image/gif')


@app.route("/spire_dance.gif", methods=['GET', 'POST'])
def doom_spire_lightning():

    frames = request.args.get('frames', default = ds.frames_default, type = int)
    w = request.args.get('width', default = ds.width_default, type = int)
    h = request.args.get('height', default = ds.height_default, type = int)
    duration = request.args.get('duration', default = ds.duration_default, type = int)

    images = ds.spires_lightning_demo_0().images()

    file_name = "spire_dance.gif"

    with tempfile.TemporaryDirectory() as tmpdirname:
        path = Path(tmpdirname) / Path(file_name)
        images[0].save(path,
            save_all=True,
            append_images=images[1:],
            optimize=True,
            duration=duration,
            loop=0)
        return send_file(path, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True)

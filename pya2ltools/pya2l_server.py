from pathlib import Path
from flask import Flask, Response, request
from tempfile import TemporaryDirectory, TemporaryFile

app = Flask(__name__)

from .a2l.tools.update_a2l import update_a2l


@app.post("/a2l/update")
def a2l_update():

    if not request.files:
        return {"error": "Request must have files"}, 400
    a2l = request.files.get("a2l")
    elf = request.files.get("elf")
    if a2l is None or elf is None:
        return {"error": "Missing a2l or elf in request"}, 400

    with TemporaryDirectory() as temp_dir:
        a2l_path = Path(temp_dir + "/" + a2l.name)
        elf_path = Path(temp_dir + "/" + elf.name)
        a2l.save(a2l_path)
        elf.save(elf_path)
        update_a2l(a2l_path, elf_path)
        with open(a2l_path, "r") as f:
            content = f.read()
    return {"a2l": content}

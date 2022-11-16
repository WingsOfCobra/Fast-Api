import tempfile
from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageSequence
import os, io
import shutil
from tempfile import SpooledTemporaryFile


api = FastAPI(docs_url="/")


@api.post("/file")
async def upload(
  file: UploadFile = File(...)
):
  if file.content_type ==  "image/tiff":
    nfile = tiff_to_pdf(file)
    return {nfile}

def tiff_to_pdf(file:  UploadFile):

  output = io.BytesIO()
  Image.open(file.file._file).convert("RGB").save(output, format="pdf")
  output.seek(0, 0)
  n_file = UploadFile('file.pdf', output)
  return n_file


if __name__ =='__main__':
  import uvicorn
  uvicorn.run('api:api', reload=True)
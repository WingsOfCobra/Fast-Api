import os, sys
import shutil
import time
from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageSequence
import io

sys.path.append(".")

api = FastAPI(docs_url="/")


@api.post("/file")
async def upload(
  file: UploadFile = File(...)
):
  if file.content_type ==  "image/tiff":
    nfile = tiff_to_pdf(file)
    print(nfile)
    return {nfile}

def tiff_to_pdf(file:  UploadFile):
  if os.path.isdir("files") == False:
    os.mkdir("files")
    return tiff_to_pdf(file)
  else:
    output = io.BytesIO()
    image = Image.open(file.file._file)
    output.seek(0, 0)
    pdf_path = "files/" + file.filename.lower().replace('.tif', '.pdf' )
  
    images = []
    for i, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)
    if len(images) == 1:
        n_file = UploadFile(file.filename.lower().replace('.tif', '.pdf'), output)
        images[0].save(pdf_path)
    else:
        n_file = UploadFile(file.filename.lower().replace('.tif', '.pdf'), output)
        images[0].save(pdf_path, save_all=True,append_images=images[1:])
    
    os.remove(pdf_path)

    return n_file
  

if __name__ =='__main__':
  import uvicorn
  uvicorn.run('api:api', reload=True)
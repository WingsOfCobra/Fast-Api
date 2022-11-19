import os, sys
import shutil
import time
from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageSequence
import io

sys.path.append(".")

api = FastAPI(
  docs_url="/",
  title="Der Einbruch"
  )


# File system

@api.post("/upload", tags=["File system"])
async def upload(
  path: str,
  file: UploadFile = File(...),
):
  if path:
    if not os.path.isdir(path):
      os.mkdir(path)
    
    fpath = f"{path}/{file.filename}"
    nfile = open(fpath, "w")
    nfile.write(fpath)
    nfile.close()
    return {"success": True, "message": "File Upload successfully", "file": file.filename, "path": path}
    
  else:
    return {"success": False, "message": "Please enter a path"}
  

@api.post("/tiff_to_pdf", tags=["File system"])
async def tiff_to_pdf_upload(
  file: UploadFile = File()
):
  if file.content_type ==  "image/tiff":
    nfile = tiff_to_pdf(file)
    print(nfile)
    return {nfile}

@api.delete("/delete_folder", tags=["File system"])
async def delete(
  path: str,
  remove_tree: bool
):
  if os.path.isdir(path):
    if remove_tree:
      f = shutil.rmtree(path)
      return{"success": True, "message": f"Deleted folder tree", "path": f"{path}/"}
    else:
      try:
        os.rmdir(path)
        return {"success": True, "message": f"Deleted folder", "path": path}
      except OSError as error:
        return {"success": False, "message": f"{error}"}
  else:
    return{"success": False, "message": "Please enter valid folder path"}

@api.delete("/delete_files", tags=["File system"])
async def delete(
  path: str,
):
  if os.path.isfile(path):
    f = os.remove(path)
    return {"success": True, "message": "File successfully removed", "file": path}
  else:
    return {"success": False, "message": "Please enter a valid file path"}
    




# Functions


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
# this is the endpoints
from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, staticfiles
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json
import csv
from  src.helper import llm_pipeline



# iitialise the fastaapi
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.post("/upload")
async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    base_folder = 'static/docs/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    pdf_filename = os.path.join(base_folder, filename)


    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)

    
    response_data = jsonable_encoder(json.dumps({"msg": "success", "pdf_filename": pdf_filename}))
    res = Response(response_data)
    return res

## another funciton to get the csv  / complete result
def get_csv(file_path):
    answer_generation_chain, ques_list = llm_pipeline(file_path)
    base_folder = "static/output/"
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = base_folder + "QA.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow({"Question", "Answer"})  # creating the headers in csv


        for question in ques_list:
            print("Question", question)
            answer = answer_generation_chain.run(question)
            print("Answer", answer)
            print("-------------------------------------------------------------------\n\n")


            # save answer to csv file
            csv_writer.writerow([question, answer])
        return output_file
    

# this function will do load the output file and return 
@app.post("/analyze")
async def chat(request: Request, pdf_filename: str = Form(...)):
    output_file = get_csv(pdf_filename)
    response_data = jsonable_encoder(json.dumps({"output_file": output_file}))


if __name__ == "__main__":
    uvicorn.run("app.py", host="0.0.0.0", port= 8080, reload=True)
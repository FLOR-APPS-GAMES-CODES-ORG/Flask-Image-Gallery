from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
import os
import glob
import sys
import binascii
import argparse
import openpyxl
import pandas as pd
import json
sheet=None

def get_sheet(excl):
    xls = pd.ExcelFile(excl)
    sheet=xls.sheet_names[3]

    return sheet

def get_word_data(word):
    sheetx=sheet
    excl="word_story_image.xlsx"
    if(sheetx==None):
       sheetx= get_sheet(excl)
    df = pd.read_excel(excl, sheet_name=sheetx)
    wordmatches=df[df["Dutch"]==str(word)].to_json(orient="columns")
    return str(wordmatches)+"ik,i,story  asdfaf,183b82ec6cf0c5d603fd19bdf31c9e062aad7b87.png"


app = Flask("Flask Image Gallery")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
def encode(x):
    return  x #binascii.hexlify(x.encode('utf-8')).decode()
def decode(x):
    return x #binascii.unhexlify(x.encode('utf-8')).decode()
@app.route('/noroot')
def home():
    root_dir =  "assets" #app.config['ROOT_DIR']
    image_paths = []
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                image_paths.append(encode(os.path.join(root,file)))
    return render_template('index.html', paths=image_paths)

@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

@app.route('/worddata/<word>')
def getWordData(word):
    word_data = get_word_data(word) 
    return  word_data # send_from_directory(word_data, as_attachment=False)

if __name__=="__main__":
    get_word_data("hebben")
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    #parser.add_argument('root_dir', help='Gallery root directory path')
    parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1', \
                                    help='address to listen on [127.0.0.1]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                                default=5000, help='port to listen on [5000]')
    args = parser.parse_args()
    #app.config['ROOT_DIR'] = args.root_dir
    app.run(host=args.host, port=args.port, debug=True)

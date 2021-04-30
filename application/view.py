import re
import time
import os
from random import randint
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *
from werkzeug.utils import secure_filename
import requests
import json

app=Flask(__name__,instance_relative_config=True)




app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path,'F:/Program Files/Microsoft SQL Server/MSSQL15.MSSQLSERVER/MSSQL'))

app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI']="mssql+pyodbc://DESKTOP-URHHJQ5/atm6?driver=SQL+Server?trusted_connection=yes"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



class song(db.Model) :

    "creating tables using flask_sqlalchemy"

    id = db.Column( db.Integer,primary_key=True)
    Name_of_song = db.Column(db.String(100),nullable=False,unique=True)
    duration_time=db.Column(db.Integer,default=0,nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)


class audioBook(db.Model):

    "creating tables using flask_sqlalchemy"

    id = db.Column( db.Integer,primary_key=True)
    title = Column(db.String(100), nullable=False)
    author = Column(db.String(100), nullable=False)
    narrator = Column(db.String(100), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    duration_time=db.Column(db.Integer,default=0,nullable=False)


class podcast(db.Model):

    "creating tables using flask_sqlalchemy"

    id = db.Column( db.Integer,primary_key=True)
    name = Column(db.String(100), nullable=False)
    host = Column(db.String(100), nullable=False)
    participants = Column(db.Text, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration_time=db.Column(db.Integer,default=0,nullable=False)
 



audiofiletype = {"song": song, "audiobook": audioBook, "podcast": podcast}



@app.route('/',methods=['POST','GET'])
def menu():

    return render_template('option.html')


 
 

@app.route('/create',methods=['POST','GET'])
def create():

    "Taking input from local file and creating and storing the data in databases "
    
    if request.method=='GET':
        #data1=request.args.get('file')

        """if we need we can take input from UI by using URL and also we get input by using file path,
        but now we considered using file path"""

        with open('C:/Users/ADMIN/Desktop/js.json','r') as f:
            data1=f.read()
        data=json.loads(data1)

        type=data[0].get('audioFileType',None)  # findinng the type of file
        if type is None:
            return 'the request is invalid:400 bad request',400
        aud_type=audiofiletype.get(type)  #checking the type of file is existing in audiofiletype 
        metadata = data.get("audioFileMetadata") 


        if metadata['duration_time']<0:
            metadata['duration_time']=0
        metadata['uploaded_time']=datetime.datetime.utcnow()

        if type=='song':
            name = metadata.get("Name_of_the_song", None)
            if (name is None or any(i for i in participent if len(i))):
                return "The request is invalid: 400 bad request",400
            try:
                aud_obj=song(**metadata)
                db.session.add(aud_obj)
                db.session.commit()
                return '200 OK', 200
            except:
                return "The request is invalid: 400 bad request", 400
        elif type=='podcast':
            obj=metadata.get('participants',None)
            if (obj is None or len(bj)>10 or 
                any(i for i in obj if len(i) > 100)):
                return 'The request is invalid: 400 bad request',400
            try:
                aud_obj=podcast(**metadata)
                db.session.add(aud_obj)
                db.session.commit()
                return '200 OK', 200
            except:
                return 'The request is invalid: 400 bad request', 400
        elif type=='audioBook':
            obj1=metadata.get('author',None)
            if (obj1 is None or any(i for i in obj1 if len(i)>100)):
                return 'The request is invalid: 400 bad request', 400
            aud_obj=audioBook(**metadata)
            db.session.add(audio_obj)
            db.session.commit()
            return '200 OK', 200
        return "The request is invalid: 400 bad request", 400



@app.route('/update/<audioFileType>/<audioFileID>',methods=['PUT'])
def update(audioFileType, audioFileID):

    "updating the existing file which data is stored in databases"
    
    if request.method=='PUT':
        #request_data=request.get_json()
        with open('C:/Users/ADMIN/Desktop/js.json','r') as f:
            data1=f.read()
        data=json.loads(data1)

        #type=data[0].get('audioFileType',None)  # findinng the type of file
        #if type is None:
            #return 'the request is invalid:400 bad request',400
        #aud_type=audiofiletype.get(type)  #checking the type of file is existing in audiofiletype 
       # metadata = data.get("audioFileMetadata") 


        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audiof_obj = audiofiletype.get(audioFileType)

        try:
            audio_obj = audiof_obj.query.filter_by(id=int(audioFileID))
            if not metadata:
                return "The request is invalid: 400 bad request", 400
            audio_obj.update(dict(metadata))
            db.session.commit()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400





          

@app.route('/delete/<audioFileType>/<audioFileID>', methods=["DELETE"])
def delete_api(audioFileType, audioFileID):

    "terminating the data which will be called"

    if request.method=='DELETE':
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_file_obj = audiofiletype.get(audioFileType)
        try:
            audio_obj = audio_file_obj.query.filter_by(id=int(audioFileID)).one()
            if not audio_obj:
                return "The request is invalid: 400 bad request", 400
            audio_obj.delete()
            db.session.commit()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400

    
@app.route("/get/<audioFileType>", methods=["GET"], defaults={"audioFileID": None})
def get_api(audioFileType, audioFileID):

    "getting the data from data bases choosing by passing argumets"
    
    if request.method=='GET':
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_obj = audiofiletype.get(audioFileType)
        data = None
        try:
            if audioFileID is not None:
                data = audio_obj.query.filter_by(id=int(audioFileID)).one()
                data = [dict(data)]
            else:
                data = audio_obj.query.all()
                data = [dict(i) for i in data]
            return jsonify({"data": data}), 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400



if __name__=='__main__':
    db.create_all()
    app.run(debug=True)


                
             
             
        

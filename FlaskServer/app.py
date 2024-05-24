from flask import Flask, redirect, url_for, request,jsonify,send_from_directory
import os
import json
from pyngrok import ngrok


app = Flask(__name__,static_folder="static")

# THis will be the path to the static folder that will contain the images
staticFolder = "static"

# THis will be the path to the unresolved static and the resolved static images
unresolvedRequests = "static\\UnResolvedRequests"

resolvedRequests = "static\\ResolvedRequests"

@app.route('/',methods = ["GET"])
def home():
    return "Server is running"

@app.route('/static/UnResolvedRequests/<path:filename>',methods = ["GET"])
def static_file(filename):
    return send_from_directory(os.path.join(app.static_folder,"UnResolvedRequests"), filename)

@app.route('/static/ResolvedRequests/<path:filename>', methods = ["GET"])
def static_file2(filename):
    return send_from_directory(os.path.join(app.static_folder,"ResolvedRequests"), filename)

# This is what will be used by the detector algorithm to post the image to the server
@app.route('/addImage',methods = ["POST"])
def countUp():
        global unresolvedRequests

        # Check if the post request has the file part
        if "imageFile" not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files["imageFile"]

        # Check if the file is selected
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        # Get the JSON data from the form
        if "fileName" not in request.form:
            return jsonify({"message": "No fileName part"}), 400

        fileName = request.form["fileName"]

        # Find the index number (assume findIndex() is defined elsewhere)
        indexNumber = findIndex()

        # Save the file
        file_path = f"{unresolvedRequests}\\{indexNumber + 1}.jpg"
        file.save(file_path)

        return jsonify({"message": "Image has been added"}), 200

# This will be what will be used by the frontend of the application to retrieve all the images in the unresolved requests folder
@app.route('/getUnResolvedImages',methods = ["GET"])
def getUnresolvedImages():
    unresolvedImages = []

    global unresolvedRequests

    try:   
        unresolvedImagesPath = f"{unresolvedRequests}"

        # Get list of filenames in the unresolved requests folder
        filenames = os.listdir(unresolvedImagesPath)

        # Create URLs for each image
        for filename in filenames:
            # Assuming your Flask app is hosted on localhost with port 5000
            image_url = url_for("static",filename=f'UnResolvedRequests/{filename}', _external=True, _scheme='http')
            unresolvedImages.append(image_url)
    except Exception as e:
        return jsonify({"message": "An error occured"})

    # Send the list of image URLs to the frontend
    return jsonify({"images" : unresolvedImages, "message" : "Images retrived successfully"})

# This will be what will be used by the frontend of the application to retrieve all the images in the resolved requests folder
@app.route('/getResolvedImages',methods = ["GET"])
def getResolvedImages():
    global resolvedRequests
    resolvedImages = []
    try:
        resolvedImagesPath = f"{resolvedRequests}"

        # Get list of filenames in the resolved requests folder
        filenames = os.listdir(resolvedImagesPath)

        # Create URLs for each image
        for filename in filenames:
            # Assuming your Flask app is hosted on localhost with port 5000
            image_url = url_for("static",filename=f'ResolvedRequests/{filename}', _external=True)
            resolvedImages.append(image_url)
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occured"})
    
    # Send the list of image URLs to the frontend
    return jsonify({"images":resolvedImages,"message":"Images retrived successfully"})

# This will be the request that the frontend will send to the server telling it that the image with the given index has been resolved
@app.route('/resolveImage',methods = ["POST"])
def resolveImage():
    global unresolvedRequests
    try:
        data = request.json
        index = int(data.get("index"))
        for image in os.listdir(f"{unresolvedRequests}"):
            print(image.split(".")[0],str(index))
            if (image.split(".")[0] == str(index)):
                 print("Got here")
                 os.rename(f"static\\UnResolvedRequests\\{image}", f"static\\ResolvedRequests\\{image}")
        # This will get the image from the unresolved requests folder and move it to the resolved requests folder
    except:
        return jsonify({"message": "An error occured", "code" : 404})
    return jsonify({"message": "Image has been resolved", "code" : 200})


# This will be the function that will find out the index of the new Image, it will be equal to the number of files in the folders resolved requests and unresolved requests
def findIndex():
    global resolvedRequests
    global unresolvedRequests
    return os.listdir(f"{resolvedRequests}").__len__() + os.listdir(f"{unresolvedRequests}").__len__()

# When this will be executed, the terminal will display the relevant server url, then you can modify the detection and tracking and the flask server accordingly
if __name__ == '__main__':
    app.run(host = "0.0.0.0",port = 5000)
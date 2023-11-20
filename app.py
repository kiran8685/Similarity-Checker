from flask import Flask, render_template, request, jsonify, redirect
import cv2
import os
import math
from PIL import Image
import imagehash

UPLOAD_FOLDER = 'static/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def similarity_check():
    result =""
    if request.method == "POST":
        
        image1 = request.files['image1']
        path1 = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
        image1.save(path1)
        
        image2 = request.files['image2']
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)
        image2.save(path2)
        
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path2)
        
        # Resize the images to the same dimensions
        
        img1 = cv2.resize(img1, (800, 600))
        img2 = cv2.resize(img2, (800, 600))
        # Convert the images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Apply a threshold to convert the images to binary
        _, thresh1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)
        
        # Find the common area between the two binary images
        common = cv2.bitwise_and(thresh1, thresh2)

        # Highlight the common area in the original images
        contours, _ = cv2.findContours(common, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        # THE CODE BELOW IS TO DISPLAY THE IMAGES WITH RECTANGLES..
        # RIGHT ABOVE CODE HAS DONE ALL THE WORK JUST NEED TO 
        # CONVERT THE 'NUMPY ARRAY OR PLI' TO AN IMAGE AND MAKE A VARIABLE 
        # AND SEND IT TOH THE RETURN STATEMENT AS A KEW WORD ARGUMENT
        
        # Display the images with the common area highlighted 
        
        # cv2.imshow('i1',img1) #gives output in terminal window
        # cv2.imshow('i2',img2) #gives output in terminal window
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        hash1 =imagehash.average_hash(Image.open(path1))
        hash2 =imagehash.average_hash(Image.open(path2))
        diff = hash1 - hash2
        
        per = 0
        if(diff != 0):
            per = 100 - ((diff/30) * 100)
        else:
            per = 100
        
        mse = ((gray1 - gray2) ** 2).mean()

        # Set a threshold for the MSE score
        threshold = 50

        # If the MSE score is below the threshold, consider the images to be plagiarized
        if mse < threshold:
            result = "The images are plagarised. The percentage of similarity is "+str(per) +"%"
            return render_template('index.html',result= result)
        else:
            result = "The percentage of similarity is "+str(per) +"%"
            return render_template('index.html',result = result)
            
    
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/hello')
# def hewllo():
#     data={"name":"kiran"}
#     return data,222
#
#C:\Users\Admin\Desktop\desktop\Similarity\static\kk.txt


@app.route('/text',methods=["POST","GET"])
def text():
    result=""
    if request.method=="POST":
        def tokenize(text):
            words = text.lower().split()
            word_count = {}
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            return word_count

    # Define a function to calculate the dot product of two vectors
        def dot_product(vector1, vector2):
            dot_product = 0
            for key in vector1:
                if key in vector2:
                    dot_product += vector1[key] * vector2[key]
            return dot_product

        # Define a function to calculate the cosine similarity of two texts
        def cosine_similarity(text1, text2):
            vector1 = tokenize(text1)
            vector2 = tokenize(text2)
            dot = dot_product(vector1, vector2)
            magnitude1 = math.sqrt(dot_product(vector1, vector1))
            magnitude2 = math.sqrt(dot_product(vector2, vector2))
            if magnitude1 == 0 or magnitude2 == 0:
                return 0
            else:
                return dot / (magnitude1 * magnitude2)

        # Define a function to compare two texts and output the percentage of plagiarism
        def compare_texts(text1, text2):
            similarity = cosine_similarity(text1, text2)
            return similarity * 100

        textfile1 = request.files['text1']
        path1 = os.path.join(app.config['UPLOAD_FOLDER'], textfile1.filename)
        textfile1.save(path1)
        
        textfile2 = request.files['text2']
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], textfile2.filename)
        textfile2.save(path2)
        
        # Define two texts to compare
        with open(path1, 'r') as file1:
            text1 = file1.read()
        with open(path2, 'r') as file2:
            text2 = file2.read()

        # Compare the two texts and output the percentage of plagiarism
        plagiarism_percentage = compare_texts(text1, text2)
        result = (f"The percentage of similarity between text file 1 and text flie 2 is: {plagiarism_percentage:.2f}%\n")
        return render_template('text.html',result = result)
    
    
    #THE BELOW CODE IS TO PRINT THE SIMILAR LINE..AND I THINK WHICH NOT NEEDED
    #THE PERCENTAGE IS FINE I GUESS
    
    
        # def read_until_fullstop(file_obj):
        #     #Reads a line from the file until it encounters a full stop.
        #     line = ""
        #     while True:
        #         char = file_obj.read(1)
        #         if not char:
        #             return line
        #         line += char
        #         if char == ".":  # check for period
        #             next_char = file_obj.read(1)
        #             if next_char == " ":  # check for space after period
        #                 return line
        #     return line


        # # Open files in read mode
        # with open(path1, 'r') as file1, open(path2, 'r') as file2:

        #     # Read the lines from the files
        #     file1_lines = []
        #     file2_lines = []

        #     while True:
        #         line = read_until_fullstop(file1)
        #         if not line:
        #             break
        #         file1_lines.append(line.strip())

        #     while True:
        #         line = read_until_fullstop(file2)
        #         if not line:
        #             break
        #         file2_lines.append(line.strip())

        #     # Find similar lines
        #     similar_lines = set(file1_lines).intersection(file2_lines)
        # with open(path1, 'r') as file1, open(path2, 'r') as file2:
        #     # Print the output
        #     print(f"file1\n")
        #     content = file1.read()
        #     print(content + "\n")
        #     print(f"file2\n")
        #     content = file2.read()
        #     print(content + "\n")
        #     if similar_lines:
        #         result = (f"{len(similar_lines)} similar lines found:\n")
        #         for line in similar_lines:
        #             result += line +"\n"
        #         return render_template('text.html',result = result)
        #     else:
        #         result = ("No similar lines found.")
        #         return render_template('text.html',result = result)
            
    return render_template('text.html')
@app.errorhandler(Exception)
def permission_denied(e):
    return redirect('/')
    
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
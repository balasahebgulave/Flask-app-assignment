import pandas as pd 
import urllib.request
from flask import Flask, render_template , jsonify , request, session
from flask import send_from_directory
import json
import os 

data = pd.read_csv('input_data.csv')

BASE_DIR = os.getcwd()
images = os.listdir('downloads/')
local_path = ['/static/downloads/'+i for i in images]
static_folder = BASE_DIR+'/static'
data['local_path'] = local_path
data.to_csv('output_data.csv')
data = pd.read_csv('output_data.csv')




def get_images():
	
	image_urls = data['image_url']
	for index, img_url in enumerate(image_urls):
		emp_name = f"emp{index}"
		try:
			urllib.request.urlretrieve(img_url, f"downloads/{emp_name}.jpg")
		except:
			print('Not Found')





app = Flask(__name__,static_url_path='/static', 
            static_folder=static_folder)

app.config['static_folder'] = static_folder


@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['static_folder'],
                               filename)




@app.route('/view/csvdata', methods = ['GET','POST'])
def confugure():
	jsondata = data.to_dict(orient='records')
	return jsonify(jsondata)



@app.route('/', methods = ['GET','POST'])
def showtable():
	return render_template('filetable.html')

@app.route('/filter', methods = ['GET','POST'])
def filter():
	type_code = list(data['type_code'])
	filterdata = {}
	if request.method == 'POST':
		response = request.form.get('filter')
		for i,j in enumerate(data.type_code):
			if int(response) == int(j):
				result = data.loc[i]
				result = []

				emp_name = data.emp_name.iloc[i]
				code = data.type_code.iloc[i]
				image_url = data.image_url.iloc[i]
				local_path = data.local_path.iloc[i]
				
				result.append(emp_name)
				result.append(code)
				result.append(image_url)
				result.append(local_path)
				image = local_path

				result = {'filterdata':result, 'type_code':type_code, 'image':image}
				return render_template('filter.html', result = result)
	result = {'filterdata':filterdata, 'type_code':type_code}
	return render_template('filter.html', result = result)

if __name__ == '__main__':
	app.run(host = 'localhost', debug = True, port = 8008)
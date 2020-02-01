from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from dbhelper import DBHelper
from traverse import Traverse
import pandas as pd  

global_session = {}

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
            
app.secret_key = "abcdhkjhfdh" 

helper = DBHelper()
help_scan = Traverse()

@app.route('/')
def index():
  if not isLogin():
    return redirect('/login')
  else:
    email = session['email']
    return render_template('logout.html', data=email)
  # if 'email' in session:
  #   email = session['email']
  #   return 'Logged in as ' + email + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
  # return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/login', methods=['GET','POST'])
def login():
  res = {
      'init' : True,
      'status': False,
      'data':[],
      'msg':'',
      'title': 'Login'
  }
  if request.method == 'POST':
      user = {
          'email': request.form['email'],
          'password': request.form['pass']
      }
      print(user['email'])
      session['email'] = user['email']
      res = helper.userExists(user, True)
      if res['status']:
          userId = res['data']['userId']
          
          return redirect ('/classes')
      else:
          res['title'] = 'Login'
          res['init'] = False
          return render_template('login.html', data=res)
  else: 
      return render_template('login.html', data=res)

@app.route('/classes', methods=['GET'])
def classes():
  if not isLogin():
    return redirect('/login')
  init_res = {
        'status': False,
        'data' : (),
        'title': 'Classes'
    }
  res = helper.getClassData()
  print(res)
  if res['status']:
    res['title'] = 'Classes'
    return render_template('class.html',data=res)
  else:
    return render_template('class.html',data=init_res)   

@app.route('/register', methods=['GET','POST'])
def register():
    res = {
        'init' : True,
        'status': False,
        'data':[],
        'msg':'',
        'title': 'Register'
    }
    if request.method == 'POST':
        user = {
            'email': request.form['email'],
            'password': request.form['pass']
        }
        res = helper.registerUser(user)
        res['title'] = 'Register'
        res['init'] = False
        if res['status'] :
            return redirect('login')
        else:
            return render_template('register.html', data=res)
    else:
        return render_template('register.html', data=res)   

@app.route('/class/<cid>', methods=['GET'])
def person(cid):
  if not isLogin():
    return redirect('/login')
  currentEmail = getMailIdFromSession()

  init_res = {
        'status': False,
        'data' : (),
        'title': 'Persons'  
    }
  res = helper.getPersonData(cid)
  print(res)
  if res['status']:
    res['title'] = 'Persons'
    res['currentEmail'] = currentEmail
    return render_template('person.html',data=res)
  else:
    return render_template('person.html',data=init_res)
  
@app.route('/person/<cid>/<pid>', methods=['GET'])
def person_image(cid,pid):
  global global_session
  if not isLogin():
    return redirect('/login')
  helper.upsertGlobalSessionData(getMailIdFromSession(),int(pid))
  init_res = {
        'status': False,
        'data' : (),
        'title': 'Person Images'  
    }
  res_enroll = helper.getClassEnrollImageData(cid,pid)
  res_predict = helper.getClassPredictImageData(cid,pid)
  print(res_enroll)
  print(res_predict)
  res = {}
  if res_enroll['status']:
    res['status'] = True
    res['data'] = {}
    res['data']['enroll'] = res_enroll['data']
    res['data']['predict'] = res_predict ['data']
    res['data']['pid'] = pid
    res['data']['cid'] = cid
  else:
    res['status'] = False
    init_res['status'] = False
    init_res['data'] = {}
    init_res['data']['enroll'] = ()
    init_res['data']['predict'] = ()
    init_res['data']['cid'] = ''
    init_res['data']['pid'] = ''

  print(res)
  if res['status']:
    res['title'] = 'Person Images'
    return render_template('person_image.html',data=res)
  else:
    return render_template('person_image.html',data=init_res)

@app.route('/api/person/<cid>/<pid>', methods=['GET'])
def person_image_data(cid,pid):
  global global_session
  error_res = {
        'status': False,
        'data' : (),
        'msg': 'Not Authorize, Please Login'  
    }
  if not isLogin():
    return jsonify(error_res)
  res_predict = helper.getClassPredictImageData(cid,pid)
  print("HERE .......................")
  print(res_predict)
  return jsonify(res_predict)

# @app.route('/mapper', methods=['POST'])
# def Mappeerdata():
@app.route('/mapper', methods=['POST'])
def postMapper():
  if request.method == 'POST':
    mapper = {
      'cid' : request.form['cid'],
      'pid' : request.form['pid'],
      'prediction_img_path' : request.form['prediction_img_path'],
      'enroll_img_path' : request.form['enroll_img_path'],
      'isSkipped':request.form['isSkipped'],
      'isNotEnrolled':request.form['isNotEnrolled']
      }
    res = helper.upsertMapperData(mapper)
    return jsonify(res)

@app.route('/api/mapper', methods=['GET'])
def Mapper():
  if not isLogin():
    return redirect('/login')
  init_res = {
        'status': False,
        'data' : (),
        'title': 'Mapper Data'
    }
  res = helper.getAllMapperData()
  classes = []
  persons = []
  prediction_img_path = []
  enroll_img_path = []
  isSkipped = []
  isNotEnrolled = []
  print(res)
  print(len(res['data']))
  for row in res['data']:
    print(row)
    classes.append(row[0])    
    persons.append(row[1])
    prediction_img_path.append(row[2])
    enroll_img_path.append(row[3])
    isSkipped.append(row[4])
    isNotEnrolled.append(row[5])       
  dict ={
    "class_name": classes,
    "person_name": persons,
    "prediction_img_path": prediction_img_path,
    "enroll_img_path": enroll_img_path,
    "isSkipped": isSkipped,
    "isNotEnrolled": isNotEnrolled   
  }

  df = pd.DataFrame(dict)
  df.to_csv('DataExport.csv')
  return jsonify(res)

@app.route('/nmap', methods=['GET'])
def nmatch():
  if not isLogin():
    return redirect('/login')
  init_res = {
        'status': False,
        'data' : (),
        'title': 'Nmatch'
    }
  res = helper.getAllNmatchData()
  print(res)
  if res['status']:
    res['title'] = 'Nmatch'
    return jsonify(res)
 
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('email', None)
   return redirect(url_for('index'))

def isLogin():
  if 'email' in session:
    if session['email']:
      return True
    else:
      return False
  else:
      return False

def getMailIdFromSession():
  if isLogin():
    return session['email']
  else: 
    return ''

def folder_scan():
  pass
  #help_scan.data_struct()
  #help_scan.scan_json()

if __name__ == "__main__":
  folder_scan()
  app.run(debug=True)
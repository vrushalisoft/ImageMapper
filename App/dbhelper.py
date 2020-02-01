import sqlite3

class DBHelper:

  def connect(self):
    
    self.conn = sqlite3.connect('./data/mydb.db')#, check_same_thread= False
    self.cursor = self.conn.cursor()
    return self.conn
    print("Opened database successfully")
  
  def getcursor(self):
    return self.cursor

  def close(self):
    self.conn.close()
    print('Connection closed')

  def getClassData(self):
    querry = "SELECT * FROM class";
    self.connect()
    classes = self.cursor.execute(querry)
    class_list = list(classes)
    if len(class_list) <= 0 :
      class_data = {
        'status':False,
        'data':[],
        'msg': 'class Data Doesnot Exists'
      }
    else:
      class_data = {
        'status':True,
        'data':class_list,
        'msg': 'Class Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return class_data

  def getPersonData(self, cid):
    querry = 'SELECT person.*,global_session.email FROM person LEFT JOIN global_session ON  global_session.pid = person.pid where cid={0}'.format(cid)
    self.connect()
    persons = self.cursor.execute(querry)
    person_list = list(persons)
    if len(person_list) <= 0 :
      person_data = {
        'status':False,
        'data':[],
        'msg': 'Person Data Doesnot Exists'
      }
    else:
      person_data = {
        'status':True,
        'data':person_list,
        'msg': 'Person Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return person_data

  def getClassEnrollImageData(self, cid, pid):
    querry = "SELECT * FROM person_image where is_Enroll='True' AND cid={0} AND pid={1}".format(cid,pid);
    self.connect()
    enroll_images = self.cursor.execute(querry)
    enroll_image_list = list(enroll_images)
    if len(enroll_image_list) <= 0 :
      enroll_image_data = {
        'status':False,
        'data':[],
        'msg': 'enroll_image Data Doesnot Exists'
      }
    else:
      enroll_image_data = {
        'status':True,
        'data':enroll_image_list,
        'msg': 'Enroll Image Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return enroll_image_data

  def getClassPredictImageData(self, cid, pid):
    querry = "SELECT * FROM person_image where is_Enroll='False' AND cid={0} AND pid={1}".format(cid,pid);
    self.connect()
    predict_images = self.cursor.execute(querry)
    predict_image_list = list(predict_images)
    if len(predict_image_list) <= 0 :
      predict_image_data = {
        'status':False,
        'data':[],
        'msg': 'Predict Image Data Doesnot Exists'
      }
    else:
      predict_image_data = {
        'status':True,
        'data':predict_image_list,
        'msg': 'Predict Image Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return predict_image_data

  def userExists(self, user, isLogin):
    user_exists = True
    if isLogin:
      querry = "SELECT userId FROM user where email='"+user['email']+"' AND pass='"+user['password']+"'"
    else:
      querry = "SELECT userId FROM user where email='"+user['email']+"'"
    self.connect()
    users = self.cursor.execute(querry)
    user_list = list(users)
    if len(user_list) <= 0 :
      user_exists = {
        'status':False,
        'data':[],
        'msg': 'User Doesnot Exists'
      }
    else:
      user_exists = {
        'status':True,
        'data':{'userId':user_list[0][0]},
        'msg': 'User Exists'
      }
    self.conn.commit()
    self.conn.close()
    return user_exists

  def registerUser(self, user):
    res = self.userExists(user, False)
    if not res['status']:
      querry = "INSERT INTO user (email, pass) VALUES ('"+user['email']+"','"+user['password']+"')"
      self.connect()
      self.cursor.execute(querry)
      self.conn.commit()
      self.conn.close()
      return {
        'status': True,
        'msg': 'User Registerd',
        'data': []
      }
    else:
      return {
        'status': False,
        'msg': 'User Exists',
        'data': []
      }

  def getMapperData(self, cid, pid, prediction_img_path, enroll_img_path):
      querry = "SELECT * FROM mapper where cid={0} AND pid={1} AND prediction_img_path=\'{2}\'".format(cid,pid,prediction_img_path)
      self.connect()
      mappers = self.cursor.execute(querry)
      mapper_list = list(mappers)
      if len(mapper_list) <= 0 :
       mapper_data = {
          'status':False,
          'data':[],
          'msg': 'Person Image Data Doesnot Exists'
        }
      else:
       mapper_data = {
          'status':True,
          'data':mapper_list[0],
          'msg': 'Person Image Data Exists'
        }
      self.conn.commit()
      self.conn.close()
      return mapper_data

  def upsertMapperData(self, mapper):
    res = self.getMapperData(mapper['cid'],mapper['pid'],mapper['prediction_img_path'],mapper['enroll_img_path'])
    if res['status']:
      print(res['data'])
      querry = "UPDATE mapper SET cid={1},pid={2},prediction_img_path=\'{3}\', enroll_img_path=\'{4}\', isSkipped={5}, isNotEnrolled={6} WHERE mapid={0}".format(res['data'][0],mapper['cid'],mapper['pid'],mapper['prediction_img_path'],mapper['enroll_img_path'],mapper['isSkipped'],mapper['isNotEnrolled'])
    else:
      querry = "INSERT into mapper('cid','pid','prediction_img_path','enroll_img_path',isSkipped,isNotEnrolled) VALUES({0},{1},\'{2}\',\'{3}\',{4},{5})".format(mapper['cid'],mapper['pid'],mapper['prediction_img_path'],mapper['enroll_img_path'],mapper['isSkipped'],mapper['isNotEnrolled'])
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()
    return {
      'status': True,
      'msg': 'Image Mapped Successfully',
      'data': []
    }    

  def insertclassid(self, class_name):
    querry = "insert into class('class_name') VALUES (\'{0}\')".format(
        class_name.lower())
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def insertpersonid(self, class_id, person_name):
    querry = "insert into person('cid','name') VALUES (\'{0}\',\'{1}\')".format(
        class_id, person_name.lower())
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def insertpersonimage(self, class_id, person_id, img_path, is_enroll):
    querry = "insert into person_image('cid','pid','image_path','is_enroll') VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\')".format(
        class_id, person_id, img_path, is_enroll)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()

  def getclassid(self, class_name):
    querry = "select cid from class where class_name=\'{0}\'".format(class_name.lower())
    self.connect()
    classs_id = self.cursor.execute(querry)
    classid = list(classs_id)
    self.conn.commit()
    self.conn.close()
    return classid

  def getpersonid(self, class_id, person_name):
    querry = "select pid from person where name=\'{0}\'and cid=\'{1}\'".format(
        person_name.lower(), class_id)
    self.connect()
    personn_id = self.cursor.execute(querry)
    person_id = list(personn_id)

    self.conn.commit()
    self.conn.close()
    return person_id

  def getpersonimage(self, class_id, person_id, img_path, is_enroll):
    querry = "select * from person_image where cid =\'{0}\'and pid=\'{1}\'and image_path =\'{2}\'and is_enroll =\'{3}\'".format(
        class_id, person_id, img_path, is_enroll)
    self.connect()
    is_imagee_exist = self.cursor.execute(querry)
    is_image_exist = list(is_imagee_exist)
    print(is_image_exist)
    self.conn.commit()
    self.conn.close()
    return is_image_exist  

  def getGlobalSessionData(self, email):
    querry = 'SELECT * FROM global_session where email=\'{0}\''.format(email)
    self.connect()
    global_sessions = self.cursor.execute(querry)
    global_session_list = list(global_sessions)
    if len(global_session_list) <= 0 :
      global_session_data = {
        'status':False,
        'data':[],
        'msg': 'Global Session Data Doesnot Exists'
      }
    else:
      global_session_data = {
        'status':True,
        'data':global_session_list,
        'msg': 'Global Session Data Exists'
      }
    self.conn.commit()
    self.conn.close()
    return global_session_data
  
  def upsertGlobalSessionData(self, email, pid):
    res = self.getGlobalSessionData(email)
    if res['status']:
      print(res['data'])
      querry = "UPDATE global_session SET pid={0} WHERE email=\'{1}\'".format(pid, email)
    else:
      querry = "INSERT into global_session('pid','email') VALUES({0},\'{1}\')".format(pid,email)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()
    return {
      'status': True,
      'msg': 'Session Updated Successfully',
      'data': []
    }  

  def upsertNmatchData(self, image_path, nmatch_path):
    res = self.getNmatchData(image_path,nmatch_path)
    if res['status']:
      print(res['data'])
      querry = "UPDATE nearest_match SET image_path=\'{1}\', nmatch_path=\'{2}\' WHERE nid={0}".format(image_path,nmatch_path)
    else:
      querry = "INSERT into nearest_match('image_path','nmatch_path') VALUES(\'{0}\',\'{1}\')".format(image_path,nmatch_path)
    self.connect()
    self.cursor.execute(querry)
    self.conn.commit()
    self.conn.close()
    return {
      'status': True,
      'msg': 'Image Match Successfully',
      'data': []
    }   

  def getNmatchData(self, image_path, nmatch_path):
        querry = "SELECT * FROM nearest_match where image_path=\'{0}\' AND nmatch_path=\'{1}\'".format(image_path,nmatch_path)
        print(querry)
        self.connect()
        nmatchs = self.cursor.execute(querry)
        nmatch_list = list(nmatchs)
        if len(nmatch_list) <= 0 :
          nmatch_data = {
            'status':False,
            'data':[],
            'msg': 'Nearest matches Data Doesnot Exists'
          }
        else:
          nmatch_data = {
            'status':True,
            'data':nmatch_list,
            'msg': 'Nearest matches Image Data Exists'
          }
        self.conn.commit()
        self.conn.close()
        return nmatch_data

  def getAllNmatchData(self):
        querry = "SELECT * FROM nearest_match "
        self.connect()
        nmatchs = self.cursor.execute(querry)
        nmatch_list = list(nmatchs)
        if len(nmatch_list) <= 0 :
          nmatch_data = {
            'status':False,
            'data':[],
            'msg': 'Nearest matches Data Doesnot Exists'
          }
        else:
          nmatch_data = {
            'status':True,
            'data':nmatch_list,
            'msg': 'Nearest matches Image Data Exists'
          }
        self.conn.commit()
        self.conn.close()
        return nmatch_data

  def getAllMapperData(self):
      querry = """SELECT 
      class.class_name as class_name,
      person.name as person_name,
      mapper.prediction_img_path,
      mapper.enroll_img_path,
      mapper.isNotEnrolled,
      mapper.isSkipped
      FROM class
      INNER JOIN person ON class.cid = person.cid
      INNER JOIN mapper ON person.pid = mapper.pid"""
      self.connect()
      mappers = self.cursor.execute(querry)
      mapper_list = list(mappers)
      if len(mapper_list) <= 0 :
        mapper_data = {
          'status':False,
          'data':[],
          'msg': 'Mapper Data Doesnot Exists'
        }
      else:
        mapper_data = {
          'status':True,
          'data':mapper_list,
          'msg': 'Mapper Data Exists'
        }
      self.conn.commit()
      self.conn.close()
      return mapper_data
      
        
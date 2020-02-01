import os
import json
from dbhelper import DBHelper

class Traverse:
    def init(self):
        self.prediction_folder_path = '/dist/image/classes/{0}/pred_crops/{1}/{2}'
        self.enroll_folder_path = '/dist/image/classes/{0}/enroll_crops/{1}/{2}'
        
        self.prediction_data_path = os.path.join(os.path.dirname(__file__), "web","static","dist","image","recognitions.json")
       

    def data_struct(self):

        helper = DBHelper()

        path = os.path.join(os.getcwd(), "web", "static", "dist", "image", "classes")
        print(path)

        l1_list = os.listdir(path)
        print("Files and directories in"+path+":")
        print(l1_list)
        for c1 in l1_list:
            class_id = helper.getclassid(c1)
            if len(class_id) <= 0:
                helper.insertclassid(c1)
                class_id = helper.getclassid(c1)

            path2 = os.path.join(path, c1)
            l2_list = os.listdir(path2)

            # print(l2_list)
            for c2 in l2_list:
                path3 = os.path.join(path2, c2)
                l3_list = os.listdir(path3)

                for person_name in l3_list:
                    person_id = helper.getpersonid(class_id[0][0], person_name)
                    if len(person_id) <= 0:
                        helper.insertpersonid(class_id[0][0], person_name)
                        person_id = helper.getpersonid(class_id[0][0], person_name)
                    print(person_id)

                    path4 = os.path.join(path3, person_name)
                    l4_list = os.listdir(path4)
                    for person_image in l4_list:
                        img_path = os.path.join(path4, person_image)
                        
                        parts = img_path.split('\\')
                        v_path = "/"+parts[6]+'/'+parts[7]+'/'+parts[8]+'/'+parts[9]+'/'+parts[10]+'/'+parts[11]+'/'+parts[12]
                        print(v_path, c2)
                        if c2 == "enroll_crops":
                            is_enroll = True
                            images = helper.getpersonimage(class_id[0][0], person_id[0][0], v_path, is_enroll)
                        else:
                            is_enroll = False
                            images = helper.getpersonimage(class_id[0][0], person_id[0][0], v_path, is_enroll)
                        if len(images) <= 0:
                            helper.insertpersonimage(class_id[0][0], person_id[0][0], v_path, is_enroll)
                            images = helper.getpersonimage(class_id[0][0], person_id[0][0], v_path, is_enroll)

    def scan_json(self):
        self.init()
        helper = DBHelper()
        with open(self.prediction_data_path) as jsonData:
            self.prediction_data = json.load(jsonData)
            self.prediction_data = self.prediction_data['recognitions']
            jsonData.close()
        prediction_data = []
        for predict_path in self.prediction_data:
            
            # prediction = {}
            # prediction['image_path'] = self.correct_image_path(predict_path['image_path'])
            # prediction['recognised_images'] = []
            parts = predict_path['image_path'].split('/')
            class_id = parts[2]
            person_id = parts[4]
            predict_img_path = self.correct_image_path(class_id,person_id,predict_path['image_path'])
            print(predict_path)
            temp = predict_path['recognised_ids']
            
            for dir_name in predict_path['recognised_ids']:
                print(dir_name)
                enroll_data_path = os.path.join(os.path.dirname(__file__), "web","static","dist","image","classes",str(class_id),"enroll_crops",str(dir_name))
                image_path = self.enroll_folder_path.format(str(class_id),str(dir_name),sorted(os.listdir(enroll_data_path))[0])
                print(image_path)
                matches = helper.getNmatchData(predict_img_path, image_path)
                print(matches)
                if len(matches['data']) <= 0:
                    helper.upsertNmatchData(predict_img_path, image_path)
            
            break;
                #prediction['recognised_images'].append(image_path)
            #prediction_data.append(prediction)
        #return prediction_data

    def correct_image_path(self, cid, pid, image_path):
        parts = image_path.split('/')
        file_name = parts[len(parts)-1]
        corrected_path = self.prediction_folder_path.format(cid,pid,file_name)
        return corrected_path

                

import os
from dbhelper import DBHelper


class Traverse:
    def data_struct(self):

        helper = DBHelper()

        path = os.path.join(os.getcwd(),"web", "static", "dist", "image", "classes")
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
                        person_id = helper.getpersonid(
                            class_id[0][0], person_name)
                    print(person_id)
                    path4 = os.path.join(path3, person_name)
                    l4_list = os.listdir(path4)
                    for person_image in l4_list:
                        img_path = os.path.join(path4, person_image)
                        print(img_path, c2)
                        if c2 == "enroll":
                            is_enroll = True
                            images = helper.getpersonimage(
                                class_id[0][0], person_id[0][0], img_path, is_enroll)
                        else:
                            is_enroll = False
                            images = helper.getpersonimage(
                                class_id[0][0], person_id[0][0], img_path, is_enroll)
                        if len(images) <= 0:
                            helper.insertpersonimage(
                                class_id[0][0], person_id[0][0], img_path, is_enroll)
                            images = helper.getpersonimage(
                                class_id[0][0], person_id[0][0], img_path, is_enroll)

                    # print(l4_list)

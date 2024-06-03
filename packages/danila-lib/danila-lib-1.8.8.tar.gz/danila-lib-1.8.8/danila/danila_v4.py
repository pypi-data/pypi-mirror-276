import hashlib
import os
from datetime import datetime

import cv2

from data.neuro.Letters_recognize import Letters_recognize
from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.Rama_prod_classify_class import Rama_prod_classify_class
from data.neuro.Text_detect_class import Text_detect_class
from data.neuro.Vagon_number_detect_class import Vagon_number_detect_class
from data.neuro.Vagon_number_recognize_class import Vagon_number_recognize_class
from data.neuro.models import *
from data.result.Class_im import Class_im
from data.result.Class_text import Class_text
from data.result.Rama_prod import Rama_Prod
from data.result.Rect import Rect

"""main module for user"""
from data.neuro.Rama_classify_class import Rama_classify_class
from data.neuro.text_recognize_yolo import Text_Recognize_yolo

class Text_recognize_result:
    def __init__(self, detail, number = None, prod = None, year = None):
        self.detail = detail
        self.number = number
        self.prod = prod
        self.year = year

class Text_cut_recognize_result:
    def __init__(self, text, conf):
        self.text = text
        self.conf = conf

class Danila_v4:
    """main class for user"""
    def __init__(self, yolov5_dir):

        yolo_path = yolov5_dir
        rama_prod_classify_model_path = RAMA_PROD_CLASSIFY_MODEL_ADDRESS
        print('reading and loading - RAMA_PROD_CLASSIFY_MODEL')
        self.rama_prod_classify_model = Rama_prod_classify_class(rama_prod_classify_model_path, yolo_path)
        rama_no_spring_detect_model_path = RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS
        print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
        self.rama_no_spring_detect_model = Rama_detect_class(rama_no_spring_detect_model_path,
                                                             'rama_no_spring_detect', yolo_path)
        rama_spring_detect_model_path = RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS
        print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
        self.rama_spring_detect_model = Rama_detect_class(rama_spring_detect_model_path, 'rama_spring_detect',
                                                             yolo_path)
        rama_spring_ruzhimmash_text_detect_model_path = RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS
        print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
        self.rama_spring_ruzhimmash_text_detect_model = Text_detect_class(rama_spring_ruzhimmash_text_detect_model_path,
                                                                          'rama_text_ruzhimmash_detect', yolo_path)
        rama_no_spring_bejickaya_text_detect_model_path = RAMA_BEJICKAYA_TEXT_DETECT_MODEL_ADDRESS
        print('reading and loading - RAMA_BEJICKAYA_TEXT_DETECT_MODEL')
        self.rama_no_spring_bejickaya_text_detect_model = Text_detect_class(rama_no_spring_bejickaya_text_detect_model_path,
                                                                            'rama_text_begickaya_detect', yolo_path)
        text_recognize_yolo_ruzhimmash_model_path = TEXT_RECOGNIZE_RUZHIMMASH_MODEL_ADDRESS
        print('reading and loading - TEXT_RECOGNIZE_RUZHIMMASH_MODEL')
        self.text_recognize_ruzhimmash_model = Text_Recognize_yolo(text_recognize_yolo_ruzhimmash_model_path, yolo_path)
        text_recognize_yolo_begickaya_model_path = TEXT_RECOGNIZE_BEGICKAYA_MODEL_ADDRESS
        print('reading and loading - TEXT_RECOGNIZE_BEGICKAYA_MODEL')
        self.text_recognize_begickaya_model = Text_Recognize_yolo(text_recognize_yolo_begickaya_model_path, yolo_path)
        vagon_number_detect_model_path = VAGON_NUMBER_DETECT_MODEL_ADDRESS
        print('reading and loading - VAGON_NUMBER_DETECT_MODEL')
        self.vagon_number_detect_model = Vagon_number_detect_class(vagon_number_detect_model_path, yolo_path)
        print('loading - VAGON_NUMBER_RECOGNIZE_MODEL')
        self.vagon_number_recognize_model = Vagon_number_recognize_class()

    # returns Rama_Prod_Conf - class of rama and confidence using CNN network
    # img - openCV frame
    def rama_classify(self, img, size = 256):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        # img = cv2.imread(img_path)
        rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
        detail_prod = Text_cut_recognize_result(rama_prod_conf.rama_prod.name, rama_prod_conf.conf)
        detail = Text_recognize_result(detail_prod)
        if (detail.detail.text == 'no_rama'):
            sizes = [256,384,512,640]
            flag = True
            for s in sizes:
                if flag:
                    rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
                    detail_prod1 = Text_cut_recognize_result(rama_prod_conf1.rama_prod.name, rama_prod_conf1.conf)
                    detail1 = Text_recognize_result(detail_prod1)
                    if (detail1.detail.text != 'no_rama'):
                        detail = detail1
                        flag = False
        return detail

    # returns openCV frame with rama from openCV frame\
    # def rama_detect(self, img, size = 256):
    #     """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
    #     hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
    #     hash_str = hash_object.hexdigest()
    #     initial_image_path = 'initial_image' + hash_str + '.jpg'
    #     cv2.imwrite(initial_image_path, img)
    #     rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
    #     rama_prod = rama_prod_conf.rama_prod
    #     if rama_prod == Rama_Prod.no_rama:
    #         sizes = [256, 384, 512, 640]
    #         flag = True
    #         for s in sizes:
    #             if flag:
    #                 rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
    #                 rama_prod1 = rama_prod_conf1.rama_prod
    #                 if (rama_prod1 != Rama_Prod.no_rama):
    #                     rama_prod_conf = rama_prod_conf1
    #                     rama_prod = rama_prod_conf.rama_prod
    #                     flag = False
    #         if flag:
    #             os.remove(initial_image_path)
    #             return img
    #     rect = Rect()
    #     if (rama_prod == Rama_Prod.ruzhimmash):
    #         rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
    #     else:
    #         rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
    #     new_img = img.copy()
    #     os.remove(initial_image_path)
    #     if rect is None:
    #         os.remove(initial_image_path)
    #         return img
    #     cv2.rectangle(new_img, (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), (0, 0, 255), 2)
    #     cv2.putText(new_img, rama_prod.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    #     return new_img

    # returns openCV image with cut_rama
    # def rama_cut(self, img, size = 256):
    #     """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
    #     hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
    #     hash_str = hash_object.hexdigest()
    #     initial_image_path = 'initial_image' + hash_str + '.jpg'
    #     cv2.imwrite(initial_image_path, img)
    #     rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
    #     rama_prod = rama_prod_conf.rama_prod
    #     if rama_prod == Rama_Prod.no_rama:
    #         sizes = [256, 384, 512, 640]
    #         flag = True
    #         for s in sizes:
    #             if flag:
    #                 rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
    #                 rama_prod1 = rama_prod_conf1.rama_prod
    #                 if (rama_prod1 != Rama_Prod.no_rama):
    #                     rama_prod_conf = rama_prod_conf1
    #                     rama_prod = rama_prod_conf.rama_prod
    #                     flag = False
    #         if flag:
    #             os.remove(initial_image_path)
    #             return img
    #     rect = Rect()
    #     if (rama_prod == Rama_Prod.ruzhimmash):
    #         rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
    #     else:
    #         rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
    #     if rect is None:
    #         os.remove(initial_image_path)
    #         return img
    #     img_res = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
    #     os.remove(initial_image_path)
    #     return img_res
    # #
    # returns openCV cut rama with drawn text areas
    def rama_text_detect_cut(self, img, size = 256):
        """returns openCV cut rama with drawn text areas"""
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
        rama_prod = rama_prod_conf.rama_prod
        if rama_prod == Rama_Prod.no_rama:
            sizes = [256, 384, 512, 640]
            flag = True
            for s in sizes:
                if flag:
                    rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
                    rama_prod1 = rama_prod_conf1.rama_prod
                    if (rama_prod1 != Rama_Prod.no_rama):
                        rama_prod_conf = rama_prod_conf1
                        rama_prod = rama_prod_conf.rama_prod
                        flag = False
            if flag:
                os.remove(initial_image_path)
                return img
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                os.remove(initial_image_path)
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_img' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                os.remove(initial_image_path)
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_img' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas

    # returns openCV img with drawn text areas
    # def text_detect(self, img, size = 256):
    #     """returns openCV img with drawn text areas"""
    #     hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
    #     hash_str = hash_object.hexdigest()
    #     initial_image_path = 'initial_image' + hash_str + '.jpg'
    #     cv2.imwrite(initial_image_path, img)
    #     rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
    #     rama_prod = rama_prod_conf.rama_prod
    #     if rama_prod == Rama_Prod.no_rama:
    #         sizes = [256, 384, 512, 640]
    #         flag = True
    #         for s in sizes:
    #             if flag:
    #                 rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
    #                 rama_prod1 = rama_prod_conf1.rama_prod
    #                 if (rama_prod1 != Rama_Prod.no_rama):
    #                     rama_prod_conf = rama_prod_conf1
    #                     rama_prod = rama_prod_conf.rama_prod
    #                     flag = False
    #         if flag:
    #             os.remove(initial_image_path)
    #             return img
    #     rect = Rect()
    #     if (rama_prod == Rama_Prod.ruzhimmash):
    #         rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
    #         if rect is None:
    #             os.remove(initial_image_path)
    #             return img
    #         img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
    #         hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
    #         hash_str = hash_object.hexdigest()
    #         img_cut_path = 'cut_img' + hash_str + '.jpg'
    #         cv2.imwrite(img_cut_path, img_cut)
    #         image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
    #         image_text_areas.explore_to_whole_image(rect)
    #         image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
    #         os.remove(initial_image_path)
    #         os.remove(img_cut_path)
    #         return image_drawn_text_areas
    #     else:
    #         rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
    #         if rect is None:
    #             os.remove(initial_image_path)
    #             return img
    #         img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
    #         hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
    #         hash_str = hash_object.hexdigest()
    #         img_cut_path = 'cut_img' + hash_str + '.jpg'
    #         cv2.imwrite(img_cut_path, img_cut)
    #         image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
    #         image_text_areas.explore_to_whole_image(rect)
    #         image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
    #         os.remove(initial_image_path)
    #         os.remove(img_cut_path)
    #         return image_drawn_text_areas

    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def rama_text_recognize(self, img, size = 256):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod_conf = self.rama_prod_classify_model.classify(img, size)
        rama_prod = rama_prod_conf.rama_prod
        detail_prod = Text_cut_recognize_result(rama_prod_conf.rama_prod.name, rama_prod_conf.conf)
        detail = Text_recognize_result(detail_prod)
        if rama_prod == Rama_Prod.no_rama:
            sizes = [256, 384, 512, 640]
            flag = True
            for s in sizes:
                if flag:
                    rama_prod_conf1 = self.rama_prod_classify_model.classify(img, s)
                    rama_prod1 = rama_prod_conf1.rama_prod
                    detail_prod1 = Text_cut_recognize_result(rama_prod_conf1.rama_prod.name, rama_prod_conf1.conf)
                    detail1 = Text_recognize_result(detail_prod1)
                    if (rama_prod1 != Rama_Prod.no_rama):
                        rama_prod_conf = rama_prod_conf1
                        rama_prod = rama_prod_conf.rama_prod
                        detail = detail1
                        detail_prod = detail_prod1
                        flag = False
            if flag:
                os.remove(initial_image_path)
                return detail
        rect = Rect()
        detail.prod = Text_cut_recognize_result(rama_prod.name, rama_prod_conf.conf)
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                os.remove(initial_image_path)
                return detail
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_img' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)

            label_area = self.text_recognize_ruzhimmash_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
            res_labels = {}
            (number_text, number_conf) = label_area.labels[Class_text.number]
            if len(number_text) == 5:
                res_labels['number'] = (number_text, number_conf)
            else:
                number_image_text_areas = image_text_areas.areas[Class_text.number]
                image_text_areas_min = []
                image_text_areas_max = []
                for number_image_text_area in number_image_text_areas:
                    w = number_image_text_area.xmax - number_image_text_area.xmin
                    if (number_image_text_area.xmin - (w // 2)) < 0:
                        new_xmin = 0
                    else:
                        new_xmin = number_image_text_area.xmin - (w // 2)
                    rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin,
                                    ymax=number_image_text_area.ymax)
                    image_text_areas_min.append(rect_min)
                    new_xmax = number_image_text_area.xmax + w // 2
                    rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin,
                                    ymax=number_image_text_area.ymax)
                    image_text_areas_max.append(rect_max)
                image_text_areas.areas[Class_text.number] = image_text_areas_min
                label_area_min = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
                (number_text_min, number_conf_min) = label_area_min.labels[Class_text.number]
                if len(number_text_min) == 5:
                    res_labels['number'] = (number_text_min, number_conf_min)
                else:
                    image_text_areas.areas[Class_text.number] = image_text_areas_max
                    label_area_max = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
                    (number_text_max, number_conf_max) = label_area_max.labels[Class_text.number]
                    if len(number_text_max) == 5:
                        res_labels['number'] = (number_text_max, number_conf_max)
                    else:
                        res_labels['number'] = (number_text, number_conf)
            res_labels['prod'] = ('1275', detail.prod.conf)
            (year_text, year_conf) = label_area.labels[Class_text.year]
            if (len(year_text) == 2) and (int(year_text) < 25):
                res_labels['year'] = (year_text, year_conf)
            else:
                res_labels['year'] = ('23', 0.25)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            res_labels_number_text, res_labels_number_conf = res_labels['number']
            detail.number = Text_cut_recognize_result(res_labels_number_text, res_labels_number_conf)
            res_labels_year_text, res_labels_year_conf = res_labels['year']
            detail.year = Text_cut_recognize_result(res_labels_year_text, res_labels_year_conf)
            res_labels_prod_text, res_labels_prod_conf = res_labels['prod']
            detail.prod = Text_cut_recognize_result(res_labels_prod_text, res_labels_prod_conf)
            return detail
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                os.remove(initial_image_path)
                return detail
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_img' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            label_area = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 6, 64, 192,
                                                                  2, 64, 64, 2, 64,64)
            res_labels = {}
            (number_text, number_conf) = label_area.labels[Class_text.number]
            if len(number_text) == 6:
                res_labels['number'] = (number_text, number_conf)
            else:
                number_image_text_areas = image_text_areas.areas[Class_text.number]
                image_text_areas_min = []
                image_text_areas_max = []
                for number_image_text_area in number_image_text_areas:
                    w = number_image_text_area.xmax - number_image_text_area.xmin
                    if (number_image_text_area.xmin - (w//2)) < 0:
                        new_xmin = 0
                    else:
                        new_xmin = number_image_text_area.xmin - (w//2)
                    rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_min.append(rect_min)
                    new_xmax = number_image_text_area.xmax + w//2
                    rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_max.append(rect_max)
                image_text_areas.areas[Class_text.number] = image_text_areas_min
                label_area_min = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 6, 64, 192,
                                                                  2, 64, 64, 2, 64,64)
                (number_text_min, number_conf_min) = label_area_min.labels[Class_text.number]
                if len(number_text_min) == 6:
                    res_labels['number'] = (number_text_min, number_conf_min)
                else:
                    image_text_areas.areas[Class_text.number] = image_text_areas_max
                    label_area_max = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 6, 64, 192,
                                                                  2, 64, 64, 2, 64,64)
                    (number_text_max, number_conf_max) = label_area_max.labels[Class_text.number]
                    if len(number_text_max) == 6:
                        res_labels['number'] = (number_text_max, number_conf_max)
                    else:
                        res_labels['number'] = (number_text, number_conf)
            res_labels['prod'] = ('12', detail.prod.conf)
            (year_text, year_conf) = label_area.labels[Class_text.year]
            if (len(year_text) == 2) and (int(year_text) < 25):
                res_labels['year'] = (year_text, year_conf)
            else:
                res_labels['year'] = ('23', 0.25)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            res_labels_number_text, res_labels_number_conf = res_labels['number']
            detail.number = Text_cut_recognize_result(res_labels_number_text, res_labels_number_conf)
            res_labels_year_text, res_labels_year_conf = res_labels['year']
            detail.year = Text_cut_recognize_result(res_labels_year_text, res_labels_year_conf)
            res_labels_prod_text, res_labels_prod_conf = res_labels['prod']
            detail.prod = Text_cut_recognize_result(res_labels_prod_text, res_labels_prod_conf)
            return detail


    def vagon_number_detect(self, img, size = 256):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        number_rects = self.vagon_number_detect_model.vagon_rama_detect(initial_image_path, size)
        if len(number_rects) == 0:
            os.remove(initial_image_path)
            return img
        img_with_number = img.copy()
        for number_rect in number_rects:
            cv2.rectangle(img_with_number, (number_rect.xmin, number_rect.ymin), (number_rect.xmax, number_rect.ymax), (0, 0, 255), 2)
            cv2.putText(img_with_number, 'number', (number_rect.xmin, number_rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return img_with_number

    def vagon_number_recognize(self, img, size = 256):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        vagon_number_rects = self.vagon_number_detect_model.vagon_rama_detect(initial_image_path, size)
        detail = Text_recognize_result(Text_cut_recognize_result('vagon',0.0))
        if len(vagon_number_rects)==0:
            detail.detail.text = 'no-vagon'
            os.remove(initial_image_path)
            return detail
        detail.number.text, detail.number.conf = self.vagon_number_recognize_model.work_image(img,vagon_number_rects)
        return detail
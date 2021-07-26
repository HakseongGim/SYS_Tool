import os
import cv2

path = 'C:/Users/HakSeong Gim/.spyder-py3/이미지 매칭'
os.chdir(path)
files = os.listdir(path)

img_files = list(filter(lambda x: x.find('.jpg') != -1 or x.find('png') != -1 or x.find('JPG') != -1 , files))
img_files_src = []

for file in img_files :
    if 'Template' in file :
        Template  = file
    else:
        img_files_src.append(file)        
           

def matcing_moment_in_image (Template, img_files_src) :    

    obj = cv2.imread(Template, cv2.IMREAD_GRAYSCALE)    
    src = cv2.imread(img_files_src, cv2.IMREAD_GRAYSCALE)
    result = cv2.imread(img_files_src)

 #-------------------------객체의-외곽 검출-------------------------------------
    _, obj_bin = cv2.threshold(obj, 128, 255, cv2.THRESH_BINARY_INV)
# 임계처리 함수 retval, dst 형태로 출력하나 retval은 제외 (_,)
    
    obj_contours, _ = cv2.findContours(obj_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    obj_pts = obj_contours[0]
    

#------------------------입력 영상 분석----------------------------------------
    _, src_bin = cv2.threshold(src, 128,255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
#-----------------------------------------------------------------------------
    for pts in contours:
        if cv2.contourArea(pts) < 1000:
            continue
         
        rc = cv2.boundingRect(pts)
        cv2.rectangle(dst, rc, (255, 0, 0), 1)
        
        # 모양 비교
        dist = cv2.matchShapes(obj_pts, pts, cv2.CONTOURS_MATCH_I3, 0)
        
        if dist < 0.1:        
            cv2.rectangle(dst, rc, (0,0,255),2)
            area = rc 
       
            return result[area[1]:area[1]+area[3], area[0]:area[0]+area[2]] 
            
img_H = 520
img_V = 280

for i in range(len(img_files_src)) :
    cropped_img = matcing_moment_in_image(Template, img_files_src[i])
    im_resize = cv2.resize(cropped_img, dsize=(img_H, img_V), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("Result_" + img_files_src[i] + ".png", im_resize)


cv2.waitKey(0)
cv2.destroyAllWindows()

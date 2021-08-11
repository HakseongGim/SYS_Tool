import os
import cv2
import pathlib
import sys

def load_image(img_path) :
    files = os.listdir(img_path)
    img_files = list(filter(lambda x: x.find('jpg') != -1 or x.find('png') != -1 or x.find('JPG') != -1 , files))
      
    if not img_files :
        print("이미지 파일이 존재하지 않습니다.")
        sys.exit()
        
    for elm in img_files :
        if 'Template' in elm :
            Temp = elm
            img_files.remove(Temp)
        else:
            Temp = None

    if not Temp :
        print("Template 이미지 파일이 존재하지 않습니다.")
        sys.exit()

    if not img_files :
        print("매칭할 이미지 파일이 존재하지 않습니다.")
        sys.exit()
        
            
    return Temp, img_files
       
def matching_moment_in_image (Temp, img_files_src) :    
    
    obj = cv2.imread(Temp, cv2.IMREAD_GRAYSCALE)      
    src = cv2.imread(img_files_src, cv2.IMREAD_GRAYSCALE)
    
    _, obj_bin = cv2.threshold(obj, 127, 255, cv2.THRESH_BINARY_INV)
    # 임계처리 함수 retval, dst 형태로 출력하나 retval은 제외 (_,)
    
    obj_contours, _ = cv2.findContours(obj_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
    obj_pts = obj_contours[0]
        
    _, src_bin = cv2.threshold(src, 128,255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
      
    dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

    area_list = []
    
    for pts in contours:
       
        if cv2.contourArea(pts) < 1000:
            continue
         
        rc = cv2.boundingRect(pts)
        cv2.rectangle(dst, rc, (255, 0, 0), 1)
        
        # 모양 비교
        dist = cv2.matchShapes(obj_pts, pts, cv2.CONTOURS_MATCH_I3, 0)
        cv2.putText(dst, str(round(dist, 4)), (rc[0], rc[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, cv2.LINE_AA)
        
        
        if dist < 0.04:        
            cv2.rectangle(dst, rc, (0,0,255),2)
            area_list.append(rc)
     
    cv2.imwrite(img_files_src + "_matching_result" + ".jpg", dst)
                
    return area_list
 
img_path = pathlib.Path().absolute()
Temp, img_files = load_image(img_path)

for i in range(len(img_files)) :
    crop_area = matching_moment_in_image(Temp, img_files[i])
    
    for j in range(len(crop_area)) :
    
        org_img = cv2.imread(img_files[i])
        obj = cv2.imread(Temp)
        
        V, H, _ = obj.shape
   
        org_crop_img = org_img[crop_area[j][1]:crop_area[j][1]+crop_area[j][3], crop_area[j][0]:crop_area[j][0]+crop_area[j][2]]
        org_crop_img_resize = cv2.resize(org_crop_img, dsize=(H, V), interpolation=cv2.INTER_CUBIC)
        
        re_crop_img = org_crop_img_resize[int(V*0.25):int(V*0.73), int(H*0.34):int(H*0.65)]
        
        V_c, H_c, _ = re_crop_img.shape
        re_crop_img_resize = cv2.resize(re_crop_img, dsize=(int(H_c*3), int(V_c*3)), interpolation=cv2.INTER_CUBIC)
        
        cv2.imwrite(img_files[i] + "_Result_" + str(j+1) + ".jpg", re_crop_img_resize)
         
cv2.waitKey(0)
cv2.destroyAllWindows()
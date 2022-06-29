import cv2
import numpy as np
import pack


def fun():

    ######################################################
    path="m.png"
    w=700
    h=700

    question=5
    choices=5

    ans=[1,2,0,1,4]

    webcamfeed=True
    camerano=0

    ######################################################

    cap=cv2.VideoCapture(camerano)
    cap.set(10,150)

    while True:
        if webcamfeed : success,i=cap.read()
        else: i=cv2.imread(path)

        #preprocessing
        i=cv2.resize(i,(w,h))
        icontours=i.copy()
        ibiggestcontours=i.copy()
        igray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
        iblur=cv2.GaussianBlur(igray,(5,5),1)
        icanny=cv2.Canny(iblur,10,50)

        try:
            #finding all contours
            contours,hierarchy=cv2.findContours(icanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(icontours,contours,-1,(0,255,0),10)

            #finding rectangles
            rectcon=pack.rectContour(contours)
            biggestcontour=pack.getCornerPoints(rectcon[0])
            gradePoints=pack.getCornerPoints(rectcon[1])
            # print(biggestcontour)

            if biggestcontour.size != 0 and gradePoints.size != 0:
                cv2.drawContours(ibiggestcontours,biggestcontour,-1,(0,0,255),20)
                cv2.drawContours(ibiggestcontours,gradePoints,-1,(255,0,0),20)
                
                biggestcontour=pack.reorder(biggestcontour)
                gradePoints=pack.reorder(gradePoints)

                pt1=np.float32(biggestcontour)
                pt2=np.float32([[0,0],[w,0],[0,h],[w,h]])
                matrix=cv2.getPerspectiveTransform(pt1,pt2)
                iwrapcolored=cv2.warpPerspective(i,matrix,(w,h))
                # cv2.imshow("i",iwrapcolored)

                ptg1=np.float32(gradePoints)
                ptg2=np.float32([[0,0],[325,0],[0,150],[325,150]])
                matrixg=cv2.getPerspectiveTransform(ptg1,ptg2)
                igradedisplay=cv2.warpPerspective(i,matrixg,(325,150))
                # cv2.imshow("grade",igradedisplay)

                #apply threshold
                iwrapgray=cv2.cvtColor(iwrapcolored,cv2.COLOR_BGR2GRAY)
                ithresh=cv2.threshold(iwrapgray,150,255,cv2.THRESH_BINARY_INV)[1]

                boxes=pack.splitBoxes(ithresh)
                #cv2.imshow("test",boxes[2])
                #print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))


                #getting non zero pixel values
                mypixelval=np.zeros((question,choices))
                countc=0
                countr=0
                for image in boxes:
                    totalpixels=cv2.countNonZero(image)
                    mypixelval[countr][countc]=totalpixels
                    countc +=1
                    if (countc == choices) : countr +=1;countc =0
                #print(mypixelval)

                #finding index values of the markings:
                myindex=[]
                for x in range (0,question):
                    arr=mypixelval[x]
                    #print("arr : ",arr)
                    myindexval=np.where(arr==np.amax(arr))
                    #print(myindexval[0])
                    myindex.append(myindexval[0][0])
                #print(myindex)

                # grading:
                grading=[]
                for x in range(0,question):
                    if ans[x]==myindex[x]:
                        grading.append(1)
                    else: grading.append(0)
                #print(grading)
                
                #final grade
                #score in percent = (sum of grading/question)*100
                score =(sum(grading)/question)*100
                #print(score)

                # displaying answer in omr:
                iresult=iwrapcolored.copy()
                iresult=pack.showAnswers(iresult,myindex,grading,ans,question,choices)
                # adding the colors in the original paper 
                iraw=np.zeros_like(iwrapcolored)
                iraw=pack.showAnswers(iraw,myindex,grading,ans,question,choices)
                invmatrix=cv2.getPerspectiveTransform(pt2,pt1)
                invwrap=cv2.warpPerspective(iraw,invmatrix,(w,h))

                ifinal=i.copy()
                ifinal=cv2.addWeighted(ifinal,1,invwrap,1,0)

                irawgrade=np.zeros_like(igradedisplay)
                cv2.putText(irawgrade,str(int(score))+"%",(50,100),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,255),3)
                invmatrixg=cv2.getPerspectiveTransform(ptg2,ptg1)
                invgradedisplay=cv2.warpPerspective(irawgrade,invmatrixg,(w,h))
                # cv2.imshow("grade : " ,irawgrade)
                ifinal=cv2.addWeighted(ifinal,1,invgradedisplay,1,0)
                
                
                
                
                
                cv2.imshow(".....SCANNER.....",ifinal)
            iblank=np.zeros_like(i)
            imageArray=([i,igray,iblur,icanny],
                        [icontours,ibiggestcontours,iwrapcolored,ithresh],
                        [iresult,iraw,invwrap,ifinal])
        except:
            iblank=np.zeros_like(i)
            imageArray=([i,igray,iblur,icanny],
                        [iblank,iblank,iblank,iblank],
                        [iblank,iblank,iblank,iblank])               
        imgstacked=pack.stackImages(imageArray,0.3)
        
        # cv2.imshow("cv",imgstacked)
        if cv2.waitKey(1) & 0xFF ==ord('s'):
            cv2.imwrite("final.jpg",ifinal)
            cv2.waitKey(3000)
    


# fun()
            

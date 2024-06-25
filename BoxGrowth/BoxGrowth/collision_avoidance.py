from depthai_sdk import OakCamera
from depthai_sdk.visualize.configs import StereoColor
import math
import depthai as dai
import cv2
import packets
import numpy as np
from munkres import Munkres

# User-defined constants
WARNING = 2000 # 5m, orange
slc_data = []
global_detections = {} #will look like {a: {'boxxmax': ymax: xmin:, ymin:}}
def compare(past,cur):
    if not past:
        for det_ in cur:
            cur[det_]["heading"] = 'unknown'
        return cur
    else:
        case = 0
        size = 0
        if len(past) < len(cur):
            size = len(cur)
            case = 1
        elif len(past) > len(cur):
            size = len(past)
            case = 2
        else:
            size = len(cur)

        costs = np.ones((size,size)) *1000
        for i,pdet in enumerate(past):
            for j,cdet in enumerate(cur):
                costs[i,j] = np.distance.euclidian(pdet['c'],cdet)
        m = Munkres()
        indexes = m.compute(costs)
    cur_lst = list(cur.keys())
    past_lst = list(past.keys())

    for row,column in indexes:
        if costs[row,column] < 900:
            cur[cur_lst[column]]['heading'] = cur[cur_lst[column]]['centroid'] - past[past_lst[row]]['centroid']
        # decide what to do about new points, this should update the heading, decide what to do about missing points,
            # change obstacle to bfs path
    
        

        
        
        
               
                
            

        


        
            
def cb(packet: packets.DisparityDepthPacket):
    global slc_data
    fontType = cv2.FONT_HERSHEY_TRIPLEX 

    depthFrameColor = packet.visualizer.draw(packet.frame)
    detections = {}
    to_use = ['a','b','c','d','e','f','g','h','i','j','k']
    visited = set()
    check_boxes = {}
    to_explore = []
    obstacles = []
    z_s= []
    for i,depthData in enumerate(slc_data):
            roi = depthData.config.roi
            roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
            x= round(roi.topLeft().x/0.0625 - .5) //1280 +1
            y = round(roi.topLeft().y/0.1 - .5) // 720 + 1
            distance = math.sqrt(coords.x ** 2 + coords.y ** 2 + coords.z ** 2)
            z_s.append(coords.z)
            if distance < WARNING:
                to_explore.append(x,y,i)
                check_boxes[(x,y)] =i

        
    # Assuming `to_explore` contains the initial positions to start exploring from


    for x, y, i in to_explore:
        if (x, y) not in visited:
            queue = []
            visited.add((x, y))
            queue.append((x, y, i))
            j = 0
            while j < len(queue):
                x, y, i = queue[j]

                # Define directions for adjacent and diagonal movements
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in check_boxes and (nx, ny) not in visited:
                        
                        if z_s[check_boxes[nx,ny]] +100 > z_s[i] and z_s[check_boxes[nx,ny]] -100 < z_s[i]:
                            visited.add((nx, ny))
                            queue.append((nx, ny, check_boxes[(nx, ny)]))
                j += 1
            obstacles.append(queue) 





                


    for depthData in slc_data:
        roi = depthData.config.roi
        roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])

        xmin = int(roi.topLeft().x)
        ymin = int(roi.topLeft().y)
        xmax = int(roi.bottomRight().x)
        ymax = int(roi.bottomRight().y)
        x= round(roi.topLeft().x/0.0625 - .5) //1280 +1
        y = round(roi.topLeft().y/0.1 - .5) // 720 + 1

        coords = depthData.spatialCoordinates
        distance = math.sqrt(coords.x ** 2 + coords.y ** 2 + coords.z ** 2)

        if distance == 0: # Invalid
            continue


        elif distance < WARNING:
            if detections:
                found = False
                for det_ in detections:
                    det = detections[det_]
                    if not found:
                        if (x >= det['boxxmin'] -1) and x <= det['boxxmax'] + 1: # check within x +-1
                            if (y >= det['boxymin'] -1) and  y <= det['boxymax'] + 1: #check within y +-1
                                if det['coordinates'][-1] + 500 > coords.z and det['coordinates'][-1] - 500 < coords.z: #add to object
                                    found = True
                                    detections[det_]["boxxmin"] = min(detections[det_]["boxxmin"],x)
                                    detections[det_]["boxymin"] = min(detections[det_]["boxymin"],y)
                                    detections[det_]["boxxmax"] = max(detections[det_]["boxxmax"],x)
                                    detections[det_]["boxymax"] = max(detections[det_]["boxymax"],y)
                                    detections[det_]["coordinates"] = (max(detections[det_]["coordinates"][0],xmax),\
                                                                      max(detections[det_]["coordinates"][1],ymax),\
                                                                        min(detections[det_]["coordinates"][2],xmin),\
                                                                              min(detections[det_]["coordinates"][3],ymin),\
                                                                                  min(detections[det_]["coordinates"][4],coords.z)) #updates the coords of object, uses worst case depth
                if not found:
                    detections[to_use.pop(0)] = {"boxxmin":x,"boxxmax":x,'boxymin':y, 'boxymax':y,'coordinates': (xmax,ymax,xmin,ymin,coords.z)} #doesn't match any object in current iteration

            else:
                detections[to_use.pop(0)] = {"boxxmin":x,"boxxmax":x,'boxymin':y, 'boxymax':y,'coordinates': (xmax,ymax,xmin,ymin,coords.z)} #first detection


            color = (0, 140, 255)
            cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, thickness=2)
            cv2.putText(depthFrameColor, "{:.1f}m {}x {}y {}z".format(distance/1000,round(coords.x/1000,2),round(coords.y/1000,2),round(coords.z/1000,2)), (xmin + 10, ymin + 20), fontType, 0.3, color)
        #calculate centroids
        for det_ in detections:
                botx,boty,topx,topy,z = detections[det_]['coordinates']
                detections[det_]['centroid'] = np.array([(topx+botx)/2,(topy+boty)/2, z])
    print(detections)
    cv2.imshow('0_depth', depthFrameColor)

with OakCamera() as oak:
    stereo = oak.create_stereo('720p')
    # We don't need high fill rate, just very accurate depth, that's why we enable some filters, and
    # set the confidence threshold to 50
    config = stereo.node.initialConfig.get()
    config.postProcessing.brightnessFilter.minBrightness = 0
    config.postProcessing.brightnessFilter.maxBrightness = 255
    stereo.node.initialConfig.set(config)
    stereo.config_postprocessing(colorize=StereoColor.RGBD, colormap=cv2.COLORMAP_BONE)
    stereo.config_stereo(confidence=50, lr_check=True, extended=True)

    oak.visualize([stereo], fps=True, callback=cb)

    slc = oak._pipeline.create(dai.node.SpatialLocationCalculator)
    for x in range(15):
        for y in range(9):
            config = dai.SpatialLocationCalculatorConfigData()
            config.depthThresholds.lowerThreshold = 200
            config.depthThresholds.upperThreshold = 10000
            config.roi = dai.Rect(dai.Point2f((x+0.5)*0.0625, (y+0.5)*0.1), dai.Point2f((x+1.5)*0.0625, (y+1.5)*0.1))
            # TODO: change from median to 10th percentile once supported
            config.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.MIN
            slc.initialConfig.addROI(config)

    stereo.depth.link(slc.inputDepth)

    slc_out = oak._pipeline.create(dai.node.XLinkOut)
    slc_out.setStreamName('slc')
    slc.out.link(slc_out.input)

    oak.start() # Start the pipeline (upload it to the OAK)

    q = oak.device.getOutputQueue('slc') # Create output queue after calling start()
    while oak.running():
        if q.has():
            slc_data = q.get().getSpatialLocations()
        oak.poll()
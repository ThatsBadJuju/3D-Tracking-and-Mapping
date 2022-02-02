import cv2
import OpenCVTest as camera
import Regression_Calc as regression
import time

webcam = camera.init_cam()

def current_time_milliseconds():
    return round(time.time() * 1000)

#a few global variables
start_time = current_time_milliseconds()
x_pos = []
y_pos = []
radius = []
times_between_scans = []
time_between_scans = 0

#run until
while True:
    ball_pos, ball_radius = camera.scan_ball(webcam)
    end_run = camera.check_for_end()

    #saves the time between each camera frame in milliseconds
    time_per_scan = current_time_milliseconds() - start_time
    time_between_scans += time_per_scan
    start_time = current_time_milliseconds()

    #if scan detected a ball then save the position / radius
    if ball_pos != (-1, -1) and ball_radius != -1:
        x_pos.append(ball_pos[0])
        y_pos.append(ball_pos[1])
        radius.append(ball_radius)
        times_between_scans.append(time_between_scans)
        time_between_scans = 0
    if not end_run:
        camera.stop_cam(webcam)
        break

seconds_between_scans = [milli / 1000.0 for milli in times_between_scans]

# calculates (roughly) the time between each scan in seconds
# disgusting code but it works I guess
seconds_elapsed = 0
total_seconds_between_scans = []
for seconds in seconds_between_scans:
    seconds_elapsed += seconds
    total_seconds_between_scans.append(seconds_elapsed)

# shift each time in the array to match the start of the first completed scan in the array
total_seconds_between_scans_adj = [seconds - total_seconds_between_scans[0] for seconds in total_seconds_between_scans]

y_graph = [y*-1 + 400 for y in y_pos]

# graphs of y_pos-t and radius-t
quadratic_constants = regression.create_quad_regression_plot(total_seconds_between_scans_adj, y_graph, total_seconds_between_scans_adj[-1] * 1.1)
print("y = ", quadratic_constants[0], "t^2 + ", quadratic_constants[1], "t + ", quadratic_constants[2])
radius_over_time = regression.create_lin_regression_plot(total_seconds_between_scans_adj, radius, total_seconds_between_scans_adj[-1] * 1.1)
print("r = ", radius_over_time[0], "t + ", radius_over_time[1])

# TODO: Add a Z-direction by checking the rate of change of the size of the ball
# then (if the camera quality allows) find the true trajectory (in inches instead of arbitrary numbers) by comparing to some image

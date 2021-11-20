import cv2
import OpenCVTest as camera
import QuadraticRegression as quad
import time

webcam = camera.init_cam()

def current_time_milliseconds():
    return round(time.time() * 1000)

start_time = current_time_milliseconds()
x_pos = []
y_pos = []
times_between_scans = []
time_between_scans = 0
while True:
    ball_pos = camera.scan_ball(webcam) #ball_pos[0] = x, ball_pos[1] = y
    end_run = camera.check_for_end()

    time_per_scan = current_time_milliseconds() - start_time
    time_between_scans += time_per_scan
    start_time = current_time_milliseconds()


    if ball_pos is not None:
        x_pos.append(ball_pos[0])
        y_pos.append(ball_pos[1])
        times_between_scans.append(time_between_scans)
        time_between_scans = 0
    if not end_run:
        camera.stop_cam(webcam)
        break

seconds_between_scans = [milli / 1000.0 for milli in times_between_scans]

seconds_elapsed = 0
total_seconds_between_scans = []
for seconds in seconds_between_scans:
    seconds_elapsed += seconds
    total_seconds_between_scans.append(seconds_elapsed)

total_seconds_between_scans_adj = [seconds - total_seconds_between_scans[0] for seconds in total_seconds_between_scans]


y_graph = [y*-1 + 400 for y in y_pos]

#print(total_seconds_between_scans_adj, y_graph)

quadratic_constants = quad.create_quad_regression_plot(total_seconds_between_scans_adj, y_graph, total_seconds_between_scans_adj[-1] * 1.1)
print("y = ", quadratic_constants[0], "x^2 + ", quadratic_constants[1], "x + ", quadratic_constants[2])

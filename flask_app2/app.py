from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
from datetime import datetime
from image_processing import process_image

app = Flask(__name__)

# Dictionary to store the camera objects
cameras = {}

def gen_frames(camera_id):
    cap = cv2.VideoCapture(camera_id)
    cameras[camera_id] = cap
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Apply some image processing (e.g., converting to grayscale)
            frame = process_image(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    camera_id = int(request.args.get('camera_id', 0))
    return Response(gen_frames(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_image', methods=['GET'])
def save_image():
    camera_id = int(request.args.get('camera_id', 0))
    color = request.args.get('color', 'none')
    cap = cameras.get(camera_id)
    if cap is not None and cap.isOpened():
        success, frame = cap.read()
        if success:
            # Define the folder path based on the color
            folder_path = os.path.join('saved_images', color)
            os.makedirs(folder_path, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{color}_{timestamp}.png"  # Change to .png
            filepath = os.path.join(folder_path, filename)
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # Save as PNG with no compression
            return jsonify({'status': 'success', 'filepath': filepath})
    return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

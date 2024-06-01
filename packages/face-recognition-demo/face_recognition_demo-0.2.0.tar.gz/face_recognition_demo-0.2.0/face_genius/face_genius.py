from face_recognition import load_image_file, face_encodings, compare_faces
import os


def load_and_encode_image(image_path):
    image = load_image_file(image_path)
    encodings = face_encodings(image)
    if encodings:
        return encodings[0]
    else:
        raise ValueError("No faces found in the image!")


def recognize_faces(known_face_encodings, image_path_to_check):
    image_to_check = load_image_file(image_path_to_check)
    encodings_to_check = face_encodings(image_to_check)
    for face_encoding in encodings_to_check:
        matches = compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            return True
    return False

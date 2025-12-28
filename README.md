# Blind-s-Eye-project
---

# 🤟 Sign Language Recognition with Text-to-Speech Assistance

This project is a real-time Sign Language Recognition system** built using **Python, OpenCV, and MediaPipe, enhanced with Text-to-Speech (TTS) technology to assist visually impaired (blind) users.

The system recognizes hand gestures from a webcam, converts them into **American Sign Language (ASL) text**, and then **speaks the recognized sign aloud**, making communication more inclusive and accessible.

---

## 🌟 Key Features

* Real-time hand gesture detection using webcam
* Recognition of basic ASL gestures (A–Z or subset)
* Live display of recognized sign on video feed
* **Text-to-Speech output for blind/visually impaired users**
* Audio feedback of recognized gestures
* Watermark displayed on screen

---

## ♿ Accessibility Focus

This project aims to bridge the communication gap by:

* Helping **visually impaired users hear recognized gestures**
* Supporting **inclusive human–computer interaction**
* Combining **computer vision + assistive technology**

---

## 🛠️ Technologies Used

* **Python 3.7+**
* **OpenCV** – video capture and image processing
* **MediaPipe** – real-time hand tracking
* **NumPy** – numerical operations
* **Text-to-Speech (pyttsx3 / gTTS)** – audio output

---

## 📦 Installation

Install all required dependencies:

```bash
pip install opencv-python mediapipe numpy pyttsx3
```

*(Optional: For cloud-based voice output)*

```bash
pip install gtts playsound
```

---

## ▶️ How to Run the Project

1. Clone the repository:

   ```bash
   https://github.com/JahnaviSingh2005/Blind-s-Eye-project.git
   ```

2. Navigate to the project folder:

   ```bash
   cd sign-language-recognition
   ```

3. Run the main file:

   ```bash
   python main.py
   ```

---

## 🔊 How Text-to-Speech Works

* When a hand gesture is recognized:

  * The corresponding **ASL character/text** is displayed on screen
  * The system **converts the text into speech**
  * The audio output announces the recognized sign aloud

This allows **blind or visually impaired users** to understand gestures through sound.

---

## 📌 Project Notes

* Use a **plain background** and **good lighting** for best accuracy
* Webcam must be properly positioned
* This is a **prototype/demo-level project**
* Accuracy depends on gesture clarity and lighting conditions

---

## 🔮 Future Enhancements

* Full ASL alphabet and word-level recognition
* Sentence formation with continuous gestures
* Deep learning-based gesture classification (CNN / LSTM)
* Multi-language speech output
* Mobile or web application integration

---

## 👩‍💻 Author

**Jahnavi Singh**
B.Tech Student | AI, Computer Vision & Assistive Technology Enthusiast

---

Just say the word 🚀


---

## ⚙️ How to Run

1. Download or clone the project folder.  
2. Open the folder in VS Code or any editor.  
3. Double-click **`index.html`** to open it in your web browser.  
4. Enter a phone number or email → click **Login** → view the **Home Page**.

---

## 🧠 Tech Stack
- **HTML5** – Structure  
- **CSS3** – Styling & layout  
- **JavaScript (Vanilla)** – Logic & interactivity  

---

## 🧾 Notes
- No backend is used — this is a **front-end demo**.
- You can easily connect it to Firebase, Node.js, or any API for authentication.

---

## 📸 Preview
*(Add a screenshot of your UI here if available)*

---

## 👨‍💻 Author
**Rudra**  
✨ Designed and developed for practice / prototype UI.

---

## 📚 Custom object-detection (dataset & training)

This project now includes an in-browser dataset collection flow and helpers to train a custom object detector (for classes like phone, person, pen, chain, table, watch, bottle, etc.).

Quick workflow:

1. Run the app and open the Object Detection page.
2. Click "Start Annotation", draw a bounding box on the live video, pick a label and "Save Annotation".
3. Repeat for samples across classes. Click "Download Dataset" to save `annotations_dataset.json`.
4. Convert the downloaded JSON into images + COCO annotations using the helper script:

	python tools/convert_annotations.py path/to/annotations_dataset.json out_dataset_folder

	The script writes `out_dataset_folder/images/` and `out_dataset_folder/annotations.json` (COCO format).

5. Upload to Roboflow (recommended) or use your preferred training pipeline:
	- Roboflow: create an Object Detection project and import the COCO `annotations.json` and images.
	- Train, validate, then export a TFJS model or use Roboflow's hosted inference endpoint.

6. To run a hosted Roboflow model in the app: on the Object Detection page choose "Roboflow Hosted", paste your endpoint string (e.g. `your-model-name/1`) and API key. The app will send frames to the endpoint and draw predictions returned by Roboflow.

Notes:
- The helper script requires Pillow: `pip install pillow`.
- Teachable Machine is for classification (not bounding boxes). For detection choose Roboflow or the TensorFlow Object Detection API.
- If you want me to add automated upload to Roboflow or direct TFJS model loading in the app, I can implement that next.

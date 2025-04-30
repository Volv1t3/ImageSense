<body style="font-family: Consolas, sans-serif; font-weight: normal; font-size: 12pt; color: beige">

<blockquote style="font-style: italic; color: whitesmoke"> <blockquote style="font-style: italic; color: whitesmoke; font-size: 9pt; text-align: center"> Hi there! I'm a huge fan of Markdown documents, so apologies in advanced for structuring this as one </blockquote>

***

<h3 style="text-align: center; font-size: large"> ImageSense: A Modern Desktop Application for Image Processing and Analysis</h3>

<h4 style="text-align: center; font-size: medium"> A comprehensive desktop application for image manipulation and computer vision processing</h4>

***

<div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 20px 0;">


![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)

![PyQt5](https://img.shields.io/badge/PyQt5-%2341CD52.svg?style=for-the-badge&logo=qt&logoColor=white)

![OpenCV](https://img.shields.io/badge/opencv-%235C3EE8.svg?style=for-the-badge&logo=opencv&logoColor=white)

</div>

<blockquote style="font-style: italic; color: whitesmoke">

<h2 style="color: beige; font-size: 14pt">&boxUR; Repository Description &boxUL;  </h2>

<p>ImageSense is a sophisticated desktop application that provides powerful image processing and computer vision capabilities. Built with Python and PyQt5, it offers an intuitive user interface for applying various image effects and transformations. The application leverages OpenCV for advanced image processing operations and includes support for YOLO-based object detection.
<br><br>
The application is designed with a modular architecture that separates the UI components from the core processing logic, making it both maintainable and extensible. It features a rich set of image manipulation tools including blur effects, noise addition, black & white conversion, and wave distortion.
</p>
<br>
<p>The repository is organized into several key directories, with the main components residing in the <code>src</code> folder. Each component is carefully structured to maintain separation of concerns and promote code reusability.
<br>
<br>
Here are some important details for those who wish to explore the files!
</p>
<ul>
<code>File Structure</code>
<li><b>src/</b>: The main source directory containing all application code:
    <ul>
    <li><b>Views/</b>: Contains all UI-related components and window definitions</li>
    <li><b>Models/</b>: Houses the core business logic and data processing modules</li>
    <li><b>main.py</b>: The application entry point</li>
    </ul>
</li>
</ul>

</blockquote>

***

<blockquote style="font-style: italic; color: whitesmoke">

<h2 style="color: beige; font-size: 14pt">&boxUR; Methodology &boxUL;  </h2>

<p>The application's architecture is divided into three main components:
<br><br>
The UI components in <code>Views</code> manage the application's visual interface, including the main window and various control panels. The left panel provides image modification tools, while other panels handle different aspects of the application.
<br><br>
Image processing operations are implemented using OpenCV and run in separate background threads to maintain UI responsiveness. The application includes several key features:
</p>

<ol>
<li>Basic Image Operations: Blur, noise addition, and black & white conversion</li>
<li>Advanced Effects: Wave distortion and other transformations</li>
<li>Background Processing: All operations run in separate threads</li>
<li>Real-time Preview: Immediate visual feedback for all operations</li>
<li>Error Handling: Robust error management for all operations</li>
</ol>

<p>Each image processing operation is implemented as a separate worker class, inheriting from QThread to ensure smooth UI performance during processing.</p>

</blockquote>

***

<blockquote style="font-style: italic; color: whitesmoke">

<h2 style="color: beige; font-size: 14pt">&boxUR; Libraries Used and How to Run &boxUL;  </h2>

<p>The project relies on several key libraries:</p>
<ul>
<li>PyQt5 for the graphical user interface</li>
<li>OpenCV (cv2) for image processing operations</li>
<li>NumPy for numerical operations and array handling</li>
<li>YOLOv4 for object detection capabilities</li>
</ul>

<p>To run the application:</p>
<ol>
<li>Ensure Python 3.11.9 is installed on your system</li>
<li>Install the required dependencies from requirements.txt</li>
  <li> Download the required yolov4.weights file from <a href="https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights">here </a> </li>
<li>Navigate to the src directory</li>
<li>Run main.py to start the application</li>
</ol>

<p>The application requires proper setup of the Python environment and all dependencies to function correctly.</p>

</blockquote>

<blockquote>
<h2 style="color: beige; font-size: 14pt">&boxUR; Authors &boxUL;  </h2>

<ul>
<li>Maria Granda Anazco</li>
<li>Santiago Arellano</li>
</ul>
</blockquote>
</body>

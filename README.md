# Tkinter Drawing Editor

A simple vector-based drawing application built with Python and the Tkinter library. This application allows users to draw lines and rectangles, select and group objects, and save/load their work to an XML file.

## Features

-   **Draw Shapes**: Create basic geometric shapes like lines and rectangles.
-   **Object Selection**:
    -   Select a single object.
    -   Select multiple objects to perform group actions.
-   **Grouping/Ungrouping**:
    -   Group multiple selected objects into a single entity.
    -   Ungroup a previously created group back into its individual components.
-   **Save and Load**:
    -   Save your drawing to a structured XML file.
    -   Open and load a drawing from an XML file, recreating the saved shapes on the canvas.

## Prerequisites

-   **Python 3**: The application is written in Python 3.
-   **Tkinter**: Tkinter is the standard GUI library for Python and is usually included with Python installations. If it's not present, you may need to install it separately (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu).

## How to Run

1.  Save the code as a Python file (e.g., `drawing_app.py`).
2.  Open your terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the application with the following command:

    ```bash
    python drawing_app.py
    ```

## How to Use

The application window consists of a main canvas, a menu bar, and a toolbar with action buttons.

### Drawing Shapes

1.  **Draw a Line**:
    -   Click the **"Draw Line"** button.
    -   Click and hold the left mouse button on the canvas to set the starting point.
    -   Drag the mouse to the desired endpoint.
    -   Release the mouse button to finish the line.

2.  **Draw a Rectangle**:
    -   Click the **"Draw Rectangle"** button.
    -   Click and hold the left mouse button on the canvas to set the first corner.
    -   Drag the mouse to the desired opposite corner.
    -   Release the mouse button to finish the rectangle.

### Selecting Objects

1.  **Select a Single Object**:
    -   Click the **"Select objects"** button. This enables single-selection mode.
    -   Click near the border of a line or rectangle. The selected object will be highlighted with a dashed outline.
    -   Selecting a new object will automatically deselect the previous one.

2.  **Select Multiple Objects**:
    -   Click the **"Select multiple objects"** button. This enables multi-selection mode.
    -   Click on any objects you wish to add to the selection. Each selected object will be highlighted.
    -   To clear the selection, click the "Select objects" or "Select multiple objects" button again.

### Grouping and Ungrouping

1.  **Group Objects**:
    -   First, select two or more objects using the multi-select mode.
    -   Click the **"Group Objects"** button.
    -   The individual object highlights will disappear, and a single blue, dashed rectangle will appear, bounding all the grouped objects. This rectangle now represents the group.

2.  **Ungroup Objects**:
    -   First, select a group by clicking its blue, dashed bounding box (use single-select mode).
    -   Click the **"Ungroup Objects"** button.
    -   The blue bounding box will be removed, and the objects will once again be individual entities.

### Saving and Loading

1.  **Save Drawing**:
    -   Go to the **File** menu and click **Save**.
    -   A file dialog will open, allowing you to choose a location and name for your `.xml` file.
    -   Click "Save" to complete the process.

2.  **Load Drawing**:
    -   Go to the **File** menu and click **Open**.
    -   A file dialog will open. Navigate to and select a previously saved `.xml` file.
    -   Click "Open". The current canvas will be cleared, and the drawing from the file will be loaded.

## XML File Format

The drawings are saved in a simple XML format. This makes the data human-readable and easy to parse.

-   Each shape (`line`, `rectangle`) is a top-level element within the root `<drawing>` tag.
-   Coordinates and properties like color are stored in nested tags.

### Example XML Structure

```xml
<drawing>
    <line>
        <begin>
            <x>150</x>
            <y>180</y>
        </begin>
        <end>
            <x>350</x>
            <y>250</y>
        </end>
        <color>black</color>
    </line>
    <rectangle>
        <upper-left>
            <x>400</x>
            <y>400</y>
        </upper-left>
        <lower-right>
            <x>600</x>
            <y>550</y>
        </lower-right>
        <color>black</color>
        <corner>square</corner>
    </rectangle>
</drawing>
```

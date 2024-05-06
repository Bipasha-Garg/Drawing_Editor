import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import xml.etree.ElementTree as ET

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Editor")

        self.canvas = tk.Canvas(
            root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white"
        )
        self.canvas.pack()

        self.lines = []
        self.rectangles = []
        self.selected_objs = []
        self.single_select = 0
        self.group_rect = None  # Store reference to the group rectangle

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_from_xml)
        file_menu.add_command(label="Save", command=self.save_to_xml)
        self.menu.add_cascade(label="File", menu=file_menu)

    def create_toolbar(self):
        self.draw_line_button = tk.Button(
            self.root, text="Draw Line", command=self.draw_line
        )
        self.draw_line_button.pack(side=tk.LEFT, padx=5)

        self.draw_rectangle_button = tk.Button(
            self.root, text="Draw Rectangle", command=self.draw_rectangle
        )
        self.draw_rectangle_button.pack(side=tk.LEFT, padx=5)

        self.select_objects_button = tk.Button(
            self.root, text="Select objects", command=self.toggle_select_mode
        )
        self.select_objects_button.pack(side=tk.LEFT, padx=5)

        self.select_objects_button = tk.Button(
            self.root,
            text="Select multiple objects",
            command=self.toggle_multi_select_mode,
        )
        self.select_objects_button.pack(side=tk.LEFT, padx=5)

        self.group_objects_button = tk.Button(
            self.root, text="Group Objects", command=self.group_objects
        )
        self.group_objects_button.pack(side=tk.LEFT, padx=5)

        self.ungroup_objects_button = tk.Button(
            self.root, text="Ungroup Objects", command=self.ungroup_objects
        )
        self.ungroup_objects_button.pack(side=tk.LEFT, padx=5)

    def save_to_xml(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml", filetypes=[("XML Files", "*.xml")]
        )
        if filename:
            try:
                root = ET.Element("drawing")

                # Save lines
                for line in self.lines:
                    line_elem = ET.SubElement(root, "line")

                    begin_elem = ET.SubElement(line_elem, "begin")
                    begin_x_elem = ET.SubElement(begin_elem, "x")
                    begin_x_elem.text = str(line[1])
                    begin_y_elem = ET.SubElement(begin_elem, "y")
                    begin_y_elem.text = str(line[2])

                    end_elem = ET.SubElement(line_elem, "end")
                    end_x_elem = ET.SubElement(end_elem, "x")
                    end_x_elem.text = str(line[3])
                    end_y_elem = ET.SubElement(end_elem, "y")
                    end_y_elem.text = str(line[4])

                    color_elem = ET.SubElement(line_elem, "color")
                    color_elem.text = "black"

                # Save rectangles
                for rect in self.rectangles:
                    rect_elem = ET.SubElement(root, "rectangle")

                    upper_left_elem = ET.SubElement(rect_elem, "upper-left")
                    upper_left_x_elem = ET.SubElement(upper_left_elem, "x")
                    upper_left_x_elem.text = str(rect[1])
                    upper_left_y_elem = ET.SubElement(upper_left_elem, "y")
                    upper_left_y_elem.text = str(rect[2])

                    lower_right_elem = ET.SubElement(rect_elem, "lower-right")
                    lower_right_x_elem = ET.SubElement(lower_right_elem, "x")
                    lower_right_x_elem.text = str(rect[3])
                    lower_right_y_elem = ET.SubElement(lower_right_elem, "y")
                    lower_right_y_elem.text = str(rect[4])

                    color_elem = ET.SubElement(rect_elem, "color")
                    color_elem.text = "black"

                    corner_elem = ET.SubElement(rect_elem, "corner")
                    corner_elem.text = "rounded" if rect[5] == "rounded" else "square"

                # Create XML tree and write to file
                tree = ET.ElementTree(root)
                tree.write(filename)

                messagebox.showinfo(
                    "Save Successful", "Drawing saved to XML successfully."
                )

            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred: {e}")

    def load_from_xml(self):
        filename = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if filename:
            try:
                tree = ET.parse(filename)
                root = tree.getroot()

                # Clear current drawing
                self.canvas.delete("all")
                self.lines = []
                self.rectangles = []
                self.selected_objs = []

                # Load lines and rectangles
                for element in root:
                    if element.tag == "line":
                        begin_elem = element.find("begin")
                        end_elem = element.find("end")
                        color_elem = element.find("color")

                        begin_x = int(begin_elem.find("x").text)
                        begin_y = int(begin_elem.find("y").text)
                        end_x = int(end_elem.find("x").text)
                        end_y = int(end_elem.find("y").text)

                        color = color_elem.text

                        line_id = self.canvas.create_line(
                            begin_x, begin_y, end_x, end_y, fill=color
                        )
                        self.lines.append((line_id, begin_x, begin_y, end_x, end_y))
                    elif element.tag == "rectangle":
                        upper_left_elem = element.find("upper-left")
                        lower_right_elem = element.find("lower-right")
                        color_elem = element.find("color")
                        corner_elem = element.find("corner")

                        upper_left_x = int(upper_left_elem.find("x").text)
                        upper_left_y = int(upper_left_elem.find("y").text)
                        lower_right_x = int(lower_right_elem.find("x").text)
                        lower_right_y = int(lower_right_elem.find("y").text)

                        color = color_elem.text
                        corner = corner_elem.text

                        rect_id = self.canvas.create_rectangle(
                            upper_left_x,
                            upper_left_y,
                            lower_right_x,
                            lower_right_y,
                            outline=color,
                        )
                        self.rectangles.append(
                            (
                                rect_id,
                                upper_left_x,
                                upper_left_y,
                                lower_right_x,
                                lower_right_y,
                                corner,
                            )
                        )

                messagebox.showinfo(
                    "Load Successful", "Drawing loaded from XML successfully."
                )

            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred: {e}")

    def draw_line(self):
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_temp_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

    def draw_rectangle(self):
        self.canvas.bind("<Button-1>", self.start_rectangle)
        self.canvas.bind("<B1-Motion>", self.draw_temp_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)

    def start_line(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_object = self.canvas.create_line(
            self.start_x, self.start_y, self.start_x, self.start_y, fill="black"
        )

    def draw_temp_line(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.current_object, self.start_x, self.start_y, x, y)

    def end_line(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.current_object, self.start_x, self.start_y, x, y)
        self.lines.append((self.current_object, self.start_x, self.start_y, x, y))
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def start_rectangle(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_object = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="black"
        )

    def draw_temp_rectangle(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.current_object, self.start_x, self.start_y, x, y)

    def end_rectangle(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.current_object, self.start_x, self.start_y, x, y)
        self.rectangles.append((self.current_object, self.start_x, self.start_y, x, y))
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def toggle_select_mode(self):
        self.single_select = 1
        self.unhighlight_objs()
        self.canvas.bind("<Button-1>", self.select_object)

    def toggle_multi_select_mode(self):
        self.single_select = 0
        self.unhighlight_objs()
        self.canvas.bind("<Button-1>", self.select_object)

    def select_object(self, event):
        if self.single_select == 1:
            self.unhighlight_objs()
        x, y = event.x, event.y
        test = 0
        for obj in self.lines:
            if self.is_on_line(obj[1], obj[2], obj[3], obj[4], x, y):
                test = 1
                self.selected_objs.append(obj)
                break
        self.highlight_selected_objects()
        if self.single_select == 1 and test == 1:
            return
        for obj in self.rectangles:
            if self.is_on_rectangle_border(obj[1], obj[2], obj[3], obj[4], x, y):
                self.selected_objs.append(obj)
                break
        self.highlight_selected_objects()

    def is_on_line(self, x1, y1, x2, y2, x, y):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            # Line segment is a point
            return x == x1 and y == y1
        else:
            t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
            if t < 0:
                # Point is closest to the start point of the line segment
                closest_x, closest_y = x1, y1
            elif t > 1:
                # Point is closest to the end point of the line segment
                closest_x, closest_y = x2, y2
            else:
                # Point is closest to the line segment itself
                closest_x = x1 + t * dx
                closest_y = y1 + t * dy
            # Check if the closest point is within a certain distance threshold of the actual point
            distance_threshold = 5
            return (
                (x - closest_x) ** 2 + (y - closest_y) ** 2
            ) ** 0.5 <= distance_threshold

    def is_on_rectangle_border(self, x1, y1, x2, y2, x, y, distance_threshold=10):

        if (
            min(abs(x - x1), abs(x - x2)) < distance_threshold
            and y > y1 + distance_threshold
            and y < y2 - distance_threshold
        ):
            return True  # left or right side
        elif (
            min(abs(y - y1), abs(y - y2)) < distance_threshold
            and x > x1 + distance_threshold
            and x < x2 - distance_threshold
        ):
            return True  # top or bottom side
        else:
            return False

    def highlight_selected_objects(self):
        for obj in self.selected_objs:
            obj_id = obj[0]
            obj_type = self.canvas.type(obj_id)

            # Change the appearance based on the type of object
            if obj_type == "line":
                self.canvas.itemconfig(obj_id, dash=(3, 3), fill="black")
            elif obj_type == "rectangle":
                self.canvas.itemconfig(obj_id, dash=(3, 3), outline="black")

    def unhighlight_objs(self):
        for obj in self.selected_objs:
            obj_id = obj[0]  # Extract the object ID
            obj_type = self.canvas.type(
                obj_id
            )  # Get the type of the object (line or rectangle)

            # Restore the original appearance based on the type of object
            if obj_type == "line":
                self.canvas.itemconfig(obj_id, dash=(), fill="black")
            elif obj_type == "rectangle":
                # Check if the rectangle originally had a dashed outline
                if self.canvas.itemcget(obj_id, "dash") == (3, 3):
                    self.canvas.itemconfig(obj_id, dash=(3, 3), outline="blue")
                else:
                    self.canvas.itemconfig(obj_id, dash=(), outline="black")
        self.selected_objs = []

    def group_objects(self):
        # Check for minimum two selected objects
        if len(self.selected_objs) < 2:
            messagebox.showwarning("Warning", "Select at least two objects to group.")
            return

        # Check if the selected objects belong to an existing group
        if len(self.selected_objs) == 1 and len(self.selected_objs[0]) == 6:
            existing_group_rect = self.selected_objs[0][0]
            existing_group_objs = self.selected_objs[0][5]

            # Remove the existing group rectangle
            self.canvas.delete(existing_group_rect)

            # Update the list of rectangles by removing the existing group
            self.rectangles.remove(self.selected_objs[0])

            # Add the selected objects to the list of objects to be grouped
            for obj_data in self.selected_objs:
                self.rectangles.append(obj_data)

            # Initialize min and max coordinates with extreme values
            min_x = float("inf")
            min_y = float("inf")
            max_x = float("-inf")
            max_y = float("-inf")

            # Iterate over selected objects to find the actual bounding box
            for obj_data in self.selected_objs:
                obj_id = obj_data[0]
                obj_type = self.canvas.type(obj_id)

                if obj_type == "line":
                    # For lines, consider the two endpoints
                    x1, y1, x2, y2 = self.canvas.coords(obj_id)
                    min_x = min(min_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)
                elif obj_type == "rectangle":
                    # For rectangles, consider all four vertices
                    x1, y1, x2, y2 = self.canvas.coords(obj_id)
                    min_x = min(min_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)

            # Create a rectangle to represent the updated group
            group_rect = self.canvas.create_rectangle(
                min_x, min_y, max_x, max_y, outline="blue", dash=(3, 3)
            )

            # Add selected objects to the group
            group_objs = [obj_data[0] for obj_data in self.selected_objs]

            # Unhighlight and clear selected objects
            self.unhighlight_objs()
            self.selected_objs = []

            # Bind group selection to the new group object
            self.canvas.tag_bind(
                group_rect,
                "<Button-1>",
                lambda event, objs=group_objs, rect=group_rect: self.select_group(
                    event, objs, rect
                ),
            )

            # Store the group rectangle and its associated objects
            self.rectangles.append((group_rect, min_x, min_y, max_x, max_y, group_objs))

        else:
            # Initialize min and max coordinates with extreme values
            min_x = float("inf")
            min_y = float("inf")
            max_x = float("-inf")
            max_y = float("-inf")

            # Iterate over selected objects to find the actual bounding box
            for obj_data in self.selected_objs:
                obj_id = obj_data[0]
                obj_type = self.canvas.type(obj_id)

                if obj_type == "line":
                    # For lines, consider the two endpoints
                    x1, y1, x2, y2 = self.canvas.coords(obj_id)
                    min_x = min(min_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)
                elif obj_type == "rectangle":
                    # For rectangles, consider all four vertices
                    x1, y1, x2, y2 = self.canvas.coords(obj_id)
                    min_x = min(min_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)
                # Add logic for other types of objects if needed

            # Create a rectangle to represent the group
            group_rect = self.canvas.create_rectangle(
                min_x, min_y, max_x, max_y, outline="blue", dash=(3, 3)
            )

            # Add selected objects to the group
            group_objs = [obj_data[0] for obj_data in self.selected_objs]

            # Unhighlight and clear selected objects
            self.unhighlight_objs()
            self.selected_objs = []

            # Bind group selection to the new group object
            self.canvas.tag_bind(
                group_rect,
                "<Button-1>",
                lambda event, objs=group_objs, rect=group_rect: self.select_group(
                    event, objs, rect
                ),
            )

            # Store the group rectangle and its associated objects
            self.rectangles.append((group_rect, min_x, min_y, max_x, max_y, group_objs))

    def select_group(self, event, group_objs, group_rect):
        self.unhighlight_objs()
        for obj in group_objs:
            self.selected_objs.append((obj,))
        self.highlight_selected_objects()

        # Bind group selection to the new group object
        self.canvas.tag_bind(
            group_rect,
            "<Button-1>",
            lambda event, objs=group_objs, rect=group_rect: self.select_group(
                event, objs, rect
            ),
        )

    def ungroup_objects(self):
        if len(self.selected_objs) == 1 and len(self.selected_objs[0]) == 6:
            group_rect = self.selected_objs[0][0]
            group_objs = self.selected_objs[0][5]

            # Remove the group rectangle
            self.canvas.delete(group_rect)

            # Remove the group from the list of rectangles
            self.rectangles.remove(self.selected_objs[0])

            # Re-add individual objects to the canvas
            for obj_id in group_objs:
                self.canvas.addtag_withtag(obj_id)

            # Unhighlight and clear selected objects
            self.unhighlight_objs()
            self.selected_objs = []

    def mainloop(self):
        self.root.mainloop()


root = tk.Tk()
app = DrawingApp(root)
app.mainloop()

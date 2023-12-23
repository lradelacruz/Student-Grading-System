import dearpygui.dearpygui as dpg
import CRUD

crud = CRUD.CRUD('student_info')


def clickSaved(sender, app_data):
    name_data = dpg.get_value("student_name")
    course_data = dpg.get_value("student_course")
    year_data = dpg.get_value("student_year")
    prelim_data = dpg.get_value("student_prelim")
    midterm_data = dpg.get_value("student_midterm")
    final_data = dpg.get_value("student_final")
    remarks = getRemarks(prelim_data, midterm_data, final_data)

    student_data = (name_data, course_data, year_data, prelim_data, midterm_data, final_data, remarks)
    crud.createRow(student_data)


def getRemarks(score1, score2, score3):
    total = score1 + score2 + score3
    avg = total / 3

    # if their scores ranges at 90-100
    if avg >= 90 and avg <= 100:
        return "A+"
    elif avg >= 80 and avg <= 89:
        return "A"
    elif avg >= 75 and avg <= 79:
        return "A-"
    elif avg >= 70 and avg <= 74:
        return "B+"
    elif avg >= 65 and avg <= 69:
        return "B"
    elif avg >= 60 and avg <= 64:
        return "B-"
    else:
        return "C"


# This function will clear the table of all the contents
def clear_table(table_tag):
    # delete headers
    dpg.delete_item("TAG-1")
    dpg.delete_item("TAG-2")
    dpg.delete_item("TAG-3")
    dpg.delete_item("TAG-4")
    dpg.delete_item("TAG-5")
    dpg.delete_item("TAG-6")
    dpg.delete_item("TAG-7")
    dpg.delete_item("TAG-8")
    dpg.delete_item("TAG-9")

    for tag in dpg.get_item_children(table_tag)[1]:
        dpg.delete_item(tag)


def dltStudent(sender, app_data, user_data):
    crud.deleteData(user_data)
    update_table('', '', user_data="datatable")


def update_table(sender, app_data, user_data):
    crud.recon()
    # parent is table tag
    parent = user_data
    # delete previous table data then recreate with new data
    clear_table(parent)

    # table headers
    dpg.add_table_column(label="ID", parent=parent, tag="TAG-1", width=20, width_fixed=True)
    dpg.add_table_column(label="NAME", parent=parent, tag="TAG-2")
    dpg.add_table_column(label="COURSE", parent=parent, tag="TAG-3")
    dpg.add_table_column(label="YEAR", parent=parent, tag="TAG-4")
    dpg.add_table_column(label="PRELIM", parent=parent, tag="TAG-5")
    dpg.add_table_column(label="MIDTERM", parent=parent, tag="TAG-6")
    dpg.add_table_column(label="FINALS", parent=parent, tag="TAG-7")
    dpg.add_table_column(label="REMARKS", parent=parent, tag="TAG-8")
    dpg.add_table_column(label="ACTION", parent=parent, tag="TAG-9")

    student = crud.getRows()

    for data_key, data_value in enumerate(student):
        with dpg.table_row(parent=parent):
            dpg.add_text(data_value[0])
            dpg.add_text(data_value[1])
            dpg.add_text(data_value[2])
            dpg.add_text(data_value[3])
            dpg.add_text(data_value[4])
            dpg.add_text(data_value[5])
            dpg.add_text(data_value[6])
            dpg.add_text(data_value[7])
            with dpg.group(horizontal=True):
                dpg.add_button(label="Delete", user_data=data_value[1], callback=dltStudent)


dpg.create_context()
dpg.create_viewport(width=980, height=500, title="Don Bosco Technical College", always_on_top=True, x_pos=400)
dpg.setup_dearpygui()

with dpg.font_registry():
    title_f = dpg.add_font("font\Freshman.ttf", 50)

with dpg.window(width=1000, height=1000, no_move=True, no_close=True, no_collapse=True, horizontal_scrollbar=True,
                pos=[0, 0], no_resize=True):
    with dpg.group(horizontal=True):
        header = dpg.add_text("DON BOSCO STUDENT RECORDS", color=[0, 230, 255], pos=[75, 25])

    dpg.add_table(tag="datatable")

    update_table("", "", user_data="datatable")
    dpg.add_button(label="SHOW", callback=update_table, user_data="datatable")

    dpg.add_text("Add Student in Records")
    dpg.add_text("Name")
    dpg.add_same_line()
    dpg.add_input_text(width=130, tag="student_name")
    dpg.add_same_line()
    dpg.add_text("Course")
    dpg.add_same_line()
    dpg.add_input_text(width=115, tag="student_course")
    dpg.add_same_line()
    dpg.add_text("Year")
    dpg.add_same_line()
    dpg.add_input_int(width=130, tag="student_year")
    dpg.add_text("PRELIM")
    dpg.add_same_line()
    dpg.add_input_int(width=70, tag="student_prelim")
    dpg.add_same_line()
    dpg.add_text("MIDTERM")
    dpg.add_same_line()
    dpg.add_input_int(width=70, tag="student_midterm")
    dpg.add_same_line()
    dpg.add_text("FINALS")
    dpg.add_same_line()
    dpg.add_input_int(width=70, tag="student_final")

    dpg.add_button(label="INSERT", callback=clickSaved)

    dpg.bind_item_font(header, title_f)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

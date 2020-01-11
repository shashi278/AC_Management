#####pip install fpdf2

from fpdf import FPDF
import os
import platform
import subprocess


class PDF(FPDF):
    def header(self):
        # Logo
        add_x=0
        add_y=0
        if self.cur_orientation=="P":
            add_x=0
            add_y=0
        else:
            add_x=50
        self.image("media/images/logo.png", 10+add_x, 8, 33)
        self.set_x(10+add_x)
        self.set_font("Arial", "B", 14)
        self.cell(93)
        self.cell(
            30, 10, "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY,KALYANI", 0, 0, "C"
        )

        self.ln(8)  # used to give vertical space of box
        self.cell(38+add_x)  # used to give horizontal space from left side
        self.set_font("Arial", "", 11)

        self.multi_cell(
            0,
            5.5,
            "(Autonomous insitution under MHRD,Govt. of India & Department of\n\
		Information Technology & ELectronics ,Govt. of West Bengal)\n c/o WEBEL IT Park,Opposite of Kalyani Water Treatment Plant\n\
		Near Buddha Park Dist. Nadia P.O Kalyani PIN-741235,West Bengal\nEmail-office@iiitkalyani.ac.in, website- www.iiitkalyani.ac.in",
            0,
            0,
            "C",
        )

        self.set_draw_color(0, 1, 1)
        self.line(10+add_x, 50, 200+add_x, 50)
        self.ln(5)

    # Page footer
    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")
        self.set_xy(-55,-20)
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "Signature of Accountant ", 0, 0, "L")


def show_doc(file_path):
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Linux":
            subprocess.call(["xdg-open", file_path])
    except PermissionError:
        from kivymd.uix.snackbar import Snackbar

        Snackbar(text="File is already opened!", duration=1.5).show()


def generate_pdf(personalinfo, feeinfo, dir):

    # if dir is not provided then it will be saved at desktop in Fee Reciepts Folder
    if dir == None:
        if platform.system() == "Windows":
            desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            if not os.path.exists(desktop + "/Fee Reciepts"):
                os.mkdir(desktop + "/Fee Reciepts")
                dir = desktop + "/Fee Reciepts"
            else:
                dir = desktop + "/Fee Reciepts"
        elif platform.system() == "Linux":
            desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
            if not os.path.exists(desktop + "/Fee Reciepts"):
                os.mkdir(desktop + "/Fee Reciepts")
                dir = desktop + "/Fee Reciepts"
            else:
                dir = desktop + "/Fee Reciepts"
    # Instantiation of inherited class

    pdf = PDF("L","mm","A4")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 5, "Fee Details", 0, 1, "C")

    pdf.ln(9)
    pdf.set_font("Times", "B", 12)

    pdf.cell(35,10,"Name: "+personalinfo["name"])
    pdf.ln(7)
    pdf.cell(50,10,"Reg No: "+personalinfo["reg"],0,0,"L")
    pdf.set_x(-50)
    pdf.cell(35,10,"Batch: "+personalinfo["batch"])
    pdf.set_x(10)
    pdf.ln(7)
    pdf.cell(35,10,"Course & Stream: "+personalinfo["course"]+"("+personalinfo["stream"]+")",0,0)
    pdf.set_x(-50)
    pdf.cell(35,10,"Tution Fee: "+personalinfo["fee"],0,1)
    pdf.set_x(10)

    pdf.ln(6)
    pdf.set_font("Times", "B", 13)
    pdf.cell(
        278,
        9,
        "  Semester          Total Paid                   Due                   Late Fine\
            Instalment                  Date                                      Trans. id",
        1,
    )

    # Data of Semesters
    pdf.cell(-140)
    pdf.ln(10)
    page_no=1
    for info in feeinfo:
        fee_len=len(info["fee"])
        pdf.cell(25, fee_len*9, info["sem"], 1, 0, "C")
        pdf.cell(36, fee_len*9, info["paid"], 1, 0, "C")
        pdf.cell(36, fee_len*9, info["due"], 1, 0, "C")
        pdf.cell(32, fee_len*9, info["late"], 1, 0, "C")
        for each in info["fee"]:
            pdf.cell(37,9,each["ppaid"],1,0,"C")
            pdf.cell(37, 9,each["date"], 1, 0, "C")
            pdf.cell(
                75,
                9,
                each["tid"] ,
                1,
                2,
                "C",
            )
            pdf.cell(-74,-9)
            page_no=pdf.page_no()
        pdf.ln(fee_len*9)
        if pdf.page_no()==page_no:
            pdf.ln(-(fee_len*9))

    pdf.set_y(-30)
    pdf.cell(0, 10, "Singnature of Accountant", 0, 0, "R")

    if not os.path.exists(dir + "/Students"):
        os.mkdir(dir + "/Students")
    filepath_and_name = dir + "/Students/" + personalinfo["reg"] + ".pdf"
    pdf.output(filepath_and_name, "F")
    show_doc(filepath_and_name)


def generate_batch_fee_pdf(basic_details, students_fee_data, dir):

    # if dir is not provided then it will be saved at desktop in Fee Reciepts Folder
    if dir == None:
        if platform.system() == "Windows":
            desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
            if not os.path.exists(desktop + "/Fee Reciepts"):
                os.mkdir(desktop + "/Fee Reciepts")
                dir = desktop + "/Fee Reciepts"
            else:
                dir = desktop + "/Fee Reciepts"
        elif platform.system() == "Linux":
            desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
            if not os.path.exists(desktop + "/Fee Reciepts"):
                os.mkdir(desktop + "/Fee Reciepts")
                dir = desktop + "/Fee Reciepts"
            else:
                dir = desktop + "/Fee Reciepts"

    pdf = PDF("P","mm","A4")
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Times", "B", 15)
    pdf.cell(0, 5, "Batch Fee Details", 0, 1, "C")

    pdf.ln(10)
    pdf.set_font("Times", "B", 12)

    pdf.multi_cell(
        0.0,
        7.0,
        "Semester: "
        + basic_details["sem"]
        + "                                                                             \
	                                            Batch: "
        + basic_details["batch"]
        + "\nCourse & Stream: "
        + basic_details["course"]
        + "("
        + basic_details["stream"]
        + (")" if basic_details["course"] == "B.Tech" else ")     ")
        + "                                                                              \
        Category: "
        + basic_details["due"],
    )

    pdf.ln(10)

    pdf.cell(
        188,
        9,
        "           Reg. No.            \
                    Name                    \
                    Paid                \
                    Due ",
        1,
    )
    pdf.ln(10)
    for student in students_fee_data:
        pdf.cell(40, 10, student["reg"], 1, 0, "C")
        pdf.cell(60, 10, student["name"], 1, 0, "C")
        pdf.cell(41, 10, student["paid"], 1, 0, "C")
        pdf.cell(47, 10, student["due"], 1, 0, "C")
        pdf.ln(10)

    if not os.path.exists(dir + "/Batch"):
        os.mkdir(dir + "/Batch")

    filepath_and_name = (
        dir
        + "/Batch/"
        + basic_details["batch"]
        + "_"
        + basic_details["course"]
        + basic_details["stream"]
        + "_Sem-"
        + basic_details["sem"]
        + ".pdf"
    )

    pdf.output(
        filepath_and_name, "F",
    )

    show_doc(filepath_and_name)


if __name__ == "__main__":

    fee_info = [
        {
            "sem": "1",
            "paid": "94700",
            "due": "1000",
            "late": "1000",
            "fee":[
                    
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345HHHHHHH",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "2",
            "paid": "94500",
            "due": "200",
            "late": "1000",
            "fee":[
                    
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "3",
            "paid": "93700",
            "due": "1000",
            "late": "0",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "4",
            "paid": "64700",
            "due": "0",
            "late": "0",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "5",
            "paid": "94700",
            "due": "1000",
            "late": "0",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    
                ],
        },
        {
            "sem": "7",
            "paid": "91730",
            "due": "1000",
            "late": "1000",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "8",
            "paid": "14500",
            "due": "1000",
            "late": "1000",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "9",
            "paid": "94700",
            "due": "1000",
            "late": "0",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "10",
            "paid": "64700",
            "due": "1000",
            "late": "0",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "11",
            "paid": "91730",
            "due": "1000",
            "late": "1000",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
        {
            "sem": "12",
            "paid": "14500",
            "due": "1000",
            "late": "1000",
            "fee":[
                    {
                        "ppaid":"20000",
                        "date": "22-12-2012",
                        "tid": "SVBNJGF4355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2014",
                        "tid": "XKJKTF55434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "10-11-2010",
                        "tid": "IOJ454355434512345",
                    },
                    {
                        "ppaid":"20000",
                        "date": "12-12-2017",
                        "tid": "GHHTG454355434512345",
                    },
                ],
        },
    ]

    personal_info = {
        "name": "N.R. Subramanyam",
        "reg": "213",
        "batch": "2017-2021",
        "course": "B.Tech",
        "stream": "CSE",
        "fee": "947000",
    }




    generate_pdf(personal_info, fee_info, None)


    batch_details = {
        "batch": "2017-2021",
        "course": "Ph.D",
        "stream": "CSE",
        "sem": "1",
        "due": "All",
    }
    students_fee_data = [
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
        {"reg": "214", "name": "Willi. M. Jonson", "paid": "97400", "due": "0",},
        {"reg": "278", "name": "Kate Richard", "paid": "80400", "due": "13000",},
        {"reg": "213", "name": "H. Watson", "paid": "87400", "due": "6000",},
    ]
    generate_batch_fee_pdf(batch_details, students_fee_data, None)

#####pip install fpdf2

from fpdf import FPDF
import os
import platform

class PDF(FPDF):
    def header(self): 
        # Logo
        self.image("media/images/logo.png", 10, 8, 33)

        self.set_font("Arial", "B", 14)
        self.cell(93)
        self.cell(
            30, 10, "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY,KALYANI", 0, 0, "C"
        )

        self.ln(8)  # used to give vertical space of box
        self.cell(40)  # used to give horizontal space from left side
        self.set_font("Arial", "", 11)

        self.multi_cell(
            0.0,
            5.5,
            "(Autonomous insitution under MHRD,Govt. of India & Department of\n\
		Information Technology & ELectronics ,Govt. of West Bengal)\n c/o WEBEL IT Park,Opposite of Kalyani Water Treatment Plant\n\
		Near Buddha Park Dist. Nadia P.O Kalyani PIN-741235,West Bengal\nEmail-office@iiitkalyani.ac.in, website- www.iiitkalyani.ac.in",
            0,
            0,
            "C",
        )

        self.set_draw_color(0, 1, 1)
        self.line(10, 50, 200, 50)
        self.ln(13)

    # Page footer
    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


def generate_pdf(personalinfo, feeinfo,dir):

    #if dir is not provided then it will saved at desktop in Fee Reciepts Folder 
    if dir==None:
        if platform.system()=="Windows":
            desktop= os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            if(not os.path.exists(desktop+"/Fee Reciepts")):
                os.mkdir(desktop+"/Fee Reciepts")
                dir= desktop+"/Fee Reciepts"
            else:
                dir= desktop+"/Fee Reciepts"
        elif platform.system()=="Linux":
            desktop= os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            if(not os.path.exists(desktop+"/Fee Reciepts")):
                os.mkdir(desktop+"/Fee Reciepts")
                dir= desktop+"/Fee Reciepts"
            else:
                dir= desktop+"/Fee Reciepts"
    # Instantiation of inherited class

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 5, "Fee Details", 0, 1, "C")

    pdf.ln(9)
    pdf.set_font("Times", "B", 12)
    
    print("\n\n\n\nI'm from generate_pdf_1\n\n\n")
    print(personalinfo)
    pdf.multi_cell(
        0.0,
        7.0,
        "Name: "
        + personalinfo["name"]
        + "\nReg No: "
        + personalinfo["reg"]
        + "                                                                             \
	                                             Batch: "
        + personalinfo["batch"]
        + "\nCourse & Stream: "
        + personalinfo["course"]
        + "("
        + personalinfo["stream"]
        + (")   " if personalinfo["course"]=="B.Tech" else ")     ")
        + "                                                                                    \
		Tution Fee: "
        + personalinfo["fee"],
    )

    pdf.ln(10)
    pdf.set_font("Times", "B", 13)
    pdf.cell(
        192,
        9,
        "  Semester            Paid                    Due              Late Fine             Date                         Tid",
        1,
    )

    # Data of Semesters
    pdf.cell(-140)
    pdf.ln(10)
    for info in feeinfo:
        pdf.cell(25, 10, info["sem"], 1, 0, "C")
        pdf.cell(31, 10, info["paid"], 1, 0, "C")
        pdf.cell(31, 10, info["due"], 1, 0, "C")
        pdf.cell(27, 10, info["late"], 1, 0, "C")
        pdf.cell(32, 10, info["date"], 1, 0, "C")
        pdf.cell(46, 10, info["tid"] if len(info["tid"])<=18 else (info["tid"])[:13]+"..." , 1, 0, "C")
        pdf.ln(10)

    pdf.set_y(-35)
    pdf.cell(0, 10, "Singnature of Accountant", 0, 0, "R")

    if(not os.path.exists(dir+"/Students")):
        os.mkdir(dir+"/Students")

    pdf.output(dir+"/Students/"+personalinfo["reg"] + ".pdf", "F")



def generate_batch_fee_pdf(basic_details,students_fee_data,dir):

    #if dir is not provided then it will saved at desktop in Fee Reciepts Folder 
    if dir==None:
        if platform.system()=="Windows":
            desktop= os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            if(not os.path.exists(desktop+"/Fee Reciepts")):
                os.mkdir(desktop+"/Fee Reciepts")
                dir= desktop+"/Fee Reciepts"
            else:
                dir= desktop+"/Fee Reciepts"
        elif platform.system()=="Linux":
            desktop= os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            if(not os.path.exists(desktop+"/Fee Reciepts")):
                os.mkdir(desktop+"/Fee Reciepts")
                dir= desktop+"/Fee Reciepts"
            else:
                dir= desktop+"/Fee Reciepts"

    pdf = PDF()
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
        + (")" if basic_details["course"]=="B.Tech" else ")     ")
        +"                                                                              \
        Category: "
        + basic_details["due"]
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


    if(not os.path.exists(dir+"/Batch")):
        os.mkdir(dir+"/Batch")


    pdf.output(dir+"/Batch/"+\
                basic_details["batch"]+"_"+\
               basic_details["course"]+\
               basic_details["stream"]+"_Sem-"+\
               basic_details["sem"]+".pdf", "F")
                        


if __name__ == "__main__":
    fee_info = [
        {
            "sem": "1",
            "paid": "94700",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2017",
            "tid": "STG454355434512345",
        },
        {
            "sem": "2",
            "paid": "94500",
            "due": "200",
            "late": "1000",
            "date": "12-12-2018",
            "tid": "QAG45453DSDFSDFSDFSDFSD",
        },
        {
            "sem": "3",
            "paid": "93700",
            "due": "1000",
            "late": "0",
            "date": "12-12-2019",
            "tid": "SAG4745",
        },
        {
            "sem": "4",
            "paid": "64700",
            "due": "0",
            "late": "0",
            "date": "12-12-2020",
            "tid": "SAG4545",
        },
        {
            "sem": "5",
            "paid": "94700",
            "due": "1000",
            "late": "0",
            "date": "12-12-2021",
            "tid": "SAG4555",
        },
        {
            "sem": "6",
            "paid": "64700",
            "due": "1000",
            "late": "0",
            "date": "12-12-2021",
            "tid": "SAJ4545",
        },
        {
            "sem": "7",
            "paid": "91730",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2015",
            "tid": "SAG4545",
        },
        {
            "sem": "8",
            "paid": "14500",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2019",
            "tid": "LAG4545",
        },
        {
            "sem": "9",
            "paid": "94700",
            "due": "1000",
            "late": "0",
            "date": "12-12-2021",
            "tid": "SAG4555",
        },
        {
            "sem": "10",
            "paid": "64700",
            "due": "1000",
            "late": "0",
            "date": "12-12-2021",
            "tid": "SAJ4545",
        },
        {
            "sem": "11",
            "paid": "91730",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2015",
            "tid": "SAG4545",
        },
        {
            "sem": "12",
            "paid": "14500",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2019",
            "tid": "LAG4545",
        },
        
    ]
    personal_info = {
        "name": "Anand Kumar",
        "reg": "213",
        "batch": "2017-2021",
        "course": "B.Tech",
        "stream": "CSE",
        "fee": "947000",
    }
    generate_pdf(personal_info, fee_info,None)

    batch_details= {
        "batch":"2017-2021",
        "course":"Ph.D",
        "stream":"CSE",
        "sem":"1",
        "due":"947000",
    }
    students_fee_data= [
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        {
        "reg":"214",
        "name":"Anish kumar Kharwar",
        "paid":"97400",
        "due":"0",
        },
        {
        "reg":"278",
        "name":"Shashi Ranjan",
        "paid":"80400",
        "due":"13000",
        },
        {
        "reg":"213",
        "name":"Anand kumar",
        "paid":"87400",
        "due":"6000",
        },
        
    ]
    generate_batch_fee_pdf(batch_details,students_fee_data,None)

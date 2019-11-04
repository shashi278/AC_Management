#####pip install fpdf2

from fpdf import FPDF


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
        self.ln(30)

    # Page footer
    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


def generate_pdf(personalinfo, feeinfo):
    # Instantiation of inherited class

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 5, "Fee Details", 0, 1, "C")

    

    pdf.ln(1)
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
        + (")" if personalinfo["course"]=="B.TECH" else ")     ")
        + "                                                                                    \
		Tution Fee: "
        + personalinfo["fee"],
    )

    print("\n\n\n\nI'm from generate_pdf_2\n\n\n")

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
        pdf.cell(25, 14, info["sem"], 1, 0, "C")
        pdf.cell(31, 14, info["paid"], 1, 0, "C")
        pdf.cell(31, 14, info["due"], 1, 0, "C")
        pdf.cell(27, 14, info["late"], 1, 0, "C")
        pdf.cell(32, 14, info["date"], 1, 0, "C")
        pdf.cell(46, 14, info["tid"], 1, 0, "C")
        pdf.ln(14)

    pdf.set_y(-35)
    pdf.cell(0, 10, "Singnature of Accountant", 0, 0, "R")
    pdf.output(personalinfo["reg"] + ".pdf", "F")

    


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
            "tid": "QAG4545",
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
            "paid": "67740",
            "due": "1000",
            "late": "1000",
            "date": "12-12-2019",
            "tid": "SAH4545",
        },
    ]
    personal_info = {
        "name": "Anand Kumar",
        "reg": "213",
        "batch": "2017-2021",
        "course": "B.TECH",
        "stream": "CSE",
        "fee": "94700",
    }
    generate_pdf(personal_info, fee_info)

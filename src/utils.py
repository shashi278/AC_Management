import os
import shutil

def move_doc(ins):
    """
    This function saves a copy of
    documents in the source folder
    
    :params ins: Instance of a kivy widget to get doc_path from
    """
    if not os.path.exists("documents/"):
        os.makedirs("documents/")

    for each in ins.ids.multipleDataContainer.children:
        if each.doc_path != "":
            extension = os.path.splitext(each.doc_path)[1]
            shutil.copy(each.doc_path, "documents/" + each.ids.tid.text + extension)
    
def rename_doc(prev_tid, curr_tid, ext):
    """
    This function renames a doc
    incase tid is updated
    
    :params prev_tid: previous txn id
    :params curr_tid: current txn id
    :params ext: file extension
    """
    if os.path.exists("documents/"+prev_tid+"."+ext):
        os.rename("documents/"+prev_tid+"."+ext,"documents/"+curr_tid+"."+ext)

def delete_doc(tid, ext):
    if os.path.exists("documents/"+tid+"."+ext):
        os.remove("documents/"+tid+"."+ext)

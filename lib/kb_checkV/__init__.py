"""
This script includes function called in kb_checkVImlp.py
"""
import os
import json
import csv
import subprocess
import uuid
import zipfile
from shutil import copytree
from html import escape

def generate_output_file_list(result_directory, shared_folder):
    """
    generate_output_file_list: zip result files and generate file_links for report
    """
    output_files = list()
    output_directory = os.path.join(shared_folder, str(uuid.uuid4()))
    os.mkdir(output_directory)
    result_file = os.path.join(output_directory, 'checkv_result.zip')
    with zipfile.ZipFile(result_file, 'w',
                         zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zip_file:
        for root, dirs, files in os.walk(result_directory):
            for file in files:
                if not (file.endswith('.zip') or
                        file.endswith('.png') or
                        file.endswith('.DS_Store')):
                    zip_file.write(os.path.join(root, file),
                                   os.path.join(os.path.basename(root), file))
    output_files.append({'path': result_file,
                         'name': os.path.basename(result_file),
                         'label': os.path.basename(result_file),
                         'description': 'File(s) generated by CheckV App'})
    return output_files

def tsv_to_json(result_directory):
    """
    This function converts tsv file to json file
    :param result_directory: output directory of checkv end_to_end command,
            includs all output tsv files
    :param shared_folder: kbase working scratch folder: /kb/module/work/tmp
    """
    json_files_directory = os.path.join("/opt/work/", "json_files_dir")
    os.mkdir(json_files_directory)
    for file in os.listdir(result_directory):
        if file.endswith(".tsv"):
            json_file_path = os.path.join(json_files_directory, file + ".json")
            # write tsv file to json file
            tsv_file_path = os.path.join(result_directory, file)
            with open(tsv_file_path) as tsv_file:
                reader = csv.DictReader(tsv_file, delimiter="\t")
                data = list(reader)
                res = {"data": data}
                with open(json_file_path, "w") as jsonfile:
                    json.dump(res, jsonfile)
    return json_files_directory


def read_template(template_file):
    """
    read in a template file and escape all html content
    used to display template contents
    """

    with open(template_file) as file:
        lines = file.read()

    # escape all the html, display the results
    escaped_lines = escape(lines, quote=True)

    return escaped_lines


def generate_template_report(result_directory, shared_folder, report_client):
    """
    This function
    :param shared_folder: kbase working scratch folder: /kb/module/work/tmp
    :param dfu: DataFileUtil clint
    :return:html_links: a list containing html report parmas
    """
    # create output_report_directory to store output report
    output_report_directory = os.path.join(shared_folder, "output_report_directory")
    os.mkdir(output_report_directory)
    report_file = "CheckV_report.html"

    # copy the template file to scratch directory
    copytree(
        os.path.join("/kb/module", "template"), os.path.join(shared_folder, "template")
    )

    template_file = os.path.join(shared_folder, "template", "checkv.tt")

    # convert tsv to json
    json_files_directory = tsv_to_json(result_directory)
    report_description = "HTML report with four tabs for CheckV"
    tmpl_data = {}

    tmpl_data["tmpl_vars"] = json.dumps(tmpl_data, sort_keys=True, indent=2)
    tmpl_data["template_content"] = read_template(template_file)

    report_client.render_template(
        {
            "template_file": template_file,
            "template_data_json": json.dumps(tmpl_data),
            "output_file": os.path.join(output_report_directory, report_file),
        }
    )

    copytree(json_files_directory, os.path.join(output_report_directory, "data"))

    html_links = [
        {
            "path": output_report_directory,
            "name": report_file,
            "description": report_description,
        }
    ]
    return html_links


def run_command(command):
    """
    This function takes command and run it with subprocess.Popen
    and print out the process in real time
    :param command: command, for example:
            ['checkv', 'end_to_end', fasta_file, output_dir, '-t', '16']
    :return: return code after execution
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, encoding="utf8")
    while True:
        output = process.stdout.readline()
        if output == "" and (process.poll() is not None):
            break
        if output:
            print(output.strip())
    return_code = process.poll()
    return return_code


def run_kb_checkv(fasta_file):
    """
    This function run CheckV command on input fasta_file
    :param fasta_file: path to Fasta_file
    :return: output directory where checkv output tsv files are stored
    """
    os.environ["CHECKVDB"] = "/data/checkv-db-v0.6"
    output_dir = "/opt/work/outputdir"
    run_command(["checkv", "end_to_end", fasta_file, output_dir, "-t", "16", "--restart"])
    return output_dir

# -*- coding: utf-8 -*-

import platform
from pathlib import Path
import PySimpleGUI as sg


#import images
images_dir = Path(__file__).absolute().parents[1] / 'images'

if platform.system() == 'Windows':
    import win32com.client
    icon = r'{}\{}'.format(images_dir, 'logo.ico')
elif platform.system() == 'Linux':
    import subprocess
    icon = '@{}/{}'.format(images_dir, 'logo.xbm')
else:
    raise RuntimeError('Unsupported OS {}.'.format(platform.system()))
    
    
# convert WORD file to pdf
def doc_to_pdf(input_file, output_path=None):
    
    input_file = Path(input_file)
    
    if output_path:
        output_path = Path(output_path)
    else:
        output_path = input_file.parent

    if not input_file.is_file():
        raise FileNotFoundError()
        
    output_path.mkdir(exist_ok=True)
    output_file = output_path / input_file.with_suffix('.pdf').name
    
    if platform.system() == 'Windows':
        word = win32com.client.Dispatch('Word.Application')
        doc = word.Documents.Open(str(input_file.absolute()))
        doc.SaveAs(str(output_file.absolute()), FileFormat=17)
        doc.Close()
        word.Quit()
    elif platform.system() == 'Linux':
        cmd = 'libreoffice --headless --convert-to pdf "{}"'.format(input_file)
        if output_path:
            cmd += ' --outdir "{}"'.format(output_path)

        p = subprocess.Popen(cmd, shell=True)   
        stdout, stderr = p.communicate()
        if stderr:
            raise subprocess.SubprocessError(stderr)
    else:
        raise RuntimeError('Unsupported OS {}.'.format(platform.system()))
        sg.Popup(
                'Cancelled',
                'Word files are not supported on {} yet.'.format(platform.system()),
                icon=icon
                )
        
    return output_file 
import os
import map_reader

def createStagesMatrixes():
    images = os.listdir('/Study/Sistemas inteligentes/diamond-rush-inteligente/lvls')
    for image in images:
        matrix = map_reader.read_image('/Study/Sistemas inteligentes/diamond-rush-inteligente/lvls/' + image)
       
        file1 = open("/Study/Sistemas inteligentes/diamond-rush-inteligente/levels.py", "a")
       
        file1.write(image.split('.')[0] + '= [ \n')
        for row in matrix:
            file1.write('[' +  ', '.join([str(a) for a in row])  + '],\n')
        
        file1.write('] \n \n')
        file1.close() 

createStagesMatrixes()
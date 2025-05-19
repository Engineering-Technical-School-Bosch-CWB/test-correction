import xlwings as xw

def readExcelNome(file):
    wb = xw.Book(file)
    records_tab = wb.sheets['Registros']
    names = records_tab.range('A2').expand('down').value

    return names


def findCandidate(candidate, file):
    names = readExcelNome(file)
    exists = True

    index_value = names.index(candidate) + 2
        
    return exists, index_value


"""
Diferença entre as duas funções de leitura do gabarito: 
Enquanto a função básica lê apenas um gabarito, a função avançada lê todos os 
gabaritos da planilha e retorna o selecionado de acordo com o parâmetro passado.
"""

def readExcelGabarito(file):
    wb = xw.Book(file)
    answers_tab = wb.sheets['Gabarito']

    score = answers_tab.range('A2').expand('down').value
    question_number = answers_tab.range('B2').expand('down').value

    answers_data = wb.sheets['Gabarito'].used_range

    answers = []
    for j in range(len(question_number)):
        answers.append((j+1, answers_data.value[j+1][2]))

    return answers, score


def readExcelGabarito_advanced(file, test):
    wb = xw.Book(file)
    answers_tab = wb.sheets['Gabaritos']

    score = answers_tab.range('A2').expand('down').value
    question_number = answers_tab.range('B2').expand('down').value

    answers_data = wb.sheets['Gabaritos'].used_range
    different_tests = len(answers_data.value[0]) - 2

    answers = []
    for i in range(different_tests):
        answers.append([])
        for j in range(len(question_number)):
            answers[i].append((j+1, answers_data.value[j+1][i+2]))

    return answers[test], score


def registerCandidate(candidate, race, answers, grade, answersWithOptions, file):
    wb = xw.Book(file)
    records_tab = wb.sheets['Registros']
    exists, line = findCandidate(candidate)

    records_tab.cells(line, 2).value = grade

    _option = ['a','b','c','d','e']
    _answers = []
    for i in range(20):
        added = False
        for j in range(5):
            if answersWithOptions[i][j] != 0:
                _answers.append(_option[j])
                added = True
                break
        if(not added):
            _answers.append("-")

    for i in range(len(_answers)):
        records_tab.cells(line, i+2).value = _answers[i]

    wb.save()
    
    return "Success", 200

var candidateName = document.querySelector("#candidateName");

function _getGrade()
{
    console.log('getGradeeeee')

    let grade = 0;
    var answers = [];
    let questionsPoints = []

    $.ajax({
        url: '/questionsValues',
        type: 'GET',
        datatype: "json",
        async: false,
        success: function(response) {
            questionsPoints = response
        },
        error: function() {
            alert("Erro: gabarito não carregado!!!")
        }
    });

    var questionsCheckboxes = document.getElementsByName('questionCheckBox');
    questionsCheckboxes.forEach((item) => {
        if (item.checked == true)
        {
            answers.push(1);
            let question = (item.id).replace("question", "");
            grade += questionsPoints[parseInt(question) - 1];
        }
        else
            answers.push(0)
    })

    return [grade, answers];
}

function cleanOptions()
{
    candidateName.innerHTML = "Selecione o Candidato";
    var checkboxes = document.getElementsByName('checkBox')
    checkboxes.forEach((item) => {
        if (item.checked == true)
        {
            item.checked = false;
        }
    });

    cleanQuestionCheckboxes();
}

function cleanQuestionCheckboxes()
{
    var questionCheckboxes = document.getElementsByName("questionCheckBox");
    questionCheckboxes.forEach((item) => {
        item.checked = false;
    });
}


function insertData(exists)
{
    var results = _getGrade();

    $.ajax({
        url: '/register',
        type: 'POST',
        data: {
            'candidate': candidateName.innerHTML,
            'grade': results[0],
            'answers': results[1].join('')
        },
        success: function()
        {
            if (exists)
                alert("Registro alterado");
            else
                alert("Candidato registrado")
            cleanOptions()
            cleanQuestionCheckboxes()
        },
        error: function(e)
        {
            alert(e)
        }
    });
}


function register()
{

    if (candidateName.innerHTML != 'Selecione o Candidato')
    {
        $.ajax({
            url: '/candidate',
            type: 'GET',
            data : {'candidate':candidateName.innerHTML},
            success: function()
            {
                insertData(true)
            },
            error: function(){
                insertData(false)
            }
        });
    }
    else
        alert("Termine de preencher as informações do candidato");
}
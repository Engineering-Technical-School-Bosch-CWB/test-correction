import { initializeApp } from "https://www.gstatic.com/firebasejs/9.21.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.21.0/firebase-analytics.js";

const firebaseConfig = {
    apiKey: "AIzaSyAdCH7JMVFTZ0qpFn97UK7iOsiOiKsrDBs",
    authDomain: "processoseletivoets.firebaseapp.com",
    databaseURL: "https://processoseletivoets-default-rtdb.firebaseio.com",
    projectId: "processoseletivoets",
    storageBucket: "processoseletivoets.appspot.com",
    messagingSenderId: "742447715808",
    appId: "1:742447715808:web:418f80cfe2b62e9561c785",
    measurementId: "G-2XG8SGQFHB"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

import {getDatabase, set, get, update, remove, ref, child} 
from "https://www.gstatic.com/firebasejs/9.21.0/firebase-database.js";

const db = getDatabase();

var candidateName = document.querySelector("#candidateName");

function getGrade()
{
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

function getActiveRace()
{
    let raceChecked = "none"
    var checkboxes = document.getElementsByName('checkBox')
    checkboxes.forEach((item) => {
        if (item.checked == true)
        {
            raceChecked = item.id;
        }
    });
    
    return raceChecked
}

function insertData()
{	
    let candidateRace = getActiveRace();
    var grade = getGrade();

    if (candidateRace != "none" && candidateName.innerHTML != 'Selecione o Candidato')
    {
        set(ref(db, "Candidates/" + candidateName.innerHTML), {
            Nome: candidateName.innerHTML,
            Identificação: candidateRace,
            Nota: grade[0],
            Questao1: grade[1][0],
            Questao2: grade[1][1],
            Questao3: grade[1][2],
            Questao4: grade[1][3],
            Questao5: grade[1][4],
            Questao6: grade[1][5],
            Questao7: grade[1][6],
            Questao8: grade[1][7],
            Questao9: grade[1][8],
            Questao10: grade[1][9],
            Questao11: grade[1][10],
            Questao12: grade[1][11],
            Questao13: grade[1][12],
            Questao14: grade[1][13],
            Questao15: grade[1][14],
            Questao16: grade[1][15],
            Questao17: grade[1][16],
            Questao18: grade[1][17],
            Questao19: grade[1][18],
            Questao20: grade[1][19]
        })
        .then(() => { alert("Candidato avaliado!") })
        .catch((error) => { alert(error) });
        cleanOptions();
    }
    else
        alert("Termine de preencher as informações do candidato");

}

function updateData()
{
    let candidateRace = getActiveRace();
    var grade = getGrade();
    if (candidateRace != "none" && candidateName.innerHTML != 'Selecione o Candidato')
    {
        update(ref(db, "Candidates/" + candidateName.innerHTML) , {
            Nome: candidateName.innerHTML,
            Identificação: candidateRace,
            Nota: grade[0],
            Questao1: grade[1][0],
            Questao2: grade[1][1],
            Questao3: grade[1][2],
            Questao4: grade[1][3],
            Questao5: grade[1][4],
            Questao6: grade[1][5],
            Questao7: grade[1][6],
            Questao8: grade[1][7],
            Questao9: grade[1][8],
            Questao10: grade[1][9],
            Questao11: grade[1][10],
            Questao12: grade[1][11],
            Questao13: grade[1][12],
            Questao14: grade[1][13],
            Questao15: grade[1][14],
            Questao16: grade[1][15],
            Questao17: grade[1][16],
            Questao18: grade[1][17],
            Questao19: grade[1][18],
            Questao20: grade[1][19]
        })
        .then( () => {
            alert("Registro de candidato alterado");
        })
        .catch((error) => {alert(error)});
        cleanOptions();
    }
    else
        alert("Termine de preencher as informações do candidato");
    
}

function register()
{
    const dbref = ref(db);
    get(child(dbref, "Candidates/" + candidateName.innerHTML))
    .then((snapshot) => {
        if (snapshot.exists())
            updateData();
        else 
            insertData();
    })
    .catch((error) => {
        alert(error)
    })
}

registerButton.addEventListener('click', register);
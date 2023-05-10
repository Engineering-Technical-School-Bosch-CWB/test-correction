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

    return grade, answers;
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
    let grade, answers = getGrade();
    if (candidateRace != "none" && candidateName.innerHTML != 'Selecione o Candidato')
    {
        set(ref(db, "Candidates/" + candidateName.innerHTML), {
            Nome: candidateName.innerHTML,
            Identificação: candidateRace,
            Nota: grade,
            Questao1: answers[0],
            Questao2: answers[1],
            Questao3: answers[2],
            Questao4: answers[3],
            Questao5: answers[4],
            Questao6: answers[5],
            Questao7: answers[6],
            Questao8: answers[7],
            Questao9: answers[8],
            Questao10: answers[9],
            Questao11: answers[10],
            Questao12: answers[11],
            Questao13: answers[12],
            Questao14: answers[13],
            Questao15: answers[14],
            Questao16: answers[15],
            Questao17: answers[16],
            Questao18: answers[17],
            Questao19: answers[18],
            Questao20: answers[19]
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
    let grade = getGrade();
    if (candidateRace != "none" && candidateName.innerHTML != 'Selecione o Candidato')
    {
        update(ref(db, "Candidates/" + candidateName.innerHTML) , {
            Nome: candidateName.innerHTML,
            Identificação: candidateRace,
            Nota: grade,
            Questao1: answers[0],
            Questao2: answers[1],
            Questao3: answers[2],
            Questao4: answers[3],
            Questao5: answers[4],
            Questao6: answers[5],
            Questao7: answers[6],
            Questao8: answers[7],
            Questao9: answers[8],
            Questao10: answers[9],
            Questao11: answers[10],
            Questao12: answers[11],
            Questao13: answers[12],
            Questao14: answers[13],
            Questao15: answers[14],
            Questao16: answers[15],
            Questao17: answers[16],
            Questao18: answers[17],
            Questao19: answers[18],
            Questao20: answers[19]
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
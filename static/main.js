let toggle = true;

let countries = []
let testAnswers = []


$.ajax({
    url: '/candidates',
    type: 'GET',
    datatype: "json",
    async: false,
    success: function(response) {
        countries = response
    }
});

$.ajax({
    url: '/getGabarito',
    type: 'GET',
    datatype: "json",
    async: false,
    success: function(response) {
        testAnswers = response
    }
});

let questions = document.getElementsByName("questionHtmlDiv");

for (let index = 0; index < testAnswers.length; index++) 
    questions[index].innerHTML = (index + 1) + " | " + testAnswers[index][1];

function search() {

    $.ajax({
        url: '/update_variable',
        type: 'GET',
        success: function(response) {
            if (response != "[]")
            {
                answersList = response.split('');
                var questionCheckboxes = document.getElementsByName("questionCheckBox");
                for (let i = 0; i < questionCheckboxes.length; i++)
                    if (answersList[i] == "1")
                        questionCheckboxes[i].checked = true;            
                    else 
                        questionCheckboxes[i].checked = false;
            }
        }
    });
    
}

// Checkboxes

function onlyOne(checkbox) {
    var myCheckboxes = document.getElementsByName('checkBox')
    myCheckboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}

// SearchBox

const wrapper = document.querySelector(".wrapper"),
selectBtn = wrapper.querySelector(".select-btn"),
searchInp = wrapper.querySelector("input"),
options = wrapper.querySelector(".options");

function addCandidate(selectedCandidate) {
    options.innerHTML = "";
    countries.forEach(candidate => {
        let isSelected = candidate == selectedCandidate ? "selected" : "";
        let li = `<li onclick="updateName(this)" class="${isSelected}">${candidate}</li>`;
        options.insertAdjacentHTML("beforeend", li);
    });
}
addCandidate();

function updateName(selectedLi) {
    searchInp.value = "";
    addCandidate(selectedLi.innerText);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
}

searchInp.addEventListener("keyup", () => {
    let arr = [];
    let searchWord = searchInp.value.toLowerCase();
    arr = countries.filter(data => {
        return data.toLowerCase().startsWith(searchWord);
    }).map(data => {
        let isSelected = data == selectBtn.firstElementChild.innerText ? "Selecionado" : "";
        return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
    }).join("");
    options.innerHTML = arr ? arr : `<p style="margin-top: 0.0vw;font-size: 2.0vw">Candidato não encontrado</p>`;
});

selectBtn.addEventListener("click", () => wrapper.classList.toggle("active"));
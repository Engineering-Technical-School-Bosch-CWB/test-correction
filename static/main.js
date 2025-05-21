
let toggle = true;

let countries = []
let testAnswers = []
let testsLabels = []


function loadData() {
    
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

    $.ajax({
        url: '/getTestsTitle',
        type: 'GET',
        datatype: "json",
        async: false,
        success: function(response) {
            testsLabels = response.templates

            try {
                addTestsTitle(response.templates, response.current)

            } catch (err) {
                console.error(err);
            }
        }
    })
    _getGrade()
    updateQuestionsCheckboxes()
}
loadData()


function selectTest(params) {
    
    $.ajax({
        url: '/selectTest',
        type: 'POST',
        data: JSON.stringify(params),
        contentType: "application/json",
        success: function()
        {
            loadData()
        },
        error: function(e)
        {
            alert(e)
        }
    })
}

function addTestsTitle(tests, current){
    var test_container = document.getElementById('select_test_radio')
    test_container.innerHTML = ""
    tests.forEach((option, index) => {
        var newOptionContainer = document.createElement('span');
        var newOption = document.createElement('input');
        newOption.setAttribute('type', 'radio');
        newOption.setAttribute('id', `test_title_${option}`);
        newOption.setAttribute('value', index);
        newOption.setAttribute('name', 'test_title');
        if(current == index)
            newOption.setAttribute('checked', true)
        newOption.onclick = () => {
            selectTest({index: index, value: option})
        }
        var newLabel = document.createElement('label')
        newLabel.setAttribute('for', `test_title_${option}`);
        newLabel.innerText = option
        newOptionContainer.appendChild(newOption)
        newOptionContainer.appendChild(newLabel)
        test_container.appendChild(newOptionContainer)
    });
}
function updateQuestionsCheckboxes() {
    let questions = document.getElementsByName("questionHtmlDiv");
    
    for (let index = 0; index < testAnswers.length; index++) 
        questions[index].innerHTML = (index + 1) + " | " + testAnswers[index][1];
}
updateQuestionsCheckboxes()

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
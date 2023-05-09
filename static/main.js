let toggle = true;

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

let countries = ["Maria Aparecida Silva","João Pedro Santos","Ana Luiza Oliveira","Lucas dos Santos Souza","Carla Fernanda Pereira","Rodrigo Almeida Costa","Larissa Lima Santos","Guilherme Castro Alves","Juliana de Souza Ferreira","Rafaela Nunes Cardoso","Pedro Henrique Rodrigues","Camila Vieira Gomes","Matheus Oliveira Martins","Isabela Silva Sousa","Thiago Ferreira Carvalho","Gabriela Costa Ribeiro","Fernando Alves Pereira","Bianca Santos Silva","Arthur Oliveira Lima","Amanda Castro Santos","Leonardo Carvalho Rodrigues","Giovanna Fernandes Souza","Ricardo Cardoso Nunes","Lívia Lima Almeida","Vinicius Pereira Gonçalves","Maria Clara Rodrigues Castro","Tiago Ferreira Almeida","Mariana Oliveira Costa","Diego Souza Ramos","Helena Martins Gomes","Luiz Henrique Silva Santos","Lara Nunes Oliveira","Renato Almeida Castro","Natália Costa Ferreira","Enzo Cardoso Sousa","Luana Ribeiro Carvalho","Daniel Pereira Alves","Gabrielle Santos Lima","Alexandre Rodrigues Castro","Leticia Ferreira Lima","Luciano Oliveira Santos","Sofia Sousa Almeida","Thales Gomes Pereira","Lorena Martins Silva","Júlio César Nunes Costa","Ana Beatriz Alves Rodrigues","Victor Hugo Souza Santos","Mariana Ferreira Oliveira","Lucas Cardoso Lima","Raquel Sousa Castro","Henrique Ribeiro Costa","Gabriela Almeida Carvalho","Felipe Santos Pereira","Carolina Lima Gomes","Pedro Castro Silva","Julia Rodrigues Oliveira","André Luiz Ferreira Santos","Isadora Costa Almeida","Matheus Nunes Sousa","Larissa Oliveira Ribeiro","Rafael Silva Martins","Beatriz Castro Lima","Rodrigo Souza Santos","Alice Carvalho Pereira","Leonardo Gomes Alves","Maria Eduarda Nunes Castro","Thiago Rodrigues Lima","Gabriela Costa Silva","Lucas Almeida Santos","Bianca Pereira Oliveira","Guilherme Lima Ferreira","Amanda Ribeiro Gomes","Luiz Felipe Martins Sousa","Vitória Santos Almeida","Rafaela Carvalho Costa","Gustavo Silva Rodrigues","Camila Castro Lima","Pedro Henrique Oliveira Santos","Mariana Ferreira Alves","Carlos Eduardo Lima Souza","Isabela Santos Costa","Ricardo Nunes Pereira","Lívia Almeida Rodrigues","Vinicius Castro Gomes"];

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
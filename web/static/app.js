
const gentesArr = [
['Acutia', 'pleb', 'Marcus', 'Lucius', 'Quintus', 'Gaius', 'Publius'],
['Aebutia', 'pat', 'Titus', 'Lucius', 'Postumus', 'Marcus'],
['Aelia', 'pleb', 'Publius', 'Sextus', 'Quintus', 'Lucius', 'Gaius'],
['Aemilia', 'pat', 'Lucius', 'Manius', 'Marcus', 'Quintus', 'Mamercus'],
['Albinia', 'pleb', 'Lucius', 'Gaius', 'Marcus'],
['Aliena', 'pleb', 'Lucius', 'Aulus'],
['Anicia', 'pleb', 'Lucius', 'Quintus', 'Marcus', 'Gnaeus', 'Titus', 'Gaius'],
['Annia', 'pleb', 'Titus', 'Marcus', 'Lucius', 'Gaius'],
['Antia', 'pleb', 'Spurius', 'Marcus', 'Gaius'],
['Antistia', 'pleb', 'Sextus', 'Lucius', 'Marcus'],
['Antonia', 'pat', 'Titus', 'Quintus', 'Lucius', 'Gaius', 'Aulus'],
['Appuleia', 'pleb', 'Lucius', 'Sextus', 'Gaius', 'Quintus'],
['Apronia', 'pleb', 'Gaius', 'Quintus', 'Lucius'],
['Aquilia', 'pat', 'Gaius', 'Lucius', 'Marcus'],
['Aternia', 'pat', 'Aulus'],
['Atilia', 'pat', 'Lucius', 'Marcus', 'Gaius', 'Aulus', 'Sextus'],
['Atinia', 'pleb', 'Titus', 'Gaius', 'Marcus'],
['Aulia', 'pleb', 'Quintus', 'Manius'],
['Caecilia', 'pleb', 'Lucius', 'Quintus', 'Gaius', 'Marcus', 'Titus'],
['Caedicia', 'pleb', 'Lucius', 'Gaius', 'Marcus', 'Quintus'],
['Calavia', 'pleb', 'Ovius', 'Ofilius', 'Novius', 'Pacuvius'],
['Canuleia', 'pleb', 'Gaius', 'Lucius', 'Marcus'],
['Cassia', 'pleb', 'Lucius', 'Gaius', 'Quintus', 'Spurius', 'Marcus'],
['Claudia', 'pat', 'Appius', 'Gaius', 'Publius', 'Tiberius', 'Marcus', 'Lucius'],
['Cloelia', 'pat', 'Titus', 'Quintus', 'Publius', 'Baius', 'Tullus'],
['Cominia', 'pleb', 'Postumus', 'Lucius', 'Sextus', 'Publius', 'Gaius', 'Quintus'],
['Cornelia', 'pat', 'Servius', 'Lucius', 'Publius', 'Gnaeus', 'Marcus', 'Gaius', 'Aulus', 'Tiberius', 'Faustus'],
['Decia', 'pleb', 'Marcus', 'Publius', 'Quintus'],
['Domitia', 'pleb', 'Gnaeus', 'Marcus', 'Lucius'],
['Duilia', 'pleb', 'Marcus', 'Caeso', 'Gaius'],
['Fabia', 'pat', 'Caeso', 'Quintus', 'Marcus', 'Numerius', 'Gaius'],
['Flavia', 'pleb', 'Marcus', 'Quintus', 'Gaius', 'Lucius', 'Titus'],
['Foslia', 'pat', 'Marcus', 'Gaius'],
['Fulcinia', 'pleb', 'Gaius', 'Marcus', 'Lucius'],
['Fulvia', 'pleb', 'Lucius', 'Marcus', 'Quintus', 'Gaius', 'Gnaeus', 'Servius'],
['Furia', 'pat', 'Lucius', 'Spurius', 'Publius', 'Marcus', 'Agrippa', 'Sextus', 'Quintus', 'Gaius'],
['Furnia', 'pleb', 'Gaius'],
['Gegania', 'pat', 'Titus', 'Lucius', 'Marcus', 'Proculus'],
['Genucia', 'pleb', 'Lucius', 'Titus', 'Marcus', 'Gnaeus'],
['Herminia', 'pat', 'Titus', 'Lars', 'Spurius', 'Lucius'],
['Horatia', 'pat', 'Publius', 'Marcus', 'Lucius', 'Gaius'],
['Hortensia', 'pleb', 'Quintus', 'Lucius', 'Marcus'],
['Hostilia', 'pleb', 'Aulus', 'Lucius', 'Gaius', 'Marcus', 'Publius', 'Hostus', 'Tullus'],
['Icilia', 'pleb', 'Spurius', 'Gaius', 'Lucius'],
['Iulia', 'pat', 'Lucius', 'Gaius', 'Sextus', 'Vopiscus', 'Spurius', 'Proculus'],
['Iunia', 'pleb', 'Marcus', 'Lucius', 'Decimus', 'Gaius', 'Quintus', 'Appius', 'Titus'],
['Iuventia', 'pleb', 'Titus', 'Lucius', 'Manius', 'Publius', 'Gaius', 'Marcus'],
['Laceria', 'pleb', 'Gaius', 'Quintus'],
['Laetoria', 'pleb', 'Marcus', 'Gaius', 'Lucius'],
['Lartia', 'pat', 'Titus', 'Spurius', 'Lucius', 'Aulus'],
['Lemonia', 'pleb', 'Lucius', 'Quintus', 'Gaius'],
['Licinia', 'pleb', 'Publius', 'Gaius', 'Lucius', 'Marcus', 'Sextus', 'Gnaeus', 'Aulus'],
['Livia', 'pleb', 'Marcus', 'Gaius', 'Lucius', 'Mamercus', 'Titus'],
['Lucretia', 'pat', 'Titus', 'Spurius', 'Lucius', 'Publius', 'Hostus', 'Opiter'],
['Maecilia', 'pleb', 'Lucius', 'Spurius', 'Marcus'],
['Maelia', 'pleb', 'Spurius', 'Gaius', 'Publius', 'Quintus'],
['Maenia', 'pleb', 'Gaius', 'Publius', 'Titus', 'Quintus'],
['Mamilia', 'pleb', 'Octavius', 'Lucius', 'Quintus', 'Gaius', 'Marcus'],
['Manilia', 'pleb', 'Sextus', 'Publius', 'Manius', 'Lucius', 'Gaius', 'Quintus', 'Marcus'],
['Manlia', 'pat', 'Publius', 'Gnaeus', 'Aulus', 'Lucius', 'Marcus', 'Titus', 'Aulus'],
['Marcia', 'pleb', 'Lucius', 'Gaius', 'Quintus', 'Publius', 'Marcus', 'Gnaeus', 'Septimus'],
['Menenia', 'pat', 'Agrippa', 'Gaius', 'Titus', 'Lucius', 'Licinus'],
['Metilia', 'pleb', 'Spurius', 'Marcus', 'Titus', 'Publius'],
['Minucia', 'pat', 'Marcus', 'Publius', 'Quintus', 'Lucius', 'Tiberius', 'Gaius', 'Spurius'],
['Mucia', 'pat', 'Publius', 'Quintus', 'Gaius'],
['Nautia', 'pat', 'Spurius', 'Gaius', 'Marcus', 'Gaius', 'Publius', 'Lucius', 'Quintus'],
['Numicia', 'pat', 'Titus', 'Tiberius', 'Publius', 'Gaius', 'Lucius', 'Marcus', 'Quintus'],
['Numisia', 'pleb', 'Lucius', 'Gaius', 'Titus', 'Publius'],
['Numitoria', 'pleb', 'Lucius', 'Publius', 'Gaius', 'Quintus'],
['Ogulnia', 'pleb', 'Quintus', 'Gnaeus', 'Lucius', 'Marcus', 'Numerius', 'Publius', 'Titus'],
['Oppia', 'pleb', 'Spurius', 'Marcus', 'Gaius', 'Lucius', 'Quintus', 'Publius'],
['Papiria', 'pat', 'Lucius', 'Marcus', 'Gaius', 'Manius', 'Spurius', 'Tiberius'],
['Petronia', 'pleb', 'Gaius', 'Marcus', 'Publius'],
['Pinaria', 'pat', 'Publius', 'Lucius', 'Mamercus'],
['Plautia', 'pleb', 'Lucius', 'Gaius', 'Publius', 'Marcus', 'Aulus', 'Quintus', 'Tiberius'],
['Poetelia', 'pleb', 'Quintus', 'Gaius', 'Marcus', 'Publius'],
['Pollia', 'pleb', 'Publius', 'Gaius', 'Marcus', 'Gnaeus', 'Lucius', 'Quintus', 'Numerius'],
['Pompilia', 'pleb', 'Mamercus', 'Sextus', 'Marcus'],
['Pomponia', 'pleb', 'Marcus', 'Lucius', 'Titus', 'Quintus', 'Publius', 'Sextus', 'Manius', 'Gaius', 'Gnaeus'],
['Pontia', 'pleb', 'Gaius', 'Titus', 'Lucius', 'Marcus'],
['Popillia', 'pleb', 'Marcus', 'Gaius', 'Publius', 'Titus', 'Quintus'],
['Postumia', 'pat', 'Aulus', 'Spurius', 'Lucius', 'Marcus', 'Publius', 'Quintus', 'Gaius', 'Gnaeus', 'Titus'],
['Potitia', 'pat', 'Publius', 'Marcus', 'Lucius'],
['Publilia', 'pleb', 'Volero', 'Lucius', 'Quintus', 'Gaius', 'Titus'],
['Pupia', 'pleb', 'Gnaeus', 'Lucius', 'Marcus', 'Publius', 'Aulus'],
['Quinctia', 'pat', 'Lucius', 'Titus', 'Caeso', 'Gnaeus', 'Quintus'],
['Quinctilia', 'pat', 'Publius', 'Sextus', 'Lucius', 'Marcus', 'Titus'],
['Rabuleia', 'pleb', 'Gaius', 'Manius', 'Quintus', 'Sextus', 'Lucius', 'Publius'],
['Racilia', 'pleb', 'Gaius', 'Lucius', 'Gnaeus', 'Marcus', 'Publius', 'Quintus', 'Titus'],
['Romilia', 'pat', 'Titus', 'Lucius', 'Gaius'],
['Roscia', 'pleb', 'Lucius', 'Marcus', 'Quintus', 'Sextus', 'Titus'],
['Salonia', 'pleb', 'Publius', 'Gaius', 'Quintus', 'Marcus'],
['Scaptia', 'pleb', 'Publius', 'Marcus', 'Lucius', 'Manius', 'Gaius', 'Statius'],
['Seccia', 'pleb', 'Gaius', 'Gnaeus', 'Lucius', 'Sextus'],
['Sempronia', 'pat', 'Aulus', 'Lucius', 'Gaius', 'Publius', 'Tiberius', 'Marcus', 'Titus'],
['Sergia', 'pat', 'Lucius', 'Manius', 'Gaius', 'Marcus', 'Gnaeus', 'Quintus'],
['Servilia', 'pat', 'Publius', 'Quintus', 'Spurius', 'Gaius', 'Gnaeus', 'Quintus', 'Marcus'],
['Sestia', 'pat', 'Publius', 'Lucius', 'Vibius', 'Titus'],
['Sextia', 'pleb', 'Marcus', 'Gaius', 'Lucius', 'Publius', 'Quintus', 'Titus', 'Sextus', 'Numerius', 'Vibius'],
['Sextilia', 'pleb', 'Gaius', 'Lucius', 'Marcus', 'Publius', 'Quintus'],
['Sicinia', 'pleb', 'Lucius', 'Gaius', 'Gnaeus', 'Titus', 'Quintus'],
['Sulpicia', 'pat', 'Publius', 'Servius', 'Quintus', 'Gaius', 'Marcus'],
['Tarpeia', 'pat', 'Spurius', 'Marcus', 'Lucius'],
['Tarquinia', 'pleb', 'Lucius', 'Sextus', 'Publius', 'Marcus', 'Appius', 'Gnaeus', 'Quintus', 'Gaius'],
['Tarquitia', 'pat', 'Lucius', 'Gaius', 'Quintus'],
['Terentia', 'pleb', 'Gaius', 'Marcus', 'Aulus', 'Publius', 'Quintus'],
['Terentilia', 'pleb', 'Gaius', 'Publius', 'Quintus', 'Statius', 'Titus'],
['Tullia', 'pleb', 'Marcus', 'Lucius', 'Quintus', 'Manius', 'Sextus', 'Tiberius'],
['Valeria', 'pat', 'Volesus', 'Publius', 'Marcus', 'Manius', 'Lucius', 'Gaius', 'Quintus', 'Aulus', 'Numerius', 'Sextus', 'Tiberius', 'Titus'],
['Verginia', 'pleb', 'Opiter', 'Proculus', 'Titus', 'Aulus', 'Lucius', 'Spurius'],
['Veturia', 'pat', 'Gaius', 'Titus', 'Spurius', 'Lucius', 'Publius', 'Tiberius', 'Marcus', 'Postumus'],
]

// This object will contain all gentes and their relevant information
const gentes = {};

// This function will populate the 'gentes' object from the arrays
function popGentes(){
    for(let gensArr of gentesArr) {
        gentes[gensArr[0]] = {'class' : gensArr[1], 'praenomina' : gensArr.slice(2,gensArr.length)}
    }
    return gentes;
}

// This object will contain the choices made
const character = {};

//const makePraenomina = function() {
function makePraenominaSection() {
    const praenominaExplanation = document.querySelector('#praenominaExplanation');
    const previousPraenomina = document.querySelector('#praenomina') 
    const previousStats = document.querySelector('#genStats');
    if(previousPraenomina) {
	previousPraenomina.remove();        
    }
    if(previousStats) previousStats.remove();
    if(character['praenomen']) {
        character['praenomen'] = false;
    }
    if(character['stats']) character['stats'] = false;
	const praenomina = document.createElement('div');
	praenomina.setAttribute("id","praenomina");
	praenomina.setAttribute("class","d-flex justify-content-center")
	praenominaExplanation.append(praenomina);
    const availPraenom = selectPraenomina();
    for(let name of availPraenom) {
        const praenomen = document.createElement('input');
        praenomen.setAttribute("value", name);
//        praenomen.setAttribute("class", "btn btn-danger");
        praenomen.setAttribute("type", "radio");
//        praenomen.style.margin = '2px';
        praenomen.setAttribute("id", name);
	praenomen.setAttribute("name",'praenomen');
	praenomen.required = true;
        praenomina.append(praenomen,name);
        praenomen.addEventListener('click', () => {
            character['praenomen'] = name;
            if(character['gens'] && character['gender'] && character['praenomen']){
                makeStatsSection();
            }
//            if(character['gender']) makePraenominaSection();
        });
    }
    
}

// This function will return an array of praenomina available from the
// gens
function selectPraenomina() {
    const chosenGens = character['gens'];
    const origPraenom = gentes[chosenGens]['praenomina'];
    if(character['gender'] === 'Female'){
        const availPraenom = [];
        for(let praenomen of origPraenom){
            if(praenomen === 'Marcus' || praenomen === 'Tullus' || praenomen === 'Titus'){
                praenomen = praenomen.slice(0,-2) + 'ia';
            }
            else if(praenomen.slice(-2,praenomen.length) === 'us'){
                praenomen = praenomen.slice(0,-2) + 'a';
            }
            else if(praenomen === 'Agrippa') praenomen = 'Agrippina';
            else if(praenomen === 'Caeso') praenomen = 'Caesula';
            else if(praenomen === 'Opiter') praenomen = 'Opita';
            else if(praenomen === 'Sertor') praenomen = 'Sertora';
            else if(praenomen === 'Volero') praenomen = 'Volerona';
            availPraenom.push(praenomen);
        }
        return availPraenom;
    }

    return origPraenom;
}

// This function will populate the page with buttons representing each clan
function clanButtons() {
    const gentes = popGentes();
    const clans = document.querySelector('#clans');
    for(let key in gentes) {
        const clan = document.createElement('input');
        clan.setAttribute("value", key);
//       clan.setAttribute("class", "btn btn-primary");
        clan.setAttribute("type", "radio");
//        clan.style.margin = '2px';
        clan.setAttribute("id", key);
	clan.setAttribute('name','gens');
	clan.required = true;
        clans.append(clan,key);
        clan.addEventListener('click', () => {
            character['gens'] = key;
            if(character['gender']) makePraenominaSection();
        });
    }
}

// This function will attach listeners to the gender buttons
function genderButtons() {
    const femaleButton = document.querySelector('#Female');
    const maleButton = document.querySelector('#Male');
    const genderChoice = [femaleButton, maleButton];
    for(let c of genderChoice){
        c.addEventListener('click', () => {
            character['gender'] = c.getAttribute('id');
            if(character['gens']) makePraenominaSection();
        });
    }
}

function makeStatsSection() {
    const statExplanation = document.querySelector('#statExplanation');
    const previousStats = document.querySelector('#genStats');
    if(previousStats) previousStats.remove();
    const genStats = document.createElement('div');
	genStats.setAttribute("id","genStats");
//	genStats.setAttribute("class","d-flex justify-content-center")
	statExplanation.append(genStats);
    makeStatsContent(genStats);
}

function makeStatsContent(genStats) {
//    const genStats = document.querySelector('#genStats');
    let stats = makeStatNumbers();
    const statChart = document.createElement('ul');
    let statString = '';
    const latinStats = {
        'str' : 'Vires',
        'dex' : 'Celeritas',
        'con' : 'Valetudo',
        'int' : 'Scientia',
        'wis' : 'Sapientia',
        'cha' : 'Gratia'
    }
    statChart.setAttribute("class", "list-group");
    for(let stat in stats){
        const ability = document.createElement('li');
        ability.setAttribute('class','list-group-item d-flex justify-content-between align-items-center');
        const num = document.createElement('span');
        num.setAttribute('class','badge badge-primary badge-pill');
        num.setAttribute('id',stat);
        num.innerText = stats[stat];
        ability.innerText = `${latinStats[stat]} (${stat})`;
        genStats.append(ability)
        ability.append(num)
	statString += (stats[stat] + ','); 
    }
    const acceptBtn = document.createElement('input');
    acceptBtn.setAttribute("value", statString);
//    acceptBtn.setAttribute("class", "btn btn-warning");
    acceptBtn.setAttribute("type", "checkbox");
//   acceptBtn.style.margin = '2px';
    acceptBtn.setAttribute("id", 'accept');
    acceptBtn.setAttribute('name', 'statAccept')
    acceptBtn.required = true;
    acceptBtn.addEventListener('click', () => {
        character['stats'] = stats;
    });
    genStats.append(acceptBtn);
    const rerollBtn = document.createElement('input');
    rerollBtn.setAttribute("value", 'Reroll');
    rerollBtn.setAttribute("class", "btn btn-warning");
    rerollBtn.setAttribute("type", "button");
    rerollBtn.style.margin = '2px';
    rerollBtn.setAttribute("id", 'reroll');
    rerollBtn.addEventListener('click', () => {
        character['stats'] = false;
        makeStatsSection(); 
    });
    genStats.append(rerollBtn);
}

function makeStatNumbers() {
    let statNums = [0,0,0,0,0,0];
    let points = 27;
    while(points > 0){
        let idx = Math.floor(Math.random() * statNums.length);
        if(statNums[idx] < 5 && points > 0) {
            statNums[idx] += 1;
            points -= 1;
        }
        else if ((statNums[idx] === 5 || statNums[idx] === 6) && points > 1) {
            statNums[idx] += 1;
            points -= 2;
        }
    }
    const stats = {
        'str' : statNums[0] + 9,
        'dex' : statNums[1] + 9,
        'con' : statNums[2] + 9,
        'int' : statNums[3] + 9,
        'wis' : statNums[4] + 9,
        'cha' : statNums[5] + 9
    }
    return stats;
}

clanButtons();
genderButtons();

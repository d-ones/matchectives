var score = '';
var guesses = 0;
let arrLines = [];
let prior_guesses = [];
let keyword = '';
let end_score = 0
let temp_score = 0
var forbidden_chars = [' ', '-']
pnrs = '';
var modal = document.getElementById("myModal");

let textInput = document.getElementById('entrybox') // take the element value
  textInput.addEventListener('input', (test) => { //whenever event input happend
    if(textInput.value.length == 0){
    document.getElementById('counter').innerHTML = "";
}
  else{
    document.getElementById('counter').innerHTML = "\uD83D\uDCAC";}
})


function init_score() {
  document.getElementById('keyword').innerHTML = keyword;
  }

function LoadFile() {
    var oFrame = document.getElementById("frmFile");
    var strRawContents = oFrame.contentWindow.document.body.childNodes[0].innerHTML;
    while (strRawContents.indexOf("\r") >= 0)
        strRawContents = strRawContents.replace("\r", "");
    arrLines = strRawContents.split("\n");
    arrLines.reverse()
    }

function LoadKeyword() {
    var oFrame = document.getElementById('frmWordFile');
    var strRawContents = oFrame.contentWindow.document.body.childNodes[0].innerHTML;
    keyword = strRawContents;
    }

  function insertLineBreaks(str) {
    let result = '';
    for (let i = 0; i < str.length; i++) {
        result += str[i];
        if ((i + 1) % 5 === 0) {
            result += '\n';
        }
    }
    return result;
}

function answer_fc(ele){
    event.preventDefault()
    document.getElementById('counter').innerHTML = "";
    var v1 = document.getElementById('entrybox').value;
    if(prior_guesses.includes(v1.toLowerCase())){
          document.getElementById('counter').innerHTML = "\u26A0\uFE0F";
          return;
    }
    if(v1.length == 0){
          document.getElementById('counter').innerHTML = "\u26A0\uFE0F";
          return;
  }
  if(forbidden_chars.some(substring=>v1.includes(substring))){
          document.getElementById('counter').innerHTML = "\u26A0\uFE0F";
          return;
    }
    prior_guesses.push(v1.toLowerCase())
  if(arrLines.includes(v1.toLowerCase())){
            document.getElementById('counter').innerHTML = "\u2705";
            score += "\u2705";
            temp_score = arrLines.indexOf(v1.toLowerCase());
            temp_score += 1
            pnrs = v1.toLowerCase() + " +" + temp_score + "<br>" + pnrs;
            end_score += temp_score;
            document.getElementById('point_notif').innerHTML = pnrs
            guesses++;
    }
    else {
            document.getElementById('counter').innerHTML = "\u274c";
            score += "\u274C"
      }

    if (guesses == 5) {
            modal.style.display = "block";
            document.getElementById('modal-text').innerHTML = "Congrats! Your score is " + end_score + ".";
            document.getElementById('modal-score').innerHTML = score;
            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
                document.getElementById('entrybox').disabled = true;
            }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                document.getElementById('entrybox').disabled = true;
            }
          }
      }
}
function copyscore(){
  const date = new Date();
  let day = date.getDate();
  let month = date.getMonth() + 1;
  let year = date.getFullYear();
  // This arrangement can be altered based on how we want the date's format to appear.
  let currentDate = `${month}/${day}/${year}`;
  scorewithbreaks = insertLineBreaks(score)
  var copyText = "matchectives.com" + "\n" + currentDate + ": " + end_score + "\n\n" + scorewithbreaks;
  navigator.clipboard.writeText(copyText);
}

// Get the modal
var modal = document.getElementById("myModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var State = {
  story: { value: [], watchers: [] },
  achievements: { value: [], watchers:[] },
  custom: {value: false, watchers: []},
  wallet: {value: '', watchers: []},
  path: {value: '', watchers: []} //Holds the current URL
};

var intro_prompt = "Date:7/1\nBranch:In this world, you can be who you want to be. All you must do is awaken and enter your truest desires. Let the games begin! \nEmotion: optimistic | Adjectives: exicted, fascinated | Energy: 100% | Water: 100% | Integrity: 100% | Affiliation: 100% | Certainity: 100% | Competence: 100%\nAchievement: Trepid Adventurer\nBranch A: Start the adventure! | Branch B: Stay in bed.\n> You choose Branch A.\n------------\n\n"

function doNav() {
  if (location.hash == "") {
    Transition("hq");
  } else {
    console.log('hash: ' + location.hash)
    let route = location.hash.slice(1);
    let subroute = route.split('/');
    path = subroute[1];
    UpdateState('path',route)
    Transition(route)
  }
}

function On(key, watcher) {
  State[key].watchers.push(watcher);
}

function Transition(route) {
  if (location.hash == "")
    route = 'hq'
  console.log("Route: " + route)
  TransitionTable[route].updater();
  TransitionTable[route].loader();
}

function UpdateState(key, value) {
  if (State[key].value === value) return;
  if (!(State[key].value instanceof Array)) {
    console.log("Not array");
    State[key].value = value;
    for (w in State[key].watchers) {
      State[key].watchers[w](value);
    }
  } else {
      console.log("Array");
      State[key].value.push(value);
      for (w in State[key].watchers) {
        State[key].watchers[w](value);
      }
  }
}

var TransitionTable = {
  hq: {
    loader: function () {
      $("#current").html(document.getElementById("hq").innerHTML);

    },
    updater: function() {}
  },

  about: {
    loader: function () {
      $("#current").html(document.getElementById("about").innerHTML);
    },
    updater: function() {}
  }

}

$(window).on("hashchange", function() {
  let route = location.hash.slice(1);
  let subroute = route.split('/')
  path = subroute[1];
  UpdateState('path',route)
  console.log('path:' + path);
  if (route == "") Transition("hq");

  if (route == "modal1" || route == "modal2" || route == "!") return;

  Transition(route);
});

function toggleModal () {

      const body = document.querySelector('body')
      const modal = document.querySelector('.modal')
      modal.classList.toggle('opacity-0')
      modal.classList.toggle('pointer-events-none')
      body.classList.toggle('modal-active')
}

 function doModal() {
   var openmodal = document.querySelectorAll('.modal-open')
    for (var i = 0; i < openmodal.length; i++) {
      openmodal[i].addEventListener('click', function(event){
    	event.preventDefault()
    	toggleModal()
      })
    }

    const overlay = document.querySelector('.modal-overlay')
    overlay.addEventListener('click', toggleModal)

    var closemodal = document.querySelectorAll('.modal-close')
    for (var i = 0; i < closemodal.length; i++) {
      closemodal[i].addEventListener('click', toggleModal)
    }

    document.onkeydown = function(evt) {
      evt = evt || window.event
      var isEscape = false
      if ("key" in evt) {
    	isEscape = (evt.key === "Escape" || evt.key === "Esc")
      } else {
    	isEscape = (evt.keyCode === 27)
      }
      if (isEscape && document.body.classList.contains('modal-active')) {
    	toggleModal()
      }
    };
 }

window.addEventListener("load", async () => {

  doModal();

  try {
    const resp = await window.solana.connect();
    console.log(resp.publicKey.toString())
    UpdateState('wallet',resp.publicKey.toString())

    // 26qv4GCcx98RihuK3c4T6ozB3J7L6VwCuFVc7Ta2A3Uo
} catch (err) {
    alert("Please connect to your web wallet to earn NFTs!")
}

  On("story", function (v) {

    html = v.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $('#journal').append('<div class="w-11/12 mt-4 mr-8 px-8 bg-green-800 p-3 rounded-lg text-white ">' + html + '</p></div>')
  })

  On("achievements", function(v) {
    html = v.replace(/(?:\r\n|\r|\n)/g, '');
    console.log(html)
    $('#ach').append('<div class="w-11/12 mt-4 mr-8 px-8 bg-blue-600 p-3 rounded-lg text-white" onclick=addressPopup(\''+ html.trim() + '\')>' + html + '</p></div>')
  })

  parseStory(intro_prompt.split('------------'))

});



function showStoryModal() {
  //$("#modal-content").html(document.getElementById('createModal').innerHTML);
  if(State.path.value != 'about') {
     toggleModal();
  }
}

function doNewStory() {
  UpdateState("custom", true);
  var params = {};

  params['story'] = $('#story').val()
  params['init_energy'] = $('#init_energy').val()
  params['init_water'] = $('#init_water').val()
  params['init_integrity'] = $('#init_integrity').val()
  params['init_affiliation'] = $('#init_affiliation').val()
  params['init_certainty'] = $('#init_certainty').val()
  params['init_competence'] = $('#init_competence').val()
  params['branch_a'] = $('#branch_a').val()
  params['branch_b'] = $('#branch_b').val()
  params['init_emotion'] = $('#init_emotion').val()
  params['adj_one'] = $('#adj_one').val()
  params['adj_two'] = $('#adj_two').val()
  params['init_ach'] = $('#init_ach').val()
  params['wallet'] = State.wallet.value

  console.log(params)
  toggleModal();

  //Add init prompt:
  stats_bar = "Emotion: " + params['init_emotion'] + " | Adjectives: " + params['adj_one'] + ", " + params['adj_two'] + " | Energy: " + params['init_energy'] + " | Water: " + params['init_water'] + " | Integrity: " + params['init_integrity'] + " | Affiliation: " + params['init_affiliation'] +" | Certainty: " + params[init_certainty] + " | Competence: " + params['init_competence'] + "\n"
  branches = "Branch A: " + params["branch_a"] + " | " + "Branch B: " + params["branch_b"] + "\n"
  prompt = "Date:7/2\n Branch: " + params['story'] + stats_bar + "Achievement: " + params['init_ach'] + "\n" + branches
  the_array = []
  the_array.push(prompt)
  parseStory(the_array);

}

function doBranchA() {
  if  ( State.story.value.length == 2 && State.custom.value) {
     initBranchA();
     return
  }

  test = State.story.value.slice(-3);
  new_prompt = test.join('\n------------\n').slice(0,-14)

  console.log("raw: " + new_prompt)

  console.log("Substring: " + new_prompt);
  new_prompt = new_prompt + '\n> You chose branch A'
  new_prompt += '\n------------\n'

  console.log("New Prompt: " + new_prompt )

  var params = {text: new_prompt, wallet: State.wallet.value};
  fetch('http://localhost:8080/continue', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'text/json',
  },
  body: JSON.stringify(params),
})
.then(response=>response.text())
.then(data=>{ parseStory(data.split('------------')); })
.catch((error) => {
  console.error('Error:', error);
});
}

function doBranchB() {
  if  ( State.story.value.length == 2 && State.custom.value) {
     initBranchB();
     return
  }


  test = State.story.value.slice(-3);
  new_prompt = test.join('\n------------\n').slice(0,-14)

  console.log("raw: " + new_prompt)

  new_prompt = new_prompt + '\n> You chose branch B'
  new_prompt += '\n------------\n'

  console.log("New Prompt: " + new_prompt )

  var params = {text: new_prompt, wallet: State.wallet.value};
  fetch('http://localhost:8080/continue', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'text/json',
  },
  body: JSON.stringify(params),
})
.then(response=>response.text())
.then(data=>{ parseStory(data.split('------------')); })
.catch((error) => {
  console.error('Error:', error);
});

}

function parseStory(text) {
   console.log("The text:" + text)

   //Remove the prompt:
   index = text[0].lastIndexOf('>') == -1 ?  text[0].length : text[0].lastIndexOf('>')-1
   journal_text = text[0].substring(0, index);

   //Find Acheivement
   lines = journal_text.split('\n')
   const found = lines.find(element => element.indexOf("Achievement: ") > -1);
   if (found != undefined) {
     the_achievement = found.slice(13);
     console.log("the_achievement: " + the_achievement)
   }

   UpdateState("achievements",the_achievement);
   UpdateState("story",journal_text);
}

function initBranchA() {
  var params = {};

  params['story'] = $('#story').val()
  params['init_energy'] = $('#init_energy').val()
  params['init_water'] = $('#init_water').val()
  params['init_integrity'] = $('#init_integrity').val()
  params['init_affiliation'] = $('#init_affiliation').val()
  params['init_certainty'] = $('#init_certainty').val()
  params['init_competence'] = $('#init_competence').val()
  params['branch_a'] = $('#branch_a').val()
  params['branch_b'] = $('#branch_b').val()
  params['init_emotion'] = $('#init_emotion').val()
  params['adj_one'] = $('#adj_one').val()
  params['adj_two'] = $('#adj_two').val()
  params['init_ach'] = $('#init_ach').val()
  params['init_choice'] = 'A'
  params['wallet'] = State.wallet.value


  fetch('http://localhost:8080', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(params),
})
.then(response=>response.text())
.then(data=>{ parseStory(data.split('------------')); })
.catch((error) => {
  console.error('Error:', error);
});
}

function initBranchB() {
  var params = {};

  params['story'] = $('#story').val()
  params['init_energy'] = $('#init_energy').val()
  params['init_water'] = $('#init_water').val()
  params['init_integrity'] = $('#init_integrity').val()
  params['init_affiliation'] = $('#init_affiliation').val()
  params['init_certainty'] = $('#init_certainty').val()
  params['init_competence'] = $('#init_competence').val()
  params['branch_a'] = $('#branch_a').val()
  params['branch_b'] = $('#branch_b').val()
  params['init_emotion'] = $('#init_emotion').val()
  params['adj_one'] = $('#adj_one').val()
  params['adj_two'] = $('#adj_two').val()
  params['init_ach'] = $('#init_ach').val()
  params['init_choice'] = 'B'
  params['wallet'] = State.wallet.value

  fetch('http://localhost:8080', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(params),
})
.then(response=>response.text())
.then(data=>{ parseStory(data.split('------------')); })
.catch((error) => {
  console.error('Error:', error);
});
}

function debugStory()
{
  console.log(State.story.value.join('\n------------\n'));
}

function addressPopup(name) {
 var params = {"name": name}
 fetch('http://localhost:8080/addr', {
 method: 'POST', // or 'PUT'
 headers: {
   'Content-Type': 'application/json',
 },
 body: JSON.stringify(params),
}).then(response=>response.text())
.then(data=>{ alert("Address: " + data)  })
.catch((error) => {
  console.error('Error:', error);
});


}

let url = new URL("/", window.location.protocol + "//" + window.location.host);

if (!checkAuth()){
  const form = document.createElement("form");
  form.id = "form"

  const el1 = document.createElement("input");
  el1.className = "input_el";
  el1.placeholder = "email";
  el1.id = "email";

  const el2 = document.createElement("input");
  el2.className = "input_el";
  el2.placeholder = "password";
  el2.id = "password";

  const btn = document.createElement("button")
  btn.textContent = "SUBMIT"
  
  form.appendChild(el1);
  form.appendChild(el2);
  form.appendChild(btn);

  const wrap = document.getElementById("wrapper");
  wrap.appendChild(form);
  listen();

}



if (checkJWT()) {
  let xhrRefresh = new XMLHttpRequest();

  xhrRefresh.open("GET", "/api/auth/refresh");
  xhrRefresh.send();
  xhrRefresh.onload = () => {
    if (xhrRefresh.status == 200) {
      location.reload();
    }
  };
}

function listen(){
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
  
    var xhr = new XMLHttpRequest();
    xhr.open("POST", (URL = "/api/auth/login"));
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    xhr.send(JSON.stringify({
      "email": email,
      "password": password
  }));

    xhr.onload = () => {
      if (xhr.status == 200) {
        location.assign(url);
      } else {
        alert("User not found");
      }
    };
  });
  
}

function checkJWT() {
  let token = getCookie("access_token");
  if (token == "") {
    return true;
  }

  if (
    Number(JSON.parse(atob(token.split(".")[1])).exp) - 3 <
    Math.floor(Date.now() / 1000)
  ) {
    return true;
  }
  return false;
}



function checkAuth(){
  let refresh = getCookie("refresh_token")
  if (refresh == "" && checkJWT()){
    return false;
  }else{
    return true;
  }
}


function getCookie(cookie) {
  cookie += "=";
  let cookies = document.cookie.split("; ");
  let token = "";

  cookies.forEach((element) => {
    if (element.substring(0, cookie.length) == cookie) {
      token = element.substring(cookie.length, element.length);
    }
  });
  return token;
}


// xhr.send(JSON.stringify({
//   value: value
// }));